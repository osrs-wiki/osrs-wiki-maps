### Build a large image out of the region tiles produced by RuneLite's image dumper
import glob
import multiprocessing.dummy
import os
from PIL import Image
import time
from memory_profiler import profile, memory_usage
import multiprocessing

# Pyvips on windows is finnicky
# Windows binaries are required: https://pypi.org/project/pyvips/, https://www.libvips.org/install.html
LIBVIPS_VERSION = "8.15"
vipsbin = os.path.join(os.getcwd(), f"vipsbin/vips-dev-{LIBVIPS_VERSION}/bin")
os.environ['PATH'] = os.pathsep.join((vipsbin, os.environ['PATH']))
import pyvips as pv

@profile
def buildCompositeImage():
	### Configure this before running the script
	VERSION = "2024-04-10_a"
	regionPath = f"./osrs-wiki-maps/out/mapgen/versions/{VERSION}"
	OUTPUT_PATH = f"./osrs-wiki-maps/out/mapgen/versions/{VERSION}/composites"
	REGION_TILE_LENGTH = 64
	TILE_PIXEL_LENGTH = 4
	MAX_MAP_SIDE_LENGTH = 999 # in regions
	PLANE_COUNT = 4

	# Identify files produced by the dumper
	fileType = "/*.png"
	regionImageFilePaths = glob.glob(f"{regionPath}/tiles/base/{fileType}")

	# Range the image dimensions
	lowerX = lowerY = MAX_MAP_SIDE_LENGTH
	upperX = upperY = 0
	for regionFilePath in regionImageFilePaths:
		fileName = os.path.splitext(os.path.basename(regionFilePath))[0]
		plane, x, y = map(int, fileName.split("_")) # Expecting {plane}_{x}_{y}
		lowerX = min(lowerX, x)
		lowerY = min(lowerY, y)
		upperX = max(upperX, x)
		upperY = max(upperY, y)

	# Arrayjoin approach
	# Need to load in images for ALL tiles to use arrayjoin
	# This means supplying black images for tiles which are not produced by the region dumper
	# Arrayjoin executes top to bottom, left to right
	pool = multiprocessing.dummy.Pool(4)
	for plane in range(0, PLANE_COUNT):
		pool.apply_async(assemblePlane, args=(plane, upperX, upperY, lowerX, lowerY, regionPath, regionImageFilePaths, REGION_TILE_LENGTH, TILE_PIXEL_LENGTH, OUTPUT_PATH))
	pool.close()
	pool.join()

def assemblePlane(plane, upperX, upperY, lowerX, lowerY, regionPath, regionImageFilePaths, REGION_TILE_LENGTH, TILE_PIXEL_LENGTH, OUTPUT_PATH):
	# Load in the plane's region images
	regionArray = list()
	for regionY in range(upperY, lowerY-1, -1):
		for regionX in range(lowerX, upperX+1, 1):			
			targetRegionFileName = os.path.normpath(os.path.join(regionPath, f"{plane}_{regionX}_{regionY}.png")).replace("\\", "/")
			# If we have an image already just load it in
			if targetRegionFileName in regionImageFilePaths:
				regionArray.append(pv.Image.new_from_file(targetRegionFileName))
			else:
				# Otherwise, provide a blank image
				regionArray.append(pv.Image.black(REGION_TILE_LENGTH * TILE_PIXEL_LENGTH, REGION_TILE_LENGTH * TILE_PIXEL_LENGTH))
	# Join the region images and write the result to file
	planeImage = pv.Image.arrayjoin(regionArray, across=(upperX-lowerX+1))
	planeImage.write_to_file(os.path.join(OUTPUT_PATH, f"plane_{plane}.png"))

if __name__ == "__main__":
	startTime = time.time()
	# buildCompositeImage()
	print(f"Peak memory usage: {max(memory_usage(proc=buildCompositeImage))}")
	print(f"Runtime: {time.time()-startTime}")
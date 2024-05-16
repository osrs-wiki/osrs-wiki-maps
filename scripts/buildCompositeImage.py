### Build a large image out of the region tiles produced by RuneLite's image dumper
import glob
import os
import time
from memory_profiler import profile, memory_usage
import multiprocessing
import cv2
import numpy as np

### Configure this before running the script
VERSION = "2024-04-10_a"
regionPath = f"./osrs-wiki-maps/out/mapgen/versions/{VERSION}/tiles/base"
OUTPUT_PATH = f"./osrs-wiki-maps/out/mapgen/versions/{VERSION}/composites"
REGION_TILE_LENGTH = 64
TILE_PIXEL_LENGTH = 4
REGION_PIXEL_LENGTH = REGION_TILE_LENGTH * TILE_PIXEL_LENGTH
MAX_MAP_SIDE_LENGTH = 999 # in regions
PLANE_COUNT = 4

# Identify files produced by the dumper
fileType = "/*.png"
regionImageFilePaths = [os.path.normpath(path) for path in glob.glob(f"{regionPath}{fileType}")]

# Define empty region appearance
emptyRegion = np.zeros((REGION_PIXEL_LENGTH, REGION_PIXEL_LENGTH, 3), dtype=np.uint8)

@profile
def assemblePlanes(plane, upperX, upperY, lowerX, lowerY):
	imageRows = list()
	for regionY in range(upperY, lowerY-1, -1):
		imageRow = list()
		for regionX in range(lowerX, upperX+1, 1):
			targetRegionFileName = os.path.normpath(os.path.join(regionPath, f"{plane}_{regionX}_{regionY}.png"))
			# If the region image exists, load it in
			if targetRegionFileName in regionImageFilePaths:
				imageRow.append(cv2.imread(targetRegionFileName, cv2.IMREAD_COLOR))
			else:
				imageRow.append(emptyRegion)
		# Merge horizontally
		row = np.hstack(imageRow)
		imageRows.append(row)
	# Merge verticall
	image = np.vstack(imageRows)
	cv2.imwrite(os.path.join(OUTPUT_PATH, f"plane_{plane}.png"), image)

def buildCompositeImage():
	# Range the image dimensions
	lowerX = lowerY = MAX_MAP_SIDE_LENGTH
	upperX = upperY = 0
	for regionFilePath in regionImageFilePaths:
		fileName = os.path.splitext(os.path.basename(regionFilePath))[0]
		_, x, y = map(int, fileName.split("_")) # Expecting {plane}_{x}_{y}
		lowerX = min(lowerX, x)
		lowerY = min(lowerY, y)
		upperX = max(upperX, x)
		upperY = max(upperY, y)

	planeRenderArgs = list()
	for plane in range(0, PLANE_COUNT):
		# assemblePlanes(plane, upperX, upperY, lowerX, lowerY)
		planeRenderArgs.append((plane, upperX, upperY, lowerX, lowerY))

	# Assign one core per plane image
	with multiprocessing.Pool() as pool:
		pool.starmap(assemblePlanes, planeRenderArgs)

if __name__ == "__main__":
	startTime = time.time()
	# buildCompositeImage()
	print(f"Peak memory usage: {max(memory_usage(proc=buildCompositeImage))}")
	print(f"Runtime: {time.time()-startTime}")
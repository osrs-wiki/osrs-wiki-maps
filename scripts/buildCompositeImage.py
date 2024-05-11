### Build a large image out of the region tiles produced by RuneLite's image dumper
import glob
import os
from PIL import Image

### Configure this before running the script
VERSION = "2024-04-10_a"
regionPath = f"./osrs-wiki-maps/out/mapgen/versions/{VERSION}"
OUTPUT_PATH = f"./osrs-wiki-maps/out/mapgen/versions/{VERSION}/composites"
REGION_TILE_LENGTH = 64
TILE_PIXEL_LENGTH = 4
MAX_SIDE_LENGTH = 999 # in regions

# Identify files produced by the dumper
fileType = "/*.png"
tileImageFilePaths = glob.glob(f"{regionPath}/tiles/base/{fileType}")

# Range the image dimensions
lowerX = lowerY = MAX_SIDE_LENGTH
upperX = upperY = 0
for regionFilePath in tileImageFilePaths:
	fileName = os.path.splitext(os.path.basename(regionFilePath))[0]
	plane, x, y = map(int, fileName.split("_")) # Expecting {plane}_{x}_{y}
	lowerX = min(lowerX, x)
	lowerY = min(lowerY, y)
	upperX = max(upperX, x)
	upperY = max(upperY, y)

# Remember there's a fencepost problem here, add one tile length of pixels
compositeWidth = (upperX - lowerX + 1) * REGION_TILE_LENGTH * TILE_PIXEL_LENGTH
compositeHeight = (upperY - lowerY + 1) * REGION_TILE_LENGTH * TILE_PIXEL_LENGTH

# We aren't rendering tiles from (0,0), so find the offset from unused region IDs
hOffset = (upperX + 1) * REGION_TILE_LENGTH * TILE_PIXEL_LENGTH - compositeWidth
vOffset = (upperY + 1) * REGION_TILE_LENGTH * TILE_PIXEL_LENGTH - compositeHeight

# Declare composite image object
compositeImages = {
	0: (Image.new('RGB', (compositeWidth, compositeHeight)), "plane_0.png"),
	1: (Image.new('RGB', (compositeWidth, compositeHeight)), "plane_1.png"),
	2: (Image.new('RGB', (compositeWidth, compositeHeight)), "plane_2.png"),
	3: (Image.new('RGB', (compositeWidth, compositeHeight)), "plane_3.png")
}

# Push region images into the composites, per plane
for regionFilePath in tileImageFilePaths:
	fileName = os.path.splitext(os.path.basename(regionFilePath))[0]
	plane, x, y = map(int, fileName.split("_"))
	# Transform region data to location in the composite image
	# Image references top left corner as origin, while Jagex uses bottom left
	compositeXCoord = (x * REGION_TILE_LENGTH * TILE_PIXEL_LENGTH) - hOffset
	compositeYCoord = compositeHeight - ((y * REGION_TILE_LENGTH * TILE_PIXEL_LENGTH) - vOffset)
	# Paste the region image into the composite image
	regionImage = Image.open(regionFilePath)
	compositeImages[plane][0].paste(regionImage, (compositeXCoord, compositeYCoord))

# Save images
if not os.path.exists(OUTPUT_PATH):
	os.makedirs(OUTPUT_PATH)
for (composite, name) in compositeImages.values():
	composite.save(os.path.join(OUTPUT_PATH, name))
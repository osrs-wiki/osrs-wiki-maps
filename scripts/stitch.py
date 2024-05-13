import json
import os
from PIL import Image, ImageFilter
import os.path
import errno
import glob
import numpy as np
from collections import defaultdict

version = "../out/mapgen/versions/2024-04-10_a"

with open("%s/worldMapDefinitions.json" % version) as f:
	defs = json.load(f)

with open("user_world_defs.json") as f:
    defs += json.load(f)
    
with open("%s/minimapIcons.json" % version) as f:
	icons = json.load(f)

iconSprites = {}
for file in glob.glob("%s/icons/*.png" % version):
	print(file)
	spriteId = int(file.split("/")[-1][:-4])
	iconSprites[spriteId] = Image.open(file)

overallXLow = 999
overallXHigh = 0
overallYLow = 999
overallYHigh = 0
for file in glob.glob("%s/tiles/base/*.png" % version):
	filename = file.split("/")[-1]
	filename = filename.replace(".png", "")
	plane, x, y = map(int, filename.split("_"))
	overallYHigh = max(y, overallYHigh)
	overallYLow = min(y, overallYLow)
	overallXHigh = max(x, overallXHigh)
	overallXLow = min(x, overallXLow)

defs.append({"name": "debug", "mapId": -1, "regionList": [{"xLowerLeft": overallXLow, "yUpperRight": overallYHigh, "yLowerRight": overallYLow, "yLowerLeft": overallYLow, "numberOfPlanes": 4, "xUpperLeft": overallXLow, "xUpperRight": overallXHigh, "yUpperLeft": overallYHigh, "plane": 0, "xLowerRight": overallXHigh}]})

def mkdir_p(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc:
        pass

def getBounds(regionList):
	lowX, lowY, highX, highY = 9999, 9999, 0, 0
	planes = 0
	for region in regionList:
		if 'xLowerLeft' in region: #typeA
			lowX = min(lowX, region['xUpperLeft'])
			highX = max(highX, region['xUpperRight'])
			lowY = min(lowY, region['yLowerLeft'])
			highY = max(highY, region['yUpperLeft'])
			planes = max(planes, region['numberOfPlanes'])
		elif 'newX' in region:
			lowX = min(lowX, region['newX'])
			highX = max(highX, region['newX'])
			lowY = min(lowY, region['newY'])
			highY = max(highY, region['newY'])
			planes = max(planes, region['numberOfPlanes'])
		elif 'xLow' in region:
			lowX = min(lowX, region['xLow'])
			highX = max(highX, region['xHigh'])
			lowY = min(lowY, region['yLow'])
			highY = max(highY, region['yHigh'])
			planes = max(planes, region['numberOfPlanes'])	
		else:
			raise ValueError(region)
	return lowX, highX, lowY, highY, planes

def pointInsideBox(position, plane, lowX, highX, lowY, highY, chunk_lowX, chunk_highX, chunk_lowY, chunk_highY, allPlanes):
	x = position['x']
	y = position['y']
	z = position['z']
	lowX = lowX * 64 + chunk_lowX * 8
	lowY = lowY * 64 + chunk_lowY * 8
	highX = highX * 64 + chunk_highX * 8 + 7
	highY = highY * 64 + chunk_highY * 8 + 7
	return ((plane == 0) or (plane == z)) and x >= lowX and x <= highX and y >= lowY and y <= highY

def getIconsInsideArea(plane, lowX, highX, lowY, highY, chunk_lowX=0, chunk_highX=7, chunk_lowY=0, chunk_highY=7, dx=0, dy=0, dz=0, allPlanes=False):
	valid = []
	for icon in icons:
		if pointInsideBox(icon['position'], plane, lowX, highX, lowY, highY, chunk_lowX, chunk_highX, chunk_lowY, chunk_highY, allPlanes):
			pos = icon['position']
			icon = [pos['x'] + dx, pos['y'] + dy, icon['spriteId']]
			valid.append(icon)
	return valid
def allBlack(im):
	data = np.asarray(im.convert('RGBA'))
	return np.all(data[:,:,:3] < 50)

PADDING = 64
baseMaps = []
px_per_square = 4
for defn in defs:
	mapId = -1
	if 'mapId' in defn:
		mapId = defn['mapId']
	elif 'fileId' in defn:
		mapId = defn['fileId']
	lowX, highX, lowY, highY, planes = getBounds(defn['regionList'])
	bounds = [[lowX * 64 - PADDING, lowY * 64 - PADDING], [(highX + 1) * 64 + PADDING, (highY + 1) * 64 + PADDING]]
	# bounds = [[0, 0], [12800, 12800]]
	if mapId < 1:
		center = [2496, 3328]
	elif 'position' in defn:
		center = [defn['position']['x'], defn['position']['y']]
	else:
		print('cent')
		center = [(lowX + highX + 1) * 32, (lowY + highY + 1) * 32]
	baseMaps.append({'mapId': mapId, 'name': defn['name'], 'bounds': bounds, 'center': center})
	overallHeight = (highY - lowY + 1) * px_per_square * 64
	overallWidth = (highX - lowX + 1) * px_per_square * 64
	
	plane0Map = None
	for plane in range(planes):
		print(mapId, plane)
		validIcons = []
		im = Image.new("RGB", (overallWidth + 512, overallHeight + 512))
		for region in defn['regionList']:
			if 'xLowerLeft' in region:
				oldLowX = region['xLowerLeft']
				oldHighX = region['xLowerRight']
				oldLowY = region['yLowerLeft']
				oldHighY = region['yUpperLeft']
				newLowX = region['xUpperLeft']
				newHighX = region['xUpperRight']
				newLowY = region['yLowerRight']
				newHighY = region['yUpperRight']
				print(oldLowX == newLowX, oldLowY == newLowY, oldHighX == newHighX, oldHighY == newHighY)
				validIcons.extend(getIconsInsideArea(region['plane'] + plane, oldLowX, oldHighX, oldLowY, oldHighY, allPlanes=plane==0))
				for x in range(oldLowX, oldHighX + 1):
					for y in range(oldLowY, oldHighY + 1):
						filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, x, y)
						if os.path.exists(filename):
							square = Image.open(filename)
							imX = (x-lowX+newLowX-oldLowX) * px_per_square * 64
							imY = (highY-y) * px_per_square * 64
							im.paste(square, box=(imX+256, imY+256))
			elif 'chunk_oldXLow' in region:
				filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['oldPlane'] + plane, region['oldX'], region['oldY'])
				dx = region['newX'] * 64 + region['chunk_newXLow'] * 8 - region['oldX'] * 64 - region['chunk_oldXLow'] * 8
				dy = region['newY'] * 64 + region['chunk_newYLow'] * 8 - region['oldY'] * 64 - region['chunk_oldYLow'] * 8
				dz = 0 - region['oldPlane']
				validIcons.extend(getIconsInsideArea(region['oldPlane'] + plane, region['oldX'], region['oldX'], region['oldY'], region['oldY'], region['chunk_oldXLow'], region['chunk_oldXHigh'], region['chunk_oldYLow'], region['chunk_oldYHigh'], dx, dy, dz, allPlanes=plane==0))
				if os.path.exists(filename):
					square = Image.open(filename)
					cropped = square.crop((region['chunk_oldXLow'] * px_per_square * 8,
					 (8-region['chunk_oldYHigh'] - 1) * px_per_square * 8,
					 (region['chunk_oldXHigh'] + 1) * px_per_square * 8,
					 (8-region['chunk_oldYLow']) * px_per_square * 8))
					imX = (region['newX']-lowX) * px_per_square * 64 + region['chunk_newXLow'] * px_per_square * 8
					imY = (highY-region['newY']) * px_per_square * 64 + (7-region['chunk_newYHigh']) * px_per_square * 8
					im.paste(cropped, box=(imX+256, imY+256))
			elif 'chunk_xLow' in region:
				validIcons.extend(getIconsInsideArea(region['plane'] + plane, region['xLow'], region['xHigh'], region['yLow'], region['yHigh'], region['chunk_xLow'], region['chunk_xHigh'], region['chunk_yLow'], region['chunk_yHigh'], allPlanes=plane==0))
				filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, region['xLow'], region['yLow'])
				if os.path.exists(filename):
					square = Image.open(filename)
					cropped = square.crop((region['chunk_xLow'] * px_per_square * 8,
					 (8-region['chunk_yHigh'] - 1) * px_per_square * 8,
					 (region['chunk_xHigh'] + 1) * px_per_square * 8,
					 (8-region['chunk_yLow']) * px_per_square * 8))
					imX = (region['xLow']-lowX) * px_per_square * 64 + region['chunk_xLow'] * px_per_square * 8
					imY = (highY-region['yLow']) * px_per_square * 64 + (7-region['chunk_yHigh']) * px_per_square * 8
					im.paste(cropped, box=(imX+256, imY+256))
			elif 'xLow' in region:
				validIcons.extend(getIconsInsideArea(region['plane'] + plane, region['xLow'], region['xHigh'], region['yLow'], region['yHigh'], allPlanes=plane==0))
				for x in range(region['xLow'], region['xHigh'] + 1):
					for y in range(region['yLow'], region['yHigh'] + 1):
						filename = "%s/tiles/base/%s_%s_%s.png" % (version, region['plane'] + plane, x, y)
						if os.path.exists(filename):
							square = Image.open(filename)
							imX = (x-lowX) * px_per_square * 64
							imY = (highY-y) * px_per_square * 64
							im.paste(square, box=(imX+256, imY+256))
			else:
				raise ValueError(region)
		if plane == 0:
			data = np.asarray(im.convert('RGB')).copy()
			data[(data == (255, 0, 255)).all(axis = -1)] = (0, 0, 0)
			im = Image.fromarray(data, mode='RGB')
			if planes > 1:
				plane0Map = im.convert('LA').filter(ImageFilter.GaussianBlur(radius=5))
		elif plane > 0:
			data = np.asarray(im.convert('RGBA')).copy()
			data[:,:,3] = 255*(data[:,:,:3] != (255, 0, 255)).all(axis = -1)
			mask = Image.fromarray(data, mode='RGBA')
			im = plane0Map.convert("RGBA")
			im.paste(mask, (0, 0), mask)

		for zoom in range(-3, 4):
			scalingFactor = 2.0**zoom/2.0**2
			zoomedWidth = int(round(scalingFactor * im.width))
			zoomedHeight = int(round(scalingFactor * im.height))
			resample = Image.BILINEAR if zoom <= 1 else Image.NEAREST
			zoomed = im.resize((zoomedWidth, zoomedHeight), resample=resample)
			if zoom >= 0:
				for x, y, spriteId in validIcons:
					sprite = iconSprites[spriteId]
					width, height = sprite.size
					imX = int(round((x - lowX * 64) * px_per_square * scalingFactor)) - width // 2 - 2
					imY = int(round(((highY + 1) * 64 - y) * px_per_square * scalingFactor)) - height // 2 - 2
					zoomed.paste(sprite, (imX+int(round(256*scalingFactor)), int(round(imY+256 * scalingFactor))), sprite)
			
			lowZoomedX = int((lowX - 1) * scalingFactor + 0.01)
			highZoomedX = int((highX + 0.9 + 1) * scalingFactor + 0.01)
			lowZoomedY = int((lowY - 1) * scalingFactor + 0.01)
			highZoomedY = int((highY + 0.9 + 1) * scalingFactor + 0.01)
			for x in range(lowZoomedX, highZoomedX + 1):
				for y in range(lowZoomedY, highZoomedY + 1):
					coordX = int((x - (lowX - 1) * scalingFactor) * 256)
					coordY = int((y - (lowY - 1) * scalingFactor) * 256)
					cropped = zoomed.crop((coordX, zoomed.size[1] - coordY - 256, coordX + 256, zoomed.size[1] - coordY))
					if not allBlack(cropped):
						outfilename = "%s/tiles/rendered/%s/%s/%s_%s_%s.png" % (version, mapId, zoom, plane, x, y)
						mkdir_p(outfilename)
						cropped.save(outfilename)
			# outfilename = "%s/tiles/rendered/%s/%s_%s_full.png" % (version, mapId, plane, zoom)
			# mkdir_p(outfilename)
			# zoomed.save(outfilename)
with open("%s/basemaps.json" % version, 'w') as f:
	json.dump(baseMaps, f)
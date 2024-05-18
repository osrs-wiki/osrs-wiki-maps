import json
import os
import os.path
import glob
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

version = "../out/mapgen/versions/2024-04-10_a"

with open(f"{version}/worldMapDefinitions.json") as f:
    defs = json.load(f)

with open("user_world_defs.json") as f:
    defs += json.load(f)

with open(f"{version}/minimapIcons.json") as f:
    icons = json.load(f)

icon_sprites = {}
for file in glob.glob(f"{version}/icons/*.png"):
    print(file)
    sprite_id = int(file.split("/")[-1][:-4])
    icon_sprites[sprite_id] = Image.open(file)

overall_x_low = 999
overall_x_high = 0
overall_y_low = 999
overall_y_high = 0
for file in glob.glob(f"{version}/tiles/base/*.png"):
    filename = file.split("/")[-1]
    filename = filename.replace(".png", "")
    plane, x, y = map(int, filename.split("_"))
    overall_y_high = max(y, overall_y_high)
    overall_y_low = min(y, overall_y_low)
    overall_x_high = max(x, overall_x_high)
    overall_x_low = min(x, overall_x_low)

defs.append(
    {
        "name": "debug",
        "mapId": -1,
        "regionList": [
            {
                "xLowerLeft": overall_x_low,
                "yUpperRight": overall_y_high,
                "yLowerRight": overall_y_low,
                "yLowerLeft": overall_y_low,
                "numberOfPlanes": 4,
                "xUpperLeft": overall_x_low,
                "xUpperRight": overall_x_high,
                "yUpperLeft": overall_y_high,
                "plane": 0,
                "xLowerRight": overall_x_high,
            }
        ],
    }
)


def mkdir_p(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def get_bounds(region_list):
    low_x, low_y, high_x, high_y = 9999, 9999, 0, 0
    planes = 0
    for region in region_list:
        if "xLowerLeft" in region:  # typeA
            low_x = min(low_x, region["xUpperLeft"])
            high_x = max(high_x, region["xUpperRight"])
            low_y = min(low_y, region["yLowerLeft"])
            high_y = max(high_y, region["yUpperLeft"])
            planes = max(planes, region["numberOfPlanes"])
        elif "newX" in region:
            low_x = min(low_x, region["newX"])
            high_x = max(high_x, region["newX"])
            low_y = min(low_y, region["newY"])
            high_y = max(high_y, region["newY"])
            planes = max(planes, region["numberOfPlanes"])
        elif "xLow" in region:
            low_x = min(low_x, region["xLow"])
            high_x = max(high_x, region["xHigh"])
            low_y = min(low_y, region["yLow"])
            high_y = max(high_y, region["yHigh"])
            planes = max(planes, region["numberOfPlanes"])
        else:
            raise ValueError(region)
    return low_x, high_x, low_y, high_y, planes


def point_inside_box(
    position, plane, low_x, high_x, low_y, high_y, chunk_low_x, chunk_high_x, chunk_low_y, chunk_high_y
):
    x = position["x"]
    y = position["y"]
    z = position["z"]
    low_x = low_x * 64 + chunk_low_x * 8
    low_y = low_y * 64 + chunk_low_y * 8
    high_x = high_x * 64 + chunk_high_x * 8 + 7
    high_y = high_y * 64 + chunk_high_y * 8 + 7
    return plane in (0, z) and low_x <= x <= high_x and low_y <= y <= high_y


def get_icons_inside_area(
    plane, low_x, high_x, low_y, high_y, chunk_lowX=0, chunk_highX=7, chunk_lowY=0, chunk_highY=7, dx=0, dy=0
):
    valid = []
    for icon in icons:
        if point_inside_box(
            icon["position"], plane, low_x, high_x, low_y, high_y, chunk_lowX, chunk_highX, chunk_lowY, chunk_highY
        ):
            pos = icon["position"]
            icon = [pos["x"] + dx, pos["y"] + dy, icon["spriteId"]]
            valid.append(icon)
    return valid


def all_black(im):
    data = np.asarray(im.convert("RGBA"))
    return np.all(data[:, :, :3] < 20)


PADDING = 64
basemaps = []
px_per_square = 4
for defn in defs:
    map_id = -1
    if "mapId" in defn:
        map_id = defn["mapId"]
    elif "fileId" in defn:
        map_id = defn["fileId"]

    low_x, high_x, low_y, high_y, planes = get_bounds(defn["regionList"])
    bounds = [[low_x * 64 - PADDING, low_y * 64 - PADDING], [(high_x + 1) * 64 + PADDING, (high_y + 1) * 64 + PADDING]]
    # bounds = [[0, 0], [12800, 12800]]

    if map_id < 1:
        center = [2496, 3328]
    elif "position" in defn:
        center = [defn["position"]["x"], defn["position"]["y"]]
    else:
        print("cent")
        center = [(low_x + high_x + 1) * 32, (low_y + high_y + 1) * 32]

    basemaps.append({"mapId": map_id, "name": defn["name"], "bounds": bounds, "center": center})
    overall_height = (high_y - low_y + 1) * px_per_square * 64
    overall_width = (high_x - low_x + 1) * px_per_square * 64

    plane_0_map = None
    for plane in range(planes):
        print(map_id, plane)
        valid_icons = []
        im = Image.new("RGB", (overall_width + 512, overall_height + 512))

        for region in defn["regionList"]:
            if "xLowerLeft" in region:
                old_low_x = region["xLowerLeft"]
                old_high_x = region["xLowerRight"]
                old_low_y = region["yLowerLeft"]
                old_high_y = region["yUpperLeft"]
                new_low_x = region["xUpperLeft"]
                new_high_x = region["xUpperRight"]
                new_low_y = region["yLowerRight"]
                new_high_y = region["yUpperRight"]
                print(
                    old_low_x == new_low_x, old_low_y == new_low_y, old_high_x == new_high_x, old_high_y == new_high_y
                )

                valid_icons.extend(
                    get_icons_inside_area(region["plane"] + plane, old_low_x, old_high_x, old_low_y, old_high_y)
                )

                for x in range(old_low_x, old_high_x + 1):
                    for y in range(old_low_y, old_high_y + 1):
                        filename = f"{version}/tiles/base/{region['plane'] + plane}_{x}_{y}.png"
                        if os.path.exists(filename):
                            square = Image.open(filename)
                            im_x = (x - low_x + new_low_x - old_low_x) * px_per_square * 64
                            im_y = (high_y - y) * px_per_square * 64
                            im.paste(square, box=(im_x + 256, im_y + 256))

            elif "chunk_oldXLow" in region:
                filename = f"{version}/tiles/base/{region['oldPlane'] + plane}_{region['oldX']}_{region['oldY']}.png"
                dx = (
                    region["newX"] * 64
                    + region["chunk_newXLow"] * 8
                    - region["oldX"] * 64
                    - region["chunk_oldXLow"] * 8
                )
                dy = (
                    region["newY"] * 64
                    + region["chunk_newYLow"] * 8
                    - region["oldY"] * 64
                    - region["chunk_oldYLow"] * 8
                )

                valid_icons.extend(
                    get_icons_inside_area(
                        region["oldPlane"] + plane,
                        region["oldX"],
                        region["oldX"],
                        region["oldY"],
                        region["oldY"],
                        region["chunk_oldXLow"],
                        region["chunk_oldXHigh"],
                        region["chunk_oldYLow"],
                        region["chunk_oldYHigh"],
                        dx,
                        dy,
                    )
                )

                if os.path.exists(filename):
                    square = Image.open(filename)
                    cropped = square.crop(
                        (
                            region["chunk_oldXLow"] * px_per_square * 8,
                            (8 - region["chunk_oldYHigh"] - 1) * px_per_square * 8,
                            (region["chunk_oldXHigh"] + 1) * px_per_square * 8,
                            (8 - region["chunk_oldYLow"]) * px_per_square * 8,
                        )
                    )
                    im_x = (region["newX"] - low_x) * px_per_square * 64 + region["chunk_newXLow"] * px_per_square * 8
                    im_y = (high_y - region["newY"]) * px_per_square * 64 + (
                        7 - region["chunk_newYHigh"]
                    ) * px_per_square * 8
                    im.paste(cropped, box=(im_x + 256, im_y + 256))

            elif "chunk_xLow" in region:
                valid_icons.extend(
                    get_icons_inside_area(
                        region["plane"] + plane,
                        region["xLow"],
                        region["xHigh"],
                        region["yLow"],
                        region["yHigh"],
                        region["chunk_xLow"],
                        region["chunk_xHigh"],
                        region["chunk_yLow"],
                        region["chunk_yHigh"],
                    )
                )

                filename = f"{version}/tiles/base/{region['plane'] + plane}_{region['xLow']}_{region['yLow']}.png"

                if os.path.exists(filename):
                    square = Image.open(filename)
                    cropped = square.crop(
                        (
                            region["chunk_xLow"] * px_per_square * 8,
                            (8 - region["chunk_yHigh"] - 1) * px_per_square * 8,
                            (region["chunk_xHigh"] + 1) * px_per_square * 8,
                            (8 - region["chunk_yLow"]) * px_per_square * 8,
                        )
                    )
                    im_x = (region["xLow"] - low_x) * px_per_square * 64 + region["chunk_xLow"] * px_per_square * 8
                    im_y = (high_y - region["yLow"]) * px_per_square * 64 + (
                        7 - region["chunk_yHigh"]
                    ) * px_per_square * 8
                    im.paste(cropped, box=(im_x + 256, im_y + 256))

            elif "xLow" in region:
                valid_icons.extend(
                    get_icons_inside_area(
                        region["plane"] + plane, region["xLow"], region["xHigh"], region["yLow"], region["yHigh"]
                    )
                )

                for x in range(region["xLow"], region["xHigh"] + 1):
                    for y in range(region["yLow"], region["yHigh"] + 1):
                        filename = f"{version}/tiles/base/{region['plane'] + plane}_{x}_{y}.png"
                        if os.path.exists(filename):
                            square = Image.open(filename)
                            im_x = (x - low_x) * px_per_square * 64
                            im_y = (high_y - y) * px_per_square * 64
                            im.paste(square, box=(im_x + 256, im_y + 256))

            else:
                raise ValueError(region)

        if plane == 0:
            data = np.asarray(im.convert("RGB")).copy()
            data[(data == (255, 0, 255)).all(axis=-1)] = (0, 0, 0)
            im = Image.fromarray(data, mode="RGB")
            if planes > 1:
                plane_0_map = im.filter(ImageFilter.GaussianBlur(radius=2))
                plane_0_map = ImageEnhance.Brightness(plane_0_map).enhance(0.7)

                # decrease contrast
                intermediate = Image.new("LA", plane0Map.size, 80).convert(plane0Map.mode)
                plane0Map = Image.blend(intermediate, plane0Map, 0.8)
                del intermediate

                plane_0_map = ImageEnhance.Color(plane_0_map).enhance(0.5)

        elif plane > 0:
            data = np.asarray(im.convert("RGBA")).copy()
            data[:, :, 3] = 255 * (data[:, :, :3] != (255, 0, 255)).all(axis=-1)
            mask = Image.fromarray(data, mode="RGBA")
            im = plane_0_map.copy()
            im.paste(mask, (0, 0), mask)

        for zoom in range(-3, 4):
            scaling_factor = 2.0**zoom / 2.0**2
            zoomed_width = int(round(scaling_factor * im.width))
            zoomed_height = int(round(scaling_factor * im.height))
            resample = Image.BILINEAR if zoom <= 1 else Image.NEAREST
            zoomed = im.resize((zoomed_width, zoomed_height), resample=resample)

            if zoom >= 0:
                for x, y, sprite_id in valid_icons:
                    sprite = icon_sprites[sprite_id]
                    width, height = sprite.size
                    im_x = int(round((x - low_x * 64) * px_per_square * scaling_factor)) - width // 2 - 2
                    im_y = int(round(((high_y + 1) * 64 - y) * px_per_square * scaling_factor)) - height // 2 - 2
                    zoomed.paste(
                        sprite,
                        (im_x + int(round(256 * scaling_factor)), int(round(im_y + 256 * scaling_factor))),
                        sprite,
                    )

            low_zoomed_x = int((low_x - 1) * scaling_factor + 0.01)
            high_zoomed_x = int((high_x + 0.9 + 1) * scaling_factor + 0.01)
            low_zoomed_y = int((low_y - 1) * scaling_factor + 0.01)
            high_zoomed_y = int((high_y + 0.9 + 1) * scaling_factor + 0.01)
            for x in range(low_zoomed_x, high_zoomed_x + 1):
                for y in range(low_zoomed_y, high_zoomed_y + 1):
                    coordX = int((x - (low_x - 1) * scaling_factor) * 256)
                    coordY = int((y - (low_y - 1) * scaling_factor) * 256)
                    cropped = zoomed.crop(
                        (coordX, zoomed.size[1] - coordY - 256, coordX + 256, zoomed.size[1] - coordY)
                    )

                    if not all_black(cropped):
                        outfilename = f"{version}/tiles/rendered/{map_id}/{zoom}/{plane}_{x}_{y}.png"
                        mkdir_p(outfilename)
                        cropped.save(outfilename)

            # outfilename = "%s/tiles/rendered/%s/%s_%s_full.png" % (version, mapId, plane, zoom)
            # mkdir_p(outfilename)
            # zoomed.save(outfilename)

with open(f"{version}/basemaps.json", "w") as f:
    json.dump(basemaps, f)

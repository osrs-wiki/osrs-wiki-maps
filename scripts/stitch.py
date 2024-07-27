import json
from PIL import Image, ImageFilter, ImageEnhance
import os.path
import glob
import numpy as np


PADDING = 64
PX_PER_TILE = 4


def debug_defn(tile_path):
    x_coords = set()
    y_coords = set()
    for file in os.listdir(tile_path):
        coords = os.path.splitext(file)[0]
        _, x, y = [int(i) for i in coords.split("_")]
        x_coords.add(x)
        y_coords.add(y)

    x_low = min(x_coords)
    y_low = min(y_coords)
    x_high = max(x_coords)
    y_high = max(y_coords)

    defn = {
        "name": "debug",
        "regionList": [
            {
                "numberOfPlanes": 4,
                "plane": 0,
                "xLow": x_low,
                "xHigh": x_high,
                "yLow": y_low,
                "yHigh": y_high,
            }
        ],
        "fileId": -1,
    }
    return defn


def load_defs(cache_defs, user_defs, base_tiles):
    with open(cache_defs) as f:
        defs = {int(d["fileId"]): d for d in json.load(f)}

    with open(user_defs) as f:
        user_defs = json.load(f)
        for d in user_defs:
            map_id = int(d["fileId"])
            if map_id in defs:  # overwrite region list
                defs[map_id]["regionList"] = d["regionList"]
            else:
                defs[map_id] = d

    defs[-1] = debug_defn(base_tiles)
    return defs


def load_icons(icons_path):
    with open(icons_path) as f:
        icons = json.load(f)

    return icons


def load_sprites(icons_dir):
    icon_sprites = {}
    for file in glob.glob(f"{icons_dir}/*.png"):
        sprite_id = int(file.split("/")[-1][:-4])
        icon_sprites[sprite_id] = Image.open(file)

    return icon_sprites


def load_basemap(map_id, map_name, low_x, high_x, low_y, high_y, defn):
    bounds = [
        [low_x * 64 - PADDING, low_y * 64 - PADDING],
        [(high_x + 1) * 64 + PADDING, (high_y + 1) * 64 + PADDING],
    ]

    if map_id < 1:
        center = [2496, 3328]
    elif "position" in defn:
        center = [defn["position"]["x"], defn["position"]["y"]]
    else:
        center = [(low_x + high_x + 1) * 32, (low_y + high_y + 1) * 32]

    return {"mapId": map_id, "name": map_name, "bounds": bounds, "center": center}


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
    return ((plane == 0) or (plane == z)) and x >= low_x and x <= high_x and y >= low_y and y <= high_y


def get_icons_inside_area(
    icons,
    plane,
    low_x,
    high_x,
    low_y,
    high_y,
    chunk_low_x=0,
    chunk_high_x=7,
    chunk_low_y=0,
    chunk_high_y=7,
    dx=0,
    dy=0,
):
    valid = []
    for icon in icons:
        if point_inside_box(
            icon["position"], plane, low_x, high_x, low_y, high_y, chunk_low_x, chunk_high_x, chunk_low_y, chunk_high_y
        ):
            pos = icon["position"]
            icon = [pos["x"] + dx, pos["y"] + dy, icon["spriteId"]]
            valid.append(icon)
    return valid


def make_plane_0_map(image):
    plane_0_map = image.filter(ImageFilter.GaussianBlur(radius=2))
    plane_0_map = ImageEnhance.Brightness(plane_0_map).enhance(0.7)

    # decrease contrast
    intermediate = Image.new("LA", plane_0_map.size, 80).convert(plane_0_map.mode)
    plane_0_map = Image.blend(intermediate, plane_0_map, 0.8)
    del intermediate

    plane_0_map = ImageEnhance.Color(plane_0_map).enhance(0.5)
    return plane_0_map


def all_black(im):
    data = np.asarray(im.convert("RGBA"))
    return np.all(data[:, :, :3]) < 7


def render_map(map_id, defn, icons, icon_sprites, base_tiles_dir, out_tiles_dir):
    map_name = defn["name"]
    low_x, high_x, low_y, high_y, planes = get_bounds(defn["regionList"])

    basemap = load_basemap(map_id, map_name, low_x, high_x, low_y, high_y, defn)

    map_height = (high_y - low_y + 1) * PX_PER_TILE * 64
    map_width = (high_x - low_x + 1) * PX_PER_TILE * 64

    plane_0_map = None
    for plane in range(planes):
        print(f"{map_id=}, {plane=}")
        valid_icons = []
        plane_image = Image.new("RGB", (map_width + 512, map_height + 512))

        for region in defn["regionList"]:
            if "xLowerLeft" in region:
                old_plane = region["plane"] + plane

                old_low_x = region["xLowerLeft"]
                old_high_x = region["xLowerRight"]
                old_low_y = region["yLowerLeft"]
                old_high_y = region["yUpperLeft"]
                new_low_x = region["xUpperLeft"]
                new_high_x = region["xUpperRight"]  # why aren't these used?
                new_low_y = region["yLowerRight"]  # ^
                new_high_y = region["yUpperRight"]  # ^
                print(
                    old_low_x == new_low_x,
                    old_low_y == new_low_y,
                    old_high_x == new_high_x,
                    old_high_y == new_high_y,
                )

                valid_icons.extend(
                    get_icons_inside_area(icons, old_plane, old_low_x, old_high_x, old_low_y, old_high_y)
                )

                for x in range(old_low_x, old_high_x + 1):
                    for y in range(old_low_y, old_high_y + 1):
                        in_path = os.path.join(base_tiles_dir, f"{old_plane}_{x}_{y}.png")
                        if os.path.exists(in_path):
                            mapsquare_image = Image.open(in_path)
                            mapsquare_x = (x - low_x + new_low_x - old_low_x) * PX_PER_TILE * 64
                            mapsquare_y = (high_y - y) * PX_PER_TILE * 64
                            plane_image.paste(mapsquare_image, box=(mapsquare_x + 256, mapsquare_y + 256))

            elif "chunk_oldXLow" in region:
                old_plane = region["oldPlane"] + plane

                in_path = os.path.join(base_tiles_dir, f"{old_plane}_{region['oldX']}_{region['oldY']}.png")
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
                        icons,
                        old_plane,
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

                if os.path.exists(in_path):
                    mapsquare_image = Image.open(in_path)
                    cropped = mapsquare_image.crop(
                        (
                            region["chunk_oldXLow"] * PX_PER_TILE * 8,
                            (8 - region["chunk_oldYHigh"] - 1) * PX_PER_TILE * 8,
                            (region["chunk_oldXHigh"] + 1) * PX_PER_TILE * 8,
                            (8 - region["chunk_oldYLow"]) * PX_PER_TILE * 8,
                        )
                    )
                    mapsquare_x = (region["newX"] - low_x) * PX_PER_TILE * 64 + region[
                        "chunk_newXLow"
                    ] * PX_PER_TILE * 8
                    mapsquare_y = (high_y - region["newY"]) * PX_PER_TILE * 64 + (
                        7 - region["chunk_newYHigh"]
                    ) * PX_PER_TILE * 8
                    plane_image.paste(cropped, box=(mapsquare_x + 256, mapsquare_y + 256))

            elif "chunk_xLow" in region:
                old_plane = region["plane"] + plane

                valid_icons.extend(
                    get_icons_inside_area(
                        icons,
                        old_plane,
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
                in_path = os.path.join(base_tiles_dir, f"{old_plane}_{region['xLow']}_{region['yLow']}.png")

                if os.path.exists(in_path):
                    mapsquare_image = Image.open(in_path)
                    cropped = mapsquare_image.crop(
                        (
                            region["chunk_xLow"] * PX_PER_TILE * 8,
                            (8 - region["chunk_yHigh"] - 1) * PX_PER_TILE * 8,
                            (region["chunk_xHigh"] + 1) * PX_PER_TILE * 8,
                            (8 - region["chunk_yLow"]) * PX_PER_TILE * 8,
                        )
                    )
                    mapsquare_x = (region["xLow"] - low_x) * PX_PER_TILE * 64 + region["chunk_xLow"] * PX_PER_TILE * 8
                    mapsquare_y = (high_y - region["yLow"]) * PX_PER_TILE * 64 + (
                        7 - region["chunk_yHigh"]
                    ) * PX_PER_TILE * 8
                    plane_image.paste(cropped, box=(mapsquare_x + 256, mapsquare_y + 256))

            elif "xLow" in region:
                old_plane = region["plane"] + plane

                valid_icons.extend(
                    get_icons_inside_area(
                        icons,
                        old_plane,
                        region["xLow"],
                        region["xHigh"],
                        region["yLow"],
                        region["yHigh"],
                    )
                )

                for x in range(region["xLow"], region["xHigh"] + 1):
                    for y in range(region["yLow"], region["yHigh"] + 1):
                        in_path = os.path.join(base_tiles_dir, f"{old_plane}_{x}_{y}.png")
                        if os.path.exists(in_path):
                            mapsquare_image = Image.open(in_path)
                            mapsquare_x = (x - low_x) * PX_PER_TILE * 64
                            mapsquare_y = (high_y - y) * PX_PER_TILE * 64
                            plane_image.paste(mapsquare_image, box=(mapsquare_x + 256, mapsquare_y + 256))

            else:
                raise ValueError(region)

        if plane == 0:
            data = np.asarray(plane_image.convert("RGB")).copy()
            data[(data == (255, 0, 255)).all(axis=-1)] = (0, 0, 0)
            plane_image = Image.fromarray(data, mode="RGB")
            if planes > 1:
                plane_0_map = make_plane_0_map(plane_image)

        elif plane > 0:
            data = np.asarray(plane_image.convert("RGBA")).copy()
            data[:, :, 3] = 255 * (data[:, :, :3] != (255, 0, 255)).all(axis=-1)
            mask = Image.fromarray(data, mode="RGBA")
            plane_image = plane_0_map.copy()
            plane_image.paste(mask, (0, 0), mask)

        for zoom in range(-3, 4):
            scaling_factor = 2.0**zoom / 2.0**2
            zoomed_width = int(round(scaling_factor * plane_image.width))
            zoomed_height = int(round(scaling_factor * plane_image.height))
            resample = Image.BILINEAR if zoom <= 1 else Image.NEAREST
            zoomed = plane_image.resize((zoomed_width, zoomed_height), resample=resample)

            if zoom >= 0:
                for x, y, sprite_id in valid_icons:
                    sprite = icon_sprites[sprite_id]
                    width, height = sprite.size
                    mapsquare_x = int(round((x - low_x * 64) * PX_PER_TILE * scaling_factor)) - width // 2 - 2
                    mapsquare_y = int(round(((high_y + 1) * 64 - y) * PX_PER_TILE * scaling_factor)) - height // 2 - 2
                    zoomed.paste(
                        sprite,
                        (
                            mapsquare_x + int(round(256 * scaling_factor)),
                            int(round(mapsquare_y + 256 * scaling_factor)),
                        ),
                        sprite,
                    )

            low_zoomed_x = int((low_x - 1) * scaling_factor + 0.01)
            high_zoomed_x = int((high_x + 0.9 + 1) * scaling_factor + 0.01)
            low_zoomed_y = int((low_y - 1) * scaling_factor + 0.01)
            high_zoomed_y = int((high_y + 0.9 + 1) * scaling_factor + 0.01)
            for x in range(low_zoomed_x, high_zoomed_x + 1):
                for y in range(low_zoomed_y, high_zoomed_y + 1):
                    coord_x = int((x - (low_x - 1) * scaling_factor) * 256)
                    coord_y = int((y - (low_y - 1) * scaling_factor) * 256)
                    cropped = zoomed.crop(
                        (coord_x, zoomed.size[1] - coord_y - 256, coord_x + 256, zoomed.size[1] - coord_y)
                    )

                    if not all_black(cropped):
                        out_path = os.path.join(out_tiles_dir, f"{map_id}/{zoom}/{plane}_{x}_{y}.png")
                        mkdir_p(out_path)
                        cropped.save(out_path)

    return basemap


def main(version_dir):
    base_tiles_dir = os.path.join(version_dir, "tiles", "base")
    out_tiles_dir = os.path.join(version_dir, "tiles", "rendered")
    icons_dir = os.path.join(version_dir, "icons")

    cache_defs_path = os.path.join(version_dir, "worldMapDefinitions.json")
    extra_defs_path = "user_world_defs.json"
    icons_path = os.path.join(version_dir, "minimapIcons.json")
    basemaps_path = os.path.join(version_dir, "basemaps.json")

    defs = load_defs(cache_defs_path, extra_defs_path, base_tiles_dir)
    icons = load_icons(icons_path)
    icon_sprites = load_sprites(icons_dir)

    basemaps = []
    for map_id, defn in defs.items():
        basemap = render_map(map_id, defn, icons, icon_sprites, base_tiles_dir, out_tiles_dir)
        basemaps.append(basemap)

    with open(basemaps_path, "w") as f:
        json.dump(basemaps, f)


if __name__ == "__main__":
    main("../out/mapgen/versions/2024-07-24_a")

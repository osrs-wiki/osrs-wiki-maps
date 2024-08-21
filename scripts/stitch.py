import json
import os.path
import glob
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np


PADDING = 64
PX_PER_TILE = 4


def debug_defn(tile_path):
    """
    Create a fake worldMapDefinition for debug (-1) map based on base image names RL
    """
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
    """
    Load worldMapDefinitions + user-defined defns + debug defn
    """
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
    """
    Get list of minimapIcons definitions (x, y, z, and sprite id)
    """
    with open(icons_path) as f:
        icons = json.load(f)

    return icons


def load_sprites(icons_dir):
    """
    Get dict of {sprite id: sprite image}
    """
    icon_sprites = {}
    for file in glob.glob(f"{icons_dir}/*.png"):
        sprite_id = int(file.split(os.sep)[-1][:-4])
        icon_sprites[sprite_id] = Image.open(file)

    return icon_sprites


def load_basemap(defn):
    """
    Get basemap dict for this map id, for telling wiki the bounds + center + name of this map
    """
    map_name = defn["name"]
    map_id = defn["fileId"]
    map_low_x, map_high_x, map_low_y, map_high_y, _ = get_bounds(defn["regionList"])

    bounds = [
        [map_low_x * 64 - PADDING, map_low_y * 64 - PADDING],
        [(map_high_x + 1) * 64 + PADDING, (map_high_y + 1) * 64 + PADDING],
    ]

    if map_id < 1:
        center = [2496, 3328]
    elif "position" in defn:
        center = [defn["position"]["x"], defn["position"]["y"]]
    else:
        center = [(map_low_x + map_high_x + 1) * 32, (map_low_y + map_high_y + 1) * 32]

    return {"mapId": map_id, "name": map_name, "bounds": bounds, "center": center}


def mkdir_p(path):
    """
    Create directory (before writing file into it, in case of permissions issues)
    """
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def get_bounds(region_list):
    """
    Get bounding box (cube?) for this map id
    """
    low_x, low_y, high_x, high_y = 9999, 9999, 0, 0
    planes = 0
    for region in region_list:
        if "xLowerLeft" in region:
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
    """
    Check if map icon is inside given area
    """
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
    """
    Get all map icons inside an area's old position (where it appears on debug map)
    """
    valid = []
    for icon in icons:
        if point_inside_box(
            icon["position"], plane, low_x, high_x, low_y, high_y, chunk_low_x, chunk_high_x, chunk_low_y, chunk_high_y
        ):
            pos = icon["position"]
            icon = [pos["x"] + dx, pos["y"] + dy, icon["spriteId"]]
            valid.append(icon)
    return valid


def map_is_selected(select_regions, map_low_x, map_high_x, map_low_y, map_high_y):
    if not select_regions:
        return True

    for region_x, region_y in select_regions:
        if (map_low_x <= region_x <= map_high_x) and (map_low_y <= region_y <= map_high_y):
            return True

    return False


def image_is_selected(select_regions, x, y, scaling_factor):
    if not select_regions:
        return True

    for region_x, region_y in select_regions:
        # don't only want to render the selected region, but also adjacent regions
        # in case icons cross over or plane 0 blur at the boundary has changed
        left = x / scaling_factor - 1  # adjacent images have lower left coord 1 *map square* to the east
        right = (x + 1) / scaling_factor  # adjacent images have lower left coord 1 *image* to the west
        bottom = y / scaling_factor - 1
        top = (y + 1) / scaling_factor
        if (left <= region_x <= right) and  (bottom <= region_y <= top):
            return True

    return False


def make_plane_0_map(image):
    """
    Get blurry + grey-ish plane 0 for rendering beneath upper planes
    """
    plane_0_map = image.filter(ImageFilter.GaussianBlur(radius=2))
    plane_0_map = ImageEnhance.Brightness(plane_0_map).enhance(0.7)

    # decrease contrast
    intermediate = Image.new("LA", plane_0_map.size, 80).convert(plane_0_map.mode)
    plane_0_map = Image.blend(intermediate, plane_0_map, 0.8)
    del intermediate

    plane_0_map = ImageEnhance.Color(plane_0_map).enhance(0.5)
    return plane_0_map


def all_black(im):
    """
    Check if image is completely black; note jagex uses RGB(2,6,6) sometimes instead of (0,0,0)
    """
    data = np.asarray(im.convert("RGBA"))
    return np.all(data[:, :, :3] < 7)


def render_region(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y):
    """
    Determine WorldMapType of a region definition and render accordingly
    """
    if "xLowerLeft" in region:
        return render_type_1(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y)

    elif "chunk_oldXLow" in region:
        return render_type_3(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y)

    elif "chunk_xLow" in region:
        return render_type_0(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y)

    elif "xLow" in region:
        return render_type_2(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y)

    else:
        raise ValueError(region)


def render_type_0(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y):
    """
    Render WorldMapType0 (selected squares + zones rendered in-place)
    """
    old_plane = region["plane"] + plane

    area_icons = get_icons_inside_area(
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
        mapsquare_x = (region["xLow"] - map_low_x) * PX_PER_TILE * 64 + region["chunk_xLow"] * PX_PER_TILE * 8
        mapsquare_y = (map_high_y - region["yLow"]) * PX_PER_TILE * 64 + (7 - region["chunk_yHigh"]) * PX_PER_TILE * 8
        plane_image.paste(cropped, box=(mapsquare_x + 256, mapsquare_y + 256))

    return plane_image, area_icons


def render_type_1(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y):
    """
    Render WorldMapType1 area (selected squares rendered in-place)
    """
    old_plane = region["plane"] + plane

    old_low_x = region["xLowerLeft"]
    old_high_x = region["xLowerRight"]
    old_low_y = region["yLowerLeft"]
    old_high_y = region["yUpperLeft"]
    new_low_x = region["xUpperLeft"]
    # new_high_x = region["xUpperRight"]  # why aren't these used?
    # new_low_y = region["yLowerRight"]  # ^
    # new_high_y = region["yUpperRight"]  # ^
    # print(
    #     old_low_x == new_low_x,
    #     old_low_y == new_low_y,
    #     old_high_x == new_high_x,
    #     old_high_y == new_high_y,
    # )

    area_icons = get_icons_inside_area(icons, old_plane, old_low_x, old_high_x, old_low_y, old_high_y)

    for x in range(old_low_x, old_high_x + 1):
        for y in range(old_low_y, old_high_y + 1):
            in_path = os.path.join(base_tiles_dir, f"{old_plane}_{x}_{y}.png")
            if os.path.exists(in_path):
                mapsquare_image = Image.open(in_path)
                mapsquare_x = (x - map_low_x + new_low_x - old_low_x) * PX_PER_TILE * 64
                mapsquare_y = (map_high_y - y) * PX_PER_TILE * 64
                plane_image.paste(mapsquare_image, box=(mapsquare_x + 256, mapsquare_y + 256))

    return plane_image, area_icons


def render_type_2(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y):
    """
    Render WorldMapType2 area (selected squares rendered in-place, equivalent to type 1?)
    """
    old_plane = region["plane"] + plane

    area_icons = get_icons_inside_area(
        icons,
        old_plane,
        region["xLow"],
        region["xHigh"],
        region["yLow"],
        region["yHigh"],
    )

    for x in range(region["xLow"], region["xHigh"] + 1):
        for y in range(region["yLow"], region["yHigh"] + 1):
            in_path = os.path.join(base_tiles_dir, f"{old_plane}_{x}_{y}.png")
            if os.path.exists(in_path):
                mapsquare_image = Image.open(in_path)
                mapsquare_x = (x - map_low_x) * PX_PER_TILE * 64
                mapsquare_y = (map_high_y - y) * PX_PER_TILE * 64
                plane_image.paste(mapsquare_image, box=(mapsquare_x + 256, mapsquare_y + 256))

    return plane_image, area_icons


def render_type_3(plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y):
    """
    Render WorldMapType3 area (selected square or zone-subset of a square to translate)
    """
    old_plane = region["oldPlane"] + plane

    in_path = os.path.join(base_tiles_dir, f"{old_plane}_{region['oldX']}_{region['oldY']}.png")
    dx = region["newX"] * 64 + region["chunk_newXLow"] * 8 - region["oldX"] * 64 - region["chunk_oldXLow"] * 8
    dy = region["newY"] * 64 + region["chunk_newYLow"] * 8 - region["oldY"] * 64 - region["chunk_oldYLow"] * 8

    area_icons = get_icons_inside_area(
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
        mapsquare_x = (region["newX"] - map_low_x) * PX_PER_TILE * 64 + region["chunk_newXLow"] * PX_PER_TILE * 8
        mapsquare_y = (map_high_y - region["newY"]) * PX_PER_TILE * 64 + (
            7 - region["chunk_newYHigh"]
        ) * PX_PER_TILE * 8
        plane_image.paste(cropped, box=(mapsquare_x + 256, mapsquare_y + 256))

    return plane_image, area_icons


def render_map(map_id, defn, icons, icon_sprites, base_tiles_dir, out_tiles_dir, select_regions):
    """
    render and save images for this map id to "out/mapgen/versions/#/output/tiles/rendered"
    """
    map_low_x, map_high_x, map_low_y, map_high_y, planes = get_bounds(defn["regionList"])

    # check if this map needs to be rendered
    if not map_is_selected(select_regions, map_low_x, map_high_x, map_low_y, map_high_y):
        return

    map_height = (map_high_y - map_low_y + 1) * PX_PER_TILE * 64
    map_width = (map_high_x - map_low_x + 1) * PX_PER_TILE * 64

    plane_0_map = None
    for plane in range(planes):
        print(f"{map_id=}, {plane=}")
        valid_icons = []
        plane_image = Image.new("RGB", (map_width + 512, map_height + 512))

        for region in defn["regionList"]:
            plane_image, area_icons = render_region(
                plane, region, icons, plane_image, base_tiles_dir, map_low_x, map_high_y
            )
            valid_icons.extend(area_icons)

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
            plane_image = plane_0_map.copy() # type: ignore
            plane_image.paste(mask, (0, 0), mask)

        for zoom in range(-3, 4):
            scaling_factor = 2.0**zoom / 2.0**2
            zoomed_width = int(round(scaling_factor * plane_image.width))
            zoomed_height = int(round(scaling_factor * plane_image.height))
            resample = Image.BILINEAR if zoom <= 1 else Image.NEAREST # type: ignore # pylint:disable=E1101
            zoomed = plane_image.resize((zoomed_width, zoomed_height), resample=resample)

            if zoom >= 0:
                for x, y, sprite_id in valid_icons:
                    sprite = icon_sprites[sprite_id]
                    width, height = sprite.size
                    mapsquare_x = int(round((x - map_low_x * 64) * PX_PER_TILE * scaling_factor)) - width // 2 - 2
                    mapsquare_y = (
                        int(round(((map_high_y + 1) * 64 - y) * PX_PER_TILE * scaling_factor)) - height // 2 - 2
                    )
                    zoomed.paste(
                        sprite,
                        (
                            mapsquare_x + int(round(256 * scaling_factor)),
                            int(round(mapsquare_y + 256 * scaling_factor)),
                        ),
                        sprite,
                    )

            low_zoomed_x = int((map_low_x - 1) * scaling_factor + 0.01)
            high_zoomed_x = int((map_high_x + 0.9 + 1) * scaling_factor + 0.01)
            low_zoomed_y = int((map_low_y - 1) * scaling_factor + 0.01)
            high_zoomed_y = int((map_high_y + 0.9 + 1) * scaling_factor + 0.01)
            for x in range(low_zoomed_x, high_zoomed_x + 1):
                for y in range(low_zoomed_y, high_zoomed_y + 1):
                    if not image_is_selected(select_regions, x, y, scaling_factor):
                        continue

                    coord_x = int((x - (map_low_x - 1) * scaling_factor) * 256)
                    coord_y = int((y - (map_low_y - 1) * scaling_factor) * 256)
                    cropped = zoomed.crop(
                        (coord_x, zoomed.size[1] - coord_y - 256, coord_x + 256, zoomed.size[1] - coord_y)
                    )

                    if not all_black(cropped):
                        out_path = os.path.join(out_tiles_dir, f"{map_id}/{zoom}/{plane}_{x}_{y}.png")
                        mkdir_p(out_path)
                        cropped.save(out_path)


def main(select_maps=()):
    version_txt = "./data/versions/version.txt"

    select_regions = []
    with open(version_txt, "rt") as file:
        for i, line in enumerate(file.read().splitlines()):
            if i == 0:
                version = line
            elif line:  # ignore blank lines
                region_id = int(line)
                region_x = region_id // 256
                region_y = region_id - region_x * 256
                select_regions.append((region_x, region_y))

    version_dir = f"./out/mapgen/versions/{version}"

    base_tiles_dir = os.path.join(version_dir, "tiles", "base")
    out_tiles_dir = os.path.join(version_dir, "output", "tiles", "rendered")
    icons_dir = os.path.join(version_dir, "output", "icons")

    cache_defs_path = os.path.join(version_dir, "worldMapDefinitions.json")
    extra_defs_path = os.path.join("scripts", "user_world_defs.json")
    icons_path = os.path.join(version_dir, "minimapIcons.json")
    basemaps_path = os.path.join(version_dir, "output", "basemaps.json")

    defs = load_defs(cache_defs_path, extra_defs_path, base_tiles_dir)
    icons = load_icons(icons_path)
    icon_sprites = load_sprites(icons_dir)

    basemaps = []
    for map_id, defn in defs.items():
        if select_maps and map_id not in select_maps:
            continue
        basemap = load_basemap(defn)
        basemaps.append(basemap)
        render_map(map_id, defn, icons, icon_sprites, base_tiles_dir, out_tiles_dir, select_regions)

    with open(basemaps_path, "w") as f:
        json.dump(basemaps, f)


if __name__ == "__main__":
    main()

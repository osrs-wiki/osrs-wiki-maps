from os import makedirs
import os.path
from io import BytesIO
import json
import datetime as dt
from zipfile import ZipFile
from string import ascii_lowercase
from dateutil.parser import isoparse
import requests


CACHE_URL_BASE = "https://archive.openrs2.org"
UTC = dt.timezone.utc


def make_output_folder(date_str: str, version_dir: str) -> tuple[str, str]:
    version_name = date_str
    out_folder = os.path.join(version_dir, version_name)
    tries = 0
    while os.path.exists(out_folder):
        version_name = date_str + f"_{ascii_lowercase[tries]}"
        out_folder = os.path.join(version_dir, version_name)
        tries += 1
    makedirs(out_folder)
    return version_name, out_folder


def get_cache_info() -> tuple[int, str]:
    cache_list = requests.get(CACHE_URL_BASE + "/caches.json", timeout=15).json()
    latest = dt.datetime(1970, 1, 1, tzinfo=UTC)
    cache_id = -1
    for cache in cache_list:
        if cache["scope"] != "runescape" or cache["game"] != "oldschool" or cache["environment"] != "live":
            continue

        timestamp = cache["timestamp"]
        if not timestamp:
            continue

        date = isoparse(timestamp)
        if date > latest:
            latest = date
            cache_id = cache["id"]

    date_str = latest.strftime("%Y-%m-%d")
    # print(f"Found cache {cache_id} from {date_str}\n")
    return cache_id, date_str


def download_xteas(cache_id, out_folder):
    keys_path = os.path.join(out_folder, "xteas.json")

    # print("Downloading xteas...")
    # start = dt.datetime.now()
    response = requests.get(CACHE_URL_BASE + f"/caches/runescape/{cache_id}/keys.json", timeout=30)
    # end = dt.datetime.now()
    # print(f"{int((end-start).total_seconds())}s elapsed.\n")

    key_list = []
    for xtea in response.json():
        new_key = {}
        for key, val in xtea.items():
            if key == "mapsquare":
                new_key["region"] = val  # runelite expects "region" not "mapsquare"
            elif key == "key":
                new_key["keys"] = val  # runelite expects "keys" not "key"

        key_list.append(new_key)

    with open(keys_path, "w", encoding="utf-8") as file:
        json.dump(key_list, file)


def download_cache(cache_id, out_folder):
    # print("Downloading cache...")
    # start = dt.datetime.now()
    raw = requests.get(CACHE_URL_BASE + f"/caches/runescape/{cache_id}/disk.zip", timeout=60).content
    # end = dt.datetime.now()
    # print(f"{int((end-start).total_seconds())}s elapsed.\n")

    z = ZipFile(BytesIO(raw))
    z.extractall(out_folder)


def write_version_txt(version_name, cache_dir):
    txt_path = os.path.join(cache_dir, "version.txt")
    if os.path.exists(txt_path):
        os.remove(txt_path)

    with open(txt_path, "wt") as file:
        file.write(version_name)


def download():
    cache_id, date_str = get_cache_info()
    cache_dir = "./data/versions"
    version_name, out_folder = make_output_folder(date_str, cache_dir)

    download_xteas(cache_id, out_folder)
    download_cache(cache_id, out_folder)
    write_version_txt(version_name, cache_dir)

    return version_name


if __name__ == "__main__":
    version = download()
    print(version)

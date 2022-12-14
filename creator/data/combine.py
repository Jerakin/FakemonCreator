from pathlib import Path
from zipfile import ZipFile
import zipfile
import json
import io
import os

FOLDER = Path(r"C:\Users\Jerakin\Downloads\Fakemon")
EXPORT = Path(r"C:\Users\Jerakin\Downloads\Fakemon\sendatsu.zip")


def _generate_empty():
    # Need to open the mem file or it will raise BadZip Exception
    mem_zip = io.BytesIO()

    with ZipFile(mem_zip, mode="w") as zf:
        pass

    return mem_zip


def combine_json(target, other):
    z_other = ZipFile(other, "r")
    with z_other.open("data.json") as fp:
        new_json = json.load(fp)

    try:
        z_target = ZipFile(target, "r")
    except zipfile.BadZipFile:
        return new_json

    if "data.json" not in z_target.filelist:
        return new_json

    with z_target.open("data.json") as fp:
        target_json = json.load(fp)

    for file_name, file_data in new_json.items():
        for entry_name, data in file_data.items():
            target_json[file_name][entry_name] = data
    z_target.close()
    z_other.close()
    return target_json


def combine_zip(target, other):
    z_other = ZipFile(other, "r")
    z_export = ZipFile(target, "w")
    new_json = combine_json(target, other)

    for name in z_other.namelist():
        if name.endswith(".json"):
            continue
        if name in z_export.namelist():
            continue
        z_export.writestr(name,  z_other.open(name).read())
    z_export.writestr('data.json', json.dumps(new_json))

    z_other.close()
    z_export.close()


def combine_json2(target_json, other):
    z_other = ZipFile(other, "r")
    with z_other.open("data.json") as fp:
        new_json = json.load(fp)

    for file_name, file_data in new_json.items():
        if file_name not in target_json:
            target_json[file_name] = {}
        for entry_name, data in file_data.items():
            target_json[file_name][entry_name] = data
    z_other.close()


if __name__ == '__main__':
    folder_list = list(FOLDER.iterdir())
    # if EXPORT.exists():
    #     os.remove(EXPORT)

    # for file_path in folder_list:
    #     if file_path.suffix != ".fkmn":
    #         continue
    #     combine_zip(EXPORT, file_path)

    data_json = {}
    for file_path in folder_list:
        if file_path.suffix != ".fkmn":
            continue
        combine_json2(data_json, file_path)

    print(data_json)
    with ZipFile(folder_list[0], 'a') as z1:
        for fname in folder_list[1:]:
            try:
                zf = ZipFile(fname, 'r')
            except PermissionError:
                continue
            for n in zf.namelist():
                if n in z1.filelist:
                    continue
                z1.writestr(n, zf.open(n).read())

    print(folder_list[0])

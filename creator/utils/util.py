import json
from pathlib import Path
import struct
import imghdr
import requests
import jsonschema


class SimpleList:
    # To be able to use the  list_view.ListView interface
    def __init__(self, _list):
        self.list = _list


class JsonToList:
    def __init__(self, file_path):
        self.list = [""]
        self.load(file_path)

    def load(self, file_path):
        extra_path = Path(file_path)
        with extra_path.open(encoding="utf-8") as f:
            data = json.load(f)

            for entry, _ in data.items():
                self.list.append(entry)

    def extend(self, file_dict):
        for entry, _ in file_dict.items():
            self.list.append(entry)


def _image_data(path):
    with open(path, 'rb') as f:
        data = f.read(25)
    return data


def get_image_size(path):
    if is_png(path):
        data = _image_data(path)
        w, h = struct.unpack('>LL', data[16:24])
        width = int(w)
        height = int(h)
    else:
        raise Exception('not a png image')
    return width, height


def is_png(path):
    return imghdr.what(str(path)) == "png"


def get_package_index():
    r = requests.get("https://raw.githubusercontent.com/Jerakin/FakemonPackages/master/index.json")
    if r.status_code in [200, 304]:
        return json.loads(r.content)
    return None


def validate(_data, schema_url):
    try:
        with open(Path(schema_url)) as f:
            schema = json.load(f)
        jsonschema.validate(_data, schema)
    except jsonschema.ValidationError as e:
        return e.schema["error"]

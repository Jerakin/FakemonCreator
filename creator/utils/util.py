import json
from pathlib import Path
import struct
import imghdr
import requests
import jsonschema
import os
import getpass
from datetime import datetime
import traceback
from io import StringIO
import logging as log
import tempfile
import shutil

from creator import __version__ as version


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
                if entry not in ["Error", "MissingNo", ""]:
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
    try:
        r = requests.get("https://raw.githubusercontent.com/Jerakin/FakemonPackages/master/index.json")
        if r.status_code in [200, 304]:
            return json.loads(r.content)
    except:
        return None


def validate(_data, schema_url):
    try:
        with open(Path(schema_url)) as f:
            schema = json.load(f)
        jsonschema.validate(_data, schema)
    except jsonschema.ValidationError as e:
        return e.schema["error"]


def get_recovery_file_name():
    username = getpass.getuser()
    now = datetime.now()
    file_name = username + "." + now.strftime("%d%m%Y.%H%M") + ".fkmn"
    if os.name == "nt":
        base_path = Path(os.getenv("LOCALAPPDATA")) / "Temp"
    elif os.name == "posix":
        base_path = Path().home() / "Documents" / "tmp"
    else:
        return None
    if not base_path.exists():
        base_path.mkdir()
    return base_path / file_name


def log_exception(extype, value, tb):
    tb_io = StringIO()
    traceback.print_tb(tb, file=tb_io)
    log.critical(
        'Global error:\n'
        'Launcher version: {version}\n'
        'Type: {extype}\n'
        'Value: {value}\n'
        'Traceback:\n{traceback}'
        .format(version=version, extype=str(extype), value=str(value), traceback=tb_io.getvalue())
    )


def tempdir():
    p = Path(tempfile.gettempdir()) / "FakemonCreator"
    if not p.exists():
        p.mkdir()
    return p


def random_word():
    url = "https://random-word-api.herokuapp.com/word?number=1"
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.content.decode())[0]
    now = datetime.now()
    return "{}{}{}".format(now.hour, now.minute, now.second)


def copy_image_to_temp_dir(image, new_name):
    dst = tempdir() / new_name
    shutil.copy(image, dst)
    return dst

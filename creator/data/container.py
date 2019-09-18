import io
import sys
import json
import zipfile
from pathlib import Path
import logging as log
import datetime
from creator.utils import validate

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class Container:
    def __init__(self):
        self.__DATA = None
        self.path = None
        self.cleaned = False

    @property
    def is_empty(self):
        if self.__DATA:
            return self.__DATA.getbuffer().nbytes < 30
        return True

    @staticmethod
    def _generate_empty():
        # Need to open the mem file or it will raise BadZip Exception
        mem_zip = io.BytesIO()

        with zipfile.ZipFile(mem_zip, mode="w") as zf:
            pass

        return mem_zip

    def validate(self):
        errors = list()
        errors.extend(validate.clean_container(self))
        data = self.data()
        errors.extend(validate.validate(root / "res/schema/pokemon.json", data["pokemon.json"]))
        errors.extend(validate.validate(root / "res/schema/pokedex_extra.json", data["pokedex_extra.json"]))
        errors.extend(validate.validate(root / "res/schema/moves.json", data["moves.json"]))
        errors.extend(validate.validate(root / "res/schema/evolve.json", data["evolve.json"]))
        errors.extend(validate.validate_package_name(self))

        return errors

    def new(self, path):
        self.path = Path(path)
        self.__DATA = self._generate_empty()

    def load(self, path):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError

        with self.path.open("rb") as f:
            self.__DATA = io.BytesIO(f.read())

    def save(self):
        if not self.__DATA or not self.path:
            return True
        try:
            with open(self.path, "wb") as f:
                f.write(self.__DATA.getvalue())
                return True
        except PermissionError:
            return False

    def add(self, path, data=None):
        log.info("Adding file")
        filename = path
        if isinstance(path, Path):
            filename = path.name

        if filename in [x.filename for x in zipfile.ZipFile(self.__DATA).filelist]:
            log.info("  Removed file {} from zip".format(filename))
            self.remove(filename)
        if not data:
            with zipfile.ZipFile(self.__DATA, "a") as f:
                log.info("  Writing file {} to zip".format(path))
                f.write(str(path), path.name)
        else:
            with zipfile.ZipFile(self.__DATA, "a") as f:
                log.info("  Writing json {} to zip".format(path))
                f.writestr(str(path), json.dumps(data, ensure_ascii=False))

    def remove(self, filename):
        log.info("Removing file")
        __TEMP = io.BytesIO()
        zin = zipfile.ZipFile(self.__DATA)
        zout = zipfile.ZipFile(__TEMP, "a")
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename != filename:
                log.info("  Keeping {}".format(item.filename))
                zout.writestr(item, buffer)
            else:
                log.info("  Skipped adding {}".format(item.filename))
        self.__DATA = __TEMP

    def clean_duplicates(self):
        _duplicate_found = False
        log.info("Cleaning duplicates from container")
        zin = zipfile.ZipFile(self.__DATA)
        __TEMP = io.BytesIO()
        zout = zipfile.ZipFile(__TEMP, "a")

        file_index = {}

        for item in zin.infolist():
            if item.filename not in file_index:
                file_index[item.filename] = {"date": datetime.datetime(*item.date_time), "count": 1}
            file_index[item.filename]["date"] = max(datetime.datetime(*item.date_time), file_index[item.filename]["date"])
            file_index[item.filename]["count"] += 1

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if file_index[item.filename]["count"] == 1 or file_index[item.filename]["date"] == datetime.datetime(*item.date_time):
                log.info("  Keeping {}".format(item.filename))
                zout.writestr(item, buffer)
            else:
                _duplicate_found = True
                log.info("  Skipped adding {}".format(item.filename))
            self.__DATA = __TEMP

        return _duplicate_found

    def clean_old_images(self):
        _old_images_found = False
        log.info("Cleaning old images from container")
        zin = zipfile.ZipFile(self.__DATA)
        __TEMP = io.BytesIO()
        zout = zipfile.ZipFile(__TEMP, "a")

        file_index = []
        data = self.data()
        for poke, data in data['pokemon.json'].items():
            if "sprite" in data:
                file_index.append(data["sprite"])
            if "icon" in data:
                file_index.append(data["icon"])

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename in file_index or item.filename.endswith(".json"):
                log.info("  Keeping {}".format(item.filename))
                zout.writestr(item, buffer)
            else:
                _old_images_found = True
                log.info("  Skipped adding {}".format(item.filename))
            self.__DATA = __TEMP

        return _old_images_found

    def data(self):
        z = zipfile.ZipFile(self.__DATA)
        if "data.json" in [x.filename for x in z.filelist]:
            with z.open("data.json") as f:
                data = json.load(f)
            return data
        return None

    def index(self):
        z = zipfile.ZipFile(self.__DATA)
        if "index.json" in [x.filename for x in z.filelist]:
            with z.open("index.json") as f:
                data = json.load(f)
            return data
        return None

    def image(self, name):
        with zipfile.ZipFile(self.__DATA).open(name) as f:
                    data = f.read()
        return data

    def delete_entry(self, file, entry):
        data = self.data()
        del data[file][entry]
        self.add("data.json", data)


if __name__ == '__main__':
    container = Container()
    # container.load(r"/Users/mattias.hedberg/Desktop/baby birds.fkmn")
    container.load(r"C:\Users\Jerakin\baby birds.fkmn")

    container.data()

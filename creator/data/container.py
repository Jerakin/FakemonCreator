import io
import sys
import json
import zipfile
from pathlib import Path
import logging as log

from creator.utils import util
from creator.utils import validate

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class Container:
    def __init__(self):
        self.__DATA = None
        self.path = None

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
        data = self.data()
        errors.extend(validate.validate(root / "res/schema/pokemon.json", data["pokemon.json"]))
        errors.extend(validate.validate(root / "res/schema/pokedex_extra.json", data["pokedex_extra.json"]))
        errors.extend(validate.validate(root / "res/schema/moves.json", data["moves.json"]))
        errors.extend(validate.validate(root / "res/schema/evolve.json", data["evolve.json"]))

        index = util.get_package_index()
        if index:
            metadata = self.index()
            for entry in index:
                if entry["name"] == metadata["name"]:
                    if entry["version"] >= metadata["version"]:
                        errors.append(
                            "The name of the package is taken, if this is an update to an existing package\n"
                            "then click the Update Existing button and select the package.")

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
            return
        with open(self.path, "wb") as f:
            f.write(self.__DATA.getvalue())

    def add(self, path, data=None):
        if path in [x.filename for x in zipfile.ZipFile(self.__DATA).filelist]:
            log.info("Removed file {} from zip".format(path))
            self.remove(path)
        if not data:
            with zipfile.ZipFile(self.__DATA, "a") as f:
                log.info("Writing file {} to zip".format(path))
                f.write(str(path), path.name)
        else:
            with zipfile.ZipFile(self.__DATA, "a") as f:
                log.info("Writing json {} to zip".format(path))
                f.writestr(str(path), json.dumps(data, ensure_ascii=False))

    def remove(self, filename):
        if isinstance(filename, Path):
            filename = filename.name
        __TEMP = io.BytesIO()
        zin = zipfile.ZipFile(self.__DATA)
        zout = zipfile.ZipFile(__TEMP, "a")
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename != filename:
                log.info("Keeping {}".format(filename))
                zout.writestr(item, buffer)
            else:
                log.info("Skipped adding {}".format(filename))
        self.__DATA = __TEMP

    def data(self):
        with zipfile.ZipFile(self.__DATA).open("data.json") as f:
            data = json.load(f)
        return data

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

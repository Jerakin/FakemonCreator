import argparse
import zipfile
import json
import shutil
from pathlib import Path

__version__ = "0.1"


class IncompletePackage(Exception):
    pass


def options():
    parser = argparse.ArgumentParser(description='Commandline tool to publish Fakemon Package')
    sub_parsers = parser.add_subparsers(dest="command")
    parser.add_argument('--version', action='version', version="DefBuild {}".format(__version__))

    sub_parsers.add_parser("peek", help="Echo information about the package")
    _add = sub_parsers.add_parser("add", help="Add the package")
    _add.add_argument("package", help="package to add")
    _add.add_argument("-pi", "--package_index", dest="package_index")
    input_args = parser.parse_args()

    return input_args


def add(package_path, package_index):
    package_path = Path(package_path)
    package_index = Path(package_index)
    z = zipfile.ZipFile(package_path)
    if "index.json" not in [x.filename for x in z.filelist]:
        raise IncompletePackage
    try:
        shutil.copy(str(package_path), str(package_index / "packages"))
    except shutil.SameFileError:
        print("Skipping moving becasue of SameFileError")

    package_index_file = package_index / "index.json"
    with package_index_file.open() as fp:
        package_index_json = json.load(fp)

    with z.open("index.json") as f:
        index_json = json.load(f)
    index_json["path"] = "packages/" + str(package_path.name)

    for package in package_index_json:
        if package["name"] == index_json["name"]:
            package["name"] = index_json["name"]
            package["author"] = index_json["author"]
            package["description"] = index_json["description"]
            package["version"] = index_json["version"]
            break

    with package_index_file.open("w") as fp:
        json.dump(package_index_json, fp, indent="  ", ensure_ascii=False)


def print_help():
    print("Usage: publisher <command> [<args>]\n")
    print("The commands are:")
    print("    add     Add the package to the index")
    print("    peek    NotImplementedError")

    print("See `publisher <command> --help` for information on a specific command.")


def main():
    _options = options()
    if _options.command == "add":
        add(_options.package, _options.package_index)
    elif _options.command == "peek":
        raise NotImplementedError
    else:
        print_help()
        add("/Users/mattias.hedberg/Downloads/AdodsOPEmporium.fkmn", "/Users/mattias.hedberg/Documents/repositories/FakemonPackages")


if __name__ == "__main__":
    main()

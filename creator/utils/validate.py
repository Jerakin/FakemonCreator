import jsonschema
import json
from pathlib import Path
from creator.utils import util
import logging as log


def _errors(sorted_errors):
    collection_of_errors = list()
    for error in sorted_errors:
        if "error" in error.schema:
            collection_of_errors.append("{} for {} ({})".format(error.schema["error"], error.path[0], error.path[-1]))
        else:
            collection_of_errors.append("{} for {} ({})".format(error.message, error.path[0], error.path[-1]))
    return collection_of_errors


def validate(schema_url, _data):
    with Path(schema_url).open(encoding="utf8") as f:
        schema = json.load(f)

    v = jsonschema.Draft7Validator(schema)
    sorted_errors = sorted(v.iter_errors(_data), key=str)
    return _errors(sorted_errors)


def validate_path(schema_url, resource_url):
    with Path(schema_url).open(encoding="utf8") as f:
        schema = json.load(f)

    with Path(resource_url).open(encoding="utf8") as f:
        _data = json.load(f)

    v = jsonschema.Draft7Validator(schema)
    sorted_errors = sorted(v.iter_errors(_data), key=str)
    return _errors(sorted_errors)


def validate_package_name(container):
    errors = list()
    index = util.get_package_index()
    if index:
        metadata = container.index()
        for entry in index:
            if entry["name"] == metadata["name"]:
                if entry["version"] >= metadata["version"]:
                    errors.append(
                        "The name of the package is taken, if this is an update to an existing package\n"
                        "then click the Update Existing button and select the package.")
    return errors


def clean_container(container):
    data = container.data()

    def clean_pokedex_extra():
        indexes = list()
        _changed = False
        for species, info in data["pokemon.json"].items():
            indexes.append(info["index"])
        for index, info in sorted(list(data["pokedex_extra.json"].items()), key=lambda x: x[0].lower(), reverse=True):
            if int(index) not in indexes:
                log.info("Index number not under use {}".format(index))
                del data["pokedex_extra.json"][index]
                _changed = True
        if _changed:
            container.add("data.json", data)

    def clean_zip():
        errors = container.clean()
        if errors:
            return ["Removed duplicated images, make sure that your images are still correct"]
        return []

    clean_pokedex_extra()
    return clean_zip()

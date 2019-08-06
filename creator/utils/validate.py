import jsonschema
import json
from pathlib import Path


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


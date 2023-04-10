from jsonschema import validate

from src.services.util import get_content_json


def validate_event(json_data: any, schema_name: str):

    schema_data = get_content_json(schema_name)
    return validate(json_data, schema_data)

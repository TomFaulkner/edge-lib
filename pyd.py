from typing import Any

from pydantic import BaseModel, create_model

type_mapping = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
}

ModelConfig = dict[str, tuple[str, Any]]


def _dict_to_typed(model_config: ModelConfig) -> dict[str, tuple[str, Any]]:
    response: dict[str, tuple[str, Any]] = {}
    for name, (type_, default) in model_config.items():
        if default is None:
            default = ...
        response[name] = (type_mapping[type_], default)
    return response


def create_model_from_dict(name: str, model_config: ModelConfig) -> type[BaseModel]:
    """Create Pydantic Model from dict.

    >>> model = model_config = {
        "name": ("str", None),
        "number": ("int", 42),
        "truth": ("bool", True),
    }
    >>> model.schema()
    {'title': 'CB',
    'type': 'object',
    'properties': {'model_config': {'title': 'Model Config',
    'default': {'name': ('str', None),
        'number': ('int', 42),
        'truth': ('bool', True)},
    'type': 'object'}}}
    """
    return create_model(name, **_dict_to_typed(model_config))

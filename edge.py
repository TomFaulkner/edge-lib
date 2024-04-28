from typing import Any

import edgedb
from fastapi.encoders import jsonable_encoder


def _encode_obj(obj):
    answer = {}
    for attr in dir(obj):
        val = getattr(obj, attr)
        answer[attr] = jsonable_encoder(val)
    return answer


def _encode_set(obj):
    return [jsonable_encoder(x) for x in obj]


def set_to_list(obj: edgedb.Set) -> list[dict[str, Any]]:
    return _encode_set(obj)


def obj_to_dict(obj: edgedb.Object) -> dict[str, Any]:
    return _encode_obj(obj)

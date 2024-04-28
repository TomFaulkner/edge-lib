#!/usr/bin/env python3

from collections.abc import Sequence
from pathlib import Path

import wat.data.queries_async as module

file = "src/wat/data/queries_async.py"

indent = "    "


def _to_camel(s: str) -> str:
    set_cap = False
    result = s[0].capitalize()
    for char in s[1:]:
        if char == "_":
            set_cap = True
            continue
        if set_cap:
            result += char.capitalize()
            set_cap = False
            continue
        result += char
    return result


def gather_inputs(fn, additional_ignores: Sequence[str] = None) -> dict[str, str]:
    ignores = ["return"]
    if additional_ignores:
        ignores += additional_ignores
    ants = fn.__annotations__
    return {
        name: repr(hint).strip("'")
        for name, hint in ants.items()
        if name not in ignores
    }


def gather_imports(filtered_annotations: dict[str, str]) -> set[str]:
    defaults = set("bool bytes int float str set dict list".split())
    return {i for i in filtered_annotations.values() if i not in defaults}


def gather_functions(module):
    functions = []
    for item in dir(module):
        if not callable(getattr(module, item)):
            continue
        if item[0].isupper():
            continue
        functions.append(item)
    return functions


def generate_class(name: str, inputs: dict[str, str]):
    # buffer = f"@dataclasses.dataclass\nclass {_to_camel(name)}:\n"
    buffer = f"class {_to_camel(name)}(pydantic.BaseModel):\n"
    if not inputs.items():
        return ""
    for name, hint in inputs.items():
        buffer += f"{indent}{name}: {hint}\n"
    buffer += "\n"
    return buffer


def generate_imports(imports: set[str]) -> str:
    return "\n".join(sorted([f'import {i.split(".")[0]}' for i in imports]))


def main():
    imports = {"dataclasses"}
    output = ""
    for fn in gather_functions(module):
        inputs = gather_inputs(getattr(module, fn), ["executor"])
        imports = imports | gather_imports(inputs)
        output += generate_class(fn, inputs)
    with Path("models.py").open("w") as f:
        # f.write(generate_imports(imports))
        f.write("\n\n\n")
        f.write(output)


class File404(Exception):
    def __init__(self, error: str):
        super().__init__(error)


def execute(file: str):
    import importlib
    import importlib.util
    import sys

    file_path = file
    module_name = file.removeprefix("queries/")

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise File404(error=f"Couldn't find {file}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    imports = {"dataclasses"}
    output = ""
    for fn in gather_functions(module):
        inputs = gather_inputs(getattr(module, fn), ["executor"])
        imports = imports | gather_imports(inputs)
        output += generate_class(fn, inputs)
    output += "\n\n\n"
    return output


if __name__ == "__main__":
    print("Generating Input Dataclasses.")
    main()


def test_gather_functions():
    gather_functions(module)
    raise AssertionError()


def test_to_camel():
    assert _to_camel("add_a_transaction") == "AddATransaction"

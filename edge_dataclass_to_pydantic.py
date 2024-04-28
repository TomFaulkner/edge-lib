#!/usr/bin/env python3


buffer = ""
found_definition = False
end_of_definition = False

with open("src/wat/data/queries_async.py") as f:
    for line in f.readlines():
        if not found_definition:
            if "class NoPydanticValidation" in line:
                found_definition = True
                continue
        elif found_definition and not end_of_definition:
            if line == "\n":
                end_of_definition = True
            continue

        if "import dataclasses" in line:
            continue
        if "@dataclasses.dataclass" in line:
            continue
        if "NoPydanticValidation" in line:
            line = line.replace("NoPydanticValidation", "pydantic.BaseModel")
        buffer += line

with open("src/wat/data/queries_async.py", "w") as f:
    f.write(buffer)

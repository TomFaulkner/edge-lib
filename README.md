# Edge Libraries
These are some things I found helpful when working with EdgeDB.

## Table of Contents
    - edge.py
      These functions use the FastAPI jsonable_encoder to convert EdgeDB query results to types that Pydantic can convert for FastAPI returns. (Edge sets to Python lists and objects to Python dictionaries)
    - edge_dataclass_to_pydantic.py
      Given a path (currently hardcoded, change it if you use this) replace the NoPydanticValidation with Pydantic BaseModel based schemas. This is probably unnecessary, but some people may find it helpful. With Pydantic v1 I had to deal with issues from this with models referred to other models that weren't yet defined. I had to call a Pydantic method to resolve this before using them.
    - pyd.py
      Tangentially related, this includes a function to create a Pydantic model from a Python dictionary.
    - tasks.py
      This is an Invoke make alternative with one endpoint, to show the workflow I've used for EdgeDB in the past. This runs the edgedb-py cli for code generation, copies it, runs edge_model_gen, copies the generated code to where I used it, then runs isort and black on the outputted code.
    - tests/functional/conftest.py and tests/functional/test_edgedb_fixture.py
      Pytest fixture and examples showing how I have tested EdgeDB queries in the past.

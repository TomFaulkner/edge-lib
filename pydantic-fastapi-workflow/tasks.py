#!/usr/bin/env python3
import os
import re
from pathlib import Path
from invoke import Collection, task
from src.sharing.generator import Generator


@task
def edge(c, input_dir="src/new/api/queries", output_file="src/new/api/queries_merged.py"):
    generator = Generator()
    generator.process_directory(Path(input_dir), parallel=True)
    c.run(
        f"""
    pdm install
    python merge_generated_files.py --input-dir {input_dir} --output-file {output_file}
    black {output_file}
    ruff format src/new/api/
    ruff check src/new/api/ --fix
    """
    )


namespace = Collection(edge, )

# def replace_section_content(text, pattern, new_content):
#     return re.sub(
#         pattern, rf"My edgedb schema:\n```\n{new_content}\n```", text, flags=re.DOTALL
#     )
#
#
# @task
# def update_schema(c):
#     cursorrules_file = ".cursorrules"
#
#     try:
#         with open(cursorrules_file, "r") as file:
#             text = file.read()
#     except FileNotFoundError:
#         print(f"Error: File '{cursorrules_file}' not found.")
#         return
#
#     pattern = r"My edgedb schema:\n```\n(.*?)\n```"
#
#     # Get the current script's directory
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     schema_file_path = os.path.join(script_dir, "dbschema", "default.esdl")
#
#     try:
#         with open(schema_file_path, "r") as schema_file:
#             new_content = schema_file.read().strip()
#     except FileNotFoundError:
#         print(f"Error: Schema file '{schema_file_path}' not found.")
#         return
#
#     modified_text = replace_section_content(text, pattern, new_content)
#
#     with open(cursorrules_file, "w") as file:
#         file.write(modified_text)
#
#     print(f"Updated {cursorrules_file} with the new schema.")

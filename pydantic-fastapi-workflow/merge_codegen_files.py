import argparse
from pathlib import Path

def merge_files(input_dir, output_file):
    # Read the content of all generated files
    generated_files = Path(input_dir).glob("*.py")
    content = ""
    imported_modules = set()
    edgeql_queries = {}

    for file in generated_files:
        query_name = file.stem.upper()
        query_variable = f"{query_name}_QUERY"
        with open(file, "r") as f:
            lines = f.readlines()
            current_query = None
            in_function = False
            for line in lines:
                if line.startswith("from") or line.startswith("import"):
                    if line.strip() not in imported_modules:
                        content += line
                        imported_modules.add(line.strip())
                elif line.startswith("EDGEQL_QUERY"):
                    if current_query is None:
                        current_query = query_name
                        edgeql_queries[current_query] = f"{query_variable} = "
                    edgeql_queries[current_query] += line.split("=", 1)[1].strip() + "\n"
                elif line.startswith("async def"):
                    in_function = True
                    content += line
                else:
                    if current_query:
                        if line.strip() == '"""':
                            edgeql_queries[current_query] += '"""\n'
                            current_query = None
                        else:
                            edgeql_queries[current_query] += line
                    else:
                        if in_function:
                            if "EDGEQL_QUERY" in line:
                                line = line.replace("EDGEQL_QUERY", query_variable)
                            if line.startswith("    return"):
                                in_function = False
                        content += line

    # Write the merged content to a single file
    with open(output_file, "w") as f:
        for module in sorted(imported_modules):
            f.write(module + "\n")
        f.write("\n")
        for query in edgeql_queries.values():
            f.write(query + "\n")
        f.write("\n\n")
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge Python files into a single file.")
    parser.add_argument("--input-dir", default="src/new/api/queries", help="Directory containing the input files (default: src/new/api/queries)")
    parser.add_argument("--output-file", default="src/new/api/queries_merged.py", help="Output file path (default: src/new/api/queries_merged.py)")
    args = parser.parse_args()

    merge_files(args.input_dir, args.output_file)
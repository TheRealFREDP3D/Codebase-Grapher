import ast
import json
import os
def traverse_ast(node, parent=None):
    """Recursively traverse the AST and keep track of parent nodes."""
    for child in ast.iter_child_nodes(node):
        child.parent = node
        traverse_ast(child, node)

def analyze_file(filepath):
    """Analyzes a single Python file and extracts information."""

    file_data = {
        "path": filepath,
        "classes": [],
        "functions": [],
        "imports": []
    }

    with open(filepath, "r") as source:
        tree = ast.parse(source.read())
    # Traverse the AST to set parent nodes
    traverse_ast(tree)

    # Extract Imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                file_data["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            file_data["imports"].append(node.module)

    # Extract Classes and Methods
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_data = {
                "name": node.name,
                "methods": []
            }
            for sub_node in node.body:
                if isinstance(sub_node, ast.FunctionDef):
                    class_data["methods"].append(sub_node.name)
            file_data["classes"].append(class_data)

    # Extract Top-Level Functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and isinstance(getattr(node, 'parent', None), ast.Module): # Check if it's a top-level function
          file_data["functions"].append(node.name)

    return file_data


def main():
    """Executes the analysis on a test file and prints the results.

    This function defines the main execution point of the script.
    It specifies the path to the test file, performs the analysis,
    and prints the results in JSON format.
    """
    filepath = "test_file.py"  # Test file path
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    analysis_result = analyze_file(filepath)
    print(json.dumps(analysis_result, indent=4))


if __name__ == "__main__":
    main()  
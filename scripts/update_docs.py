# Run this file with `python docs.py` or `python -m docs` to generate
# updated documentation for the client interface.

# Standard library imports
import ast
from os import path, listdir, mkdir

# KeyMaster imports
from utils.config import DOCS_DIR, ROOT

DOCS_DIR = path.join(ROOT, "docs")
CLASSES_DIR = path.join(ROOT, "classes")
UTILS_DIR = path.join(ROOT, "utils")
SCRIPTS_DIR = path.join(ROOT, "scripts")
CLIENT_DIR = path.join(ROOT, "client")


def create_dir(dir) -> None:
    """Creates a directory if it doesn't exist."""
    if not path.exists(dir):
        mkdir(dir)


def get_filenames(dir) -> list[str]:
    """Returns a list of all python files in a directory."""
    filenames = []
    for filename in listdir(dir):
        if filename.endswith(".py"):
            filenames.append(filename)
    return filenames


def get_files() -> dict[str, list[str]]:
    """Returns a dictionary of folder:list of filenames."""
    files = {}
    files['scripts'] = get_filenames(SCRIPTS_DIR)
    files['utils'] = get_filenames(UTILS_DIR)
    files['classes'] = get_filenames(CLASSES_DIR)
    files['client'] = get_filenames(CLIENT_DIR)
    return files


def create_directories() -> None:
    """Creates the docs directory and subdirectories if they don't exist."""
    create_dir(DOCS_DIR)
    create_dir(path.join(DOCS_DIR, "classes"))
    create_dir(path.join(DOCS_DIR, "utils"))
    create_dir(path.join(DOCS_DIR, "scripts"))
    create_dir(path.join(DOCS_DIR, "client"))


def extract_class_info(source):
    """
    Extracts class name and docstring for each class in the source code.
    """
    tree = ast.parse(source)
    class_info = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            docstring = ast.get_docstring(node, clean=True)
            class_info.append((class_name, docstring))

    return class_info


def extract_function_info(source):
    """
    Extracts function name, parameters, and docstring for each function in the source code.
    """
    tree = ast.parse(source)
    function_info = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            # params = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node, clean=True)
            # function_info.append((func_name, params, docstring))
            function_info.append((func_name, docstring))

    return function_info


def write_to_markdown(class_info, function_info, filepath):
    """Writes function information to a markdown file."""
    errors = []
    error_count = 0
    with open(filepath, 'w') as file:
        if len(class_info) != 0:
            file.write('# Class Documentation\n\n')
            for info in class_info:
                class_name = info[0]
                file.write(f'## Class: `{class_name}`\n')
                if info[1] is None:
                    continue
                file.write(info[1] + '\n\n')
        if len(function_info) == 0:
            return
        file.write('# Function Documentation\n\n')
        def wrap_in_grave(x): return "`" + x + "`"

        ERROR_BASE = 'ERROR: FIX DOCSTRING. '
        for info in function_info:
            function_name = info[0]
            if function_name[:2] == '__' and function_name[-2:] == '__':
                continue
            function_name = wrap_in_grave(function_name)
            file.write(f'## Method: {function_name}\n')
            if info[1] is None:
                continue
            file.write(info[1] + '\n\n')


def main():
    """
    Main function to read the input file and store function information.
    """
    create_directories()
    files = get_files()
    for folder in files:
        if folder == 'utils':
            continue
            source_folder = UTILS_DIR
        elif folder == 'classes':
            continue
            source_folder = CLASSES_DIR
        elif folder == 'scripts':
            continue
            source_folder = SCRIPTS_DIR
        elif folder == 'client':
            source_folder = CLIENT_DIR
        else:
            raise ValueError("Invalid folder name.")
        filenames = files[folder]
        for filename in filenames:
            if filename == '__init__.py':
                continue
            source_filepath = path.join(source_folder, filename)
            with open(source_filepath, 'r') as f:
                source = f.read()
            class_info = extract_class_info(source)
            function_info = extract_function_info(source)
            new_filename = f'docs_{filename[:-3]}.md'
            new_filepath = path.join(DOCS_DIR, folder, new_filename)
            write_to_markdown(class_info, function_info, new_filepath)
            print(f'{filename} ☑')


if __name__ == "__main__":
    main()

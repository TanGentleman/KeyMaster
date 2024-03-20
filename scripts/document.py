# Run this file with `python docs.py` or `python -m docs` to generate
# updated documentation for the client interface.

# Standard library imports
import ast
from os import path, listdir, mkdir

# KeyMaster imports
from utils.config import ROOT

DOCS_DIR = path.join(ROOT, "docs")
CLASSES_DIR = path.join(ROOT, "classes")
UTILS_DIR = path.join(ROOT, "utils")
SCRIPTS_DIR = path.join(ROOT, "scripts")
CLIENT_DIR = path.join(ROOT, "client")

PRODUCTION_DIRS = [CLIENT_DIR]


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


def get_files(directories: list[str]) -> dict[str, list[str]]:
    """Returns a dictionary of folder:list of filenames."""
    files = {}
    for folderpath in directories:
        # get the filenames for each filepath
        folder = path.basename(folderpath)
        files[folder] = get_filenames(folderpath)

    return files


def create_directories() -> None:
    """Creates the docs directory and subdirectories if they don't exist."""
    create_dir(DOCS_DIR)
    create_dir(path.join(DOCS_DIR, "classes"))
    create_dir(path.join(DOCS_DIR, "utils"))
    create_dir(path.join(DOCS_DIR, "scripts"))
    create_dir(path.join(DOCS_DIR, "client"))


def extract_class_info(source) -> list[tuple]:
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


def extract_function_info(source) -> list[tuple]:
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


def write_to_markdown(
        class_info: list[tuple], function_info, filepath):
    """Writes function information to a markdown file."""
    # errors = []
    # error_count = 0
    with open(filepath, 'w') as file:
        if len(class_info) != 0:
            file.write('# Class Documentation\n\n')
            for info in class_info:
                class_name = info[0]
                file.write(f'## Class: `{class_name}`\n')
                if info[1] is None:
                    continue
                # chunks: list[str] = []
                # chunks = info[1].split('\n\n')
                # for chunk in chunks:
                #     lines = chunk.splitlines()
                #     if len(lines) == 0:
                #         continue
                #     if 'Parameters' in lines[0] or 'Attributes' in lines[0]:
                #         print('yee')
                #         raise ValueError('yee')
                #     for line in lines:
                #         if line == '':
                #             continue
                #         if 'Parameters' in line or 'Attributes' in line:
                #             if not lines[1] or '----------' not in lines[1]:
                #                 print(f'Missing Separator! {class_name} in {filepath[-20:]}')
                #                 file.write(chunk + '\n\n')
                #                 break
                #             # Write parameters block and then break
                #             # Append '- ' to each line after the separator
                #             file.write(line + '\n')
                #             file.write(lines[1] + '\n')
                #             for line in lines[2:]:
                #                 file.write(f'- {line}\n')
                #             print('Bullets after separator ☑')
                #             print(f'{class_name} in {filepath[-20:]}')
                #             print(chunk)
                #             break

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
    files = get_files(PRODUCTION_DIRS)
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

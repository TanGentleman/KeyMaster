# Run this file with `python docs.py` or `python -m docs` to generate
# updated documentation for the client interface.

# Standard library imports
import ast
from typing import List, Tuple
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


def get_filenames(dir) -> List[str]:
    """Returns a list of all python files in a directory."""
    filenames = []
    for filename in listdir(dir):
        if filename.endswith(".py"):
            filenames.append(filename)
    return filenames


def get_files() -> dict[str, List[str]]:
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


def extract_function_info(source):
    """
    Extracts function name, parameters, and docstring for each function in the source code.
    """
    tree = ast.parse(source)
    function_info = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            params = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node, clean=True)
            function_info.append((func_name, params, docstring))

    return function_info


def write_to_markdown(function_info, filepath) -> Tuple[List[str], int]:
    """Writes function information to a markdown file."""
    with open(filepath, 'w') as file:
        file.write('# Function Documentation\n\n')

        def wrap_in_grave(x): return "`" + x + "`"
        errors = []
        error_count = 0
        ERROR_BASE = 'ERROR: FIX DOCSTRING. '

        for info in function_info:
            function_name = wrap_in_grave(
                "init" if "__init__" in info[0] else info[0])
            file.write(f'## Function: {function_name}\n')
            if info[2] is None:
                continue
            content_chunks: list[str] = info[2].split('\n\n')
            # check if one liner
            chunk_count = len(content_chunks)
            if chunk_count == 1:
                file.write(info[2] + '\n')
                continue
            if chunk_count > 3:
                error_message = f'Chunk count {chunk_count} > 3'
                file.write(ERROR_BASE + error_message + '\n')
                errors.append(error_message)
                error_count += 1
                continue
            # write docstring
            for i in range(len(content_chunks)):
                if i == 0:
                    info_string = content_chunks[i].strip()
                    file.write(info_string + '\n')
                elif i == 1:
                    if 'Args:' not in content_chunks[i]:
                        if 'Returns:' in content_chunks[i]:
                            # Write without the returns
                            return_block = content_chunks[i].split('\n')
                            file.write(f'### Returns\n')
                            for line in return_block:
                                line = line.strip()
                                if line == "Returns:":
                                    continue
                                file.write(line + '\n')
                        continue
                    file.write(f'### Parameters:\n')
                    args_block = content_chunks[i].split('\n')
                    for arg in args_block:
                        arg = arg.strip()
                        if arg == "Args:":
                            continue
                        file.write(f'- {arg}\n')
                elif i == 2:
                    if 'Args:' in content_chunks[i]:
                        error_message = 'Args should be chunk 2, not 3'
                        file.write(ERROR_BASE + error_message + '\n')
                        errors.append(error_message)
                        error_count += 1
                        continue
                    if 'Returns:' not in content_chunks[i]:
                        continue
                    return_block = content_chunks[i].split('\n')
                    file.write(f'### Returns\n')
                    for line in return_block:
                        line = line.strip()
                        if line == "Returns:":
                            continue
                        file.write(line + '\n')
    if len(errors) != error_count:
        print("Error count does not match error list length!")
    return errors, error_count


def main():
    """
    Main function to read the input file and store function information.
    """
    create_directories()
    files = get_files()
    for folder in files:
        if folder == 'utils':
            source_folder = UTILS_DIR
        elif folder == 'classes':
            source_folder = CLASSES_DIR
        elif folder == 'scripts':
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
            print(f'Documenting {filename}...')
            with open(source_filepath, 'r') as f:
                source = f.read()
            function_info = extract_function_info(source)
            new_filename = f'docs_{filename[:-3]}.md'
            new_filepath = path.join(DOCS_DIR, folder, new_filename)
            errors, error_count = write_to_markdown(
                function_info, new_filepath)
            if error_count == 0:
                print(f'File {filename} is now well documented.')
            else:
                count = 0
                for error in errors:
                    count += 1
                    print(f'{count}. {error}')


if __name__ == "__main__":
    main()

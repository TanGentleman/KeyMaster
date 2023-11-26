# Run this file with `python docs.py` or `python -m docs` to generate updated documentation for the client interface.

# Standard library imports
import ast
from os import path, listdir

# KeyMaster imports
from utils.config import DOCS_DIR, ROOT

CLASSES_DIR = path.join(ROOT, "classes")

# Iterate through folder to collect all filenames
def get_filenames():
    """Returns a list of all filenames in the classes directory."""
    filenames = []
    for filename in listdir(CLASSES_DIR):
        if filename.endswith(".py"):
            filenames.append(filename)
    return filenames

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

def write_to_markdown(function_info, filepath) -> tuple[list[str], int]:
    """Writes function information to a markdown file."""
    with open(filepath, 'w') as file:
        file.write('# Function Documentation\n\n')
        file.write('This file contains documentation for all functions in the project.\n\n')
        wrap_in_grave = lambda x: "`" + x + "`"
        errors = []
        error_count = 0
        ERROR_BASE = 'ERROR: FIX DOCSTRING. '
        
        for info in function_info:
            function_name = wrap_in_grave("init" if "__init__" in info[0] else info[0])
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
                    file.write(f'{content_chunks[i]}\n')
                elif i == 1:
                    if 'Args:' not in content_chunks[i]:
                        continue
                    file.write(f'### Parameters:\n')
                    args_block = content_chunks[i].split('\n')
                    for arg in args_block:
                        if arg.strip() == "Args:":
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
                        if line.strip() == "Returns:":
                            continue
                        file.write(line + '\n')
    if len(errors) != error_count:
        print("Error count does not match error list length!")
    return errors, error_count

def main():                                                                  
    """                                                                      
    Main function to read the input file and store function information.     
    """   
    files = get_filenames()     
    for filename in files:
        if filename == '__init__.py':
            continue
        print(f'Documenting {filename}...')
        filepath = path.join(CLASSES_DIR, filename)
        with open(filepath, 'r') as f:                                      
            source = f.read()                                                 

        function_info = extract_function_info(source)  
        new_filename = f'docs_{filename[:-3]}.md'
        new_filepath = path.join(DOCS_DIR, new_filename)
        errors, error_count = write_to_markdown(function_info, new_filepath)
        if error_count == 0:
            print(f'File {filename} is now well documented.')
        else:
            count = 0
            for error in errors:
                count += 1
                print(f'{count}.: {error}')
                                                                            
if __name__ == "__main__":                                                   
    main()                                                                   

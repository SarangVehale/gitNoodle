import os
from pathlib import Path
import subprocess
import ast

def clone_repository(repo_url, clone_dir="cloned_repo"):
    """
    Clones the GitHub repository to a local directory.
    """
    if os.path.exists(clone_dir):
        print(f"Directory '{clone_dir}' already exists. Skipping clone.")
        return clone_dir

    print(f"Cloning repository from {repo_url}...")
    try:
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        print("Repository cloned successfully.")
        return clone_dir
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        return None

def get_code_description(file_path):
    """
    Extracts function and class definitions from a Python file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=file_path)
        description = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                description.append(f"Function: {node.name} (Line {node.lineno})")
            elif isinstance(node, ast.ClassDef):
                description.append(f"Class: {node.name} (Line {node.lineno})")
        return description
    except Exception as e:
        return [f"Error parsing file: {e}"]

def get_file_structure(directory, prefix=""):
    """
    Recursively retrieves the file structure of a directory.
    """
    structure = []
    for item in Path(directory).iterdir():
        if item.is_dir():
            structure.append(f"{prefix}📁 {item.name}/")
            structure.extend(get_file_structure(item, prefix + "    "))
        elif item.is_file():
            structure.append(f"{prefix}📄 {item.name}")
            if item.suffix == ".py":
                description = get_code_description(item)
                if description:
                    structure.append(f"{prefix}    Description:")
                    for line in description:
                        structure.append(f"{prefix}    - {line}")
    return structure

def print_structure(structure):
    """
    Prints the file structure.
    """
    for item in structure:
        print(item)

def main():
    github_url = input("Enter the GitHub repository URL: ")
    clone_dir = "cloned_repo"

    # Clone the repository
    repo_path = clone_repository(github_url, clone_dir)
    if not repo_path:
        return

    # Get and print the file structure
    print("\nRepository File Structure:")
    structure = get_file_structure(repo_path)
    print_structure(structure)

    # Clean up (optional)
    # Uncomment the following lines to delete the cloned repository after printing the structure
    # print("\nCleaning up...")
    # subprocess.run(["rm", "-rf", clone_dir])

if __name__ == "__main__":
    main()

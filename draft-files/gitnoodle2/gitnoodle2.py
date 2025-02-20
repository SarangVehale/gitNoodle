import requests
import base64
import ast

# Replace with your GitHub Personal Access Token (PAT)
GITHUB_TOKEN = "your_personal_access_token_here"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repo_contents(url, path=""):
    """
    Recursively fetches the file structure of a GitHub repository using the GitHub API.
    """
    api_url = url.replace("https://github.com/", "https://api.github.com/repos/")
    if path:
        api_url += f"/contents/{path}"
    else:
        api_url += "/contents"

    response = requests.get(api_url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repository contents: {response.status_code} - {response.text}")

    contents = response.json()
    structure = []

    for item in contents:
        if item["type"] == "file":
            structure.append(f"{path}/{item['name']}" if path else item["name"])
        elif item["type"] == "dir":
            structure.append(f"{path}/{item['name']}/" if path else f"{item['name']}/")
            structure.extend(get_repo_contents(url, f"{path}/{item['name']}" if path else item["name"]))

    return structure

def get_code_description(file_url):
    """
    Extracts function and class definitions from a Python file using the GitHub API.
    """
    response = requests.get(file_url, headers=HEADERS)
    if response.status_code != 200:
        return [f"Error fetching file: {response.status_code} - {response.text}"]

    file_content = base64.b64decode(response.json()["content"]).decode("utf-8")
    try:
        tree = ast.parse(file_content)
        description = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                description.append(f"Function: {node.name} (Line {node.lineno})")
            elif isinstance(node, ast.ClassDef):
                description.append(f"Class: {node.name} (Line {node.lineno})")
        return description
    except Exception as e:
        return [f"Error parsing file: {e}"]

def print_structure(structure, repo_url, indent=0):
    """
    Prints the file structure with proper indentation and code descriptions.
    """
    for item in structure:
        if item.endswith("/"):
            print(" " * indent + f"📁 {item}")
            print_structure([i for i in structure if i.startswith(item) and i != item], repo_url, indent + 4)
        else:
            print(" " * indent + f"📄 {item}")
            if item.endswith(".py"):
                file_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + f"/contents/{item}"
                description = get_code_description(file_url)
                if description:
                    print(" " * (indent + 4) + "Description:")
                    for line in description:
                        print(" " * (indent + 8) + f"- {line}")

def main():
    github_url = input("Enter the GitHub repository URL: ")
    try:
        structure = get_repo_contents(github_url)
        print("\nRepository File Structure:")
        print_structure(structure, github_url)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()



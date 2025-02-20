import os
import requests
import zipfile
import tempfile
from urllib.parse import urlparse

def parse_github_url(url):
    """Parse GitHub URL to extract owner, repository, and branch."""
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    owner = path_parts[0]
    repo = path_parts[1]
    branch = 'main'
    
    try:
        tree_index = path_parts.index('tree')
        branch = path_parts[tree_index + 1]
    except (ValueError, IndexError):
        pass  # Use default branch if 'tree' not found
    
    return owner, repo, branch

def download_repo(url):
    """Download repository as ZIP and return extracted directory path."""
    owner, repo, branch = parse_github_url(url)
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    
    response = requests.get(zip_url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download repository: {response.status_code}")
    
    temp_dir = tempfile.TemporaryDirectory()
    zip_path = os.path.join(temp_dir.name, 'repo.zip')
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir.name)
    
    extracted_folder = os.path.join(temp_dir.name, f"{repo}-{branch}")
    if not os.path.exists(extracted_folder):
        extracted_folder = os.path.join(temp_dir.name, os.listdir(temp_dir.name)[0])
    
    return extracted_folder, temp_dir

def print_structure(path, indent=0):
    """Recursively print directory structure with proper formatting."""
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(f"{' ' * indent}📁 {item}")
            print_structure(item_path, indent + 4)
        else:
            print(f"{' ' * indent}📄 {item}")

def main():
    url = input("Enter GitHub repository URL: ")
    try:
        extracted_path, temp_dir = download_repo(url)
        print("\nFile Structure:")
        print_structure(extracted_path)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        temp_dir.cleanup()

if __name__ == "__main__":
    main()

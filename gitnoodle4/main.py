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

def extract_file_description(file_path):
    """Extract description from file comments or metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Look for common comment patterns
        comment_patterns = {
            "python": ('"""', '"""'),
            "javascript": ('/**', '*/'),
            "java": ('/**', '*/'),
            "bash": ('#', ''),
            "html": ('<!--', '-->'),
        }
        
        # Determine file type based on extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".py":
            start, end = comment_patterns["python"]
        elif ext in (".js", ".ts"):
            start, end = comment_patterns["javascript"]
        elif ext == ".java":
            start, end = comment_patterns["java"]
        elif ext == ".sh":
            start, end = comment_patterns["bash"]
        elif ext == ".html":
            start, end = comment_patterns["html"]
        else:
            return None
        
        # Extract the first comment block
        description = []
        in_comment = False
        for line in lines:
            if start in line:
                in_comment = True
                line = line.split(start)[1].strip()
            if in_comment:
                if end in line:
                    description.append(line.split(end)[0].strip())
                    break
                description.append(line.strip())
        
        return " ".join(description) if description else None
    except Exception:
        return None

def extract_directory_description(dir_path):
    """Extract description from a README.md or DESCRIPTION.txt file."""
    readme_path = os.path.join(dir_path, "README.md")
    description_path = os.path.join(dir_path, "DESCRIPTION.txt")
    
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                return f.readline().strip()  # Use the first line of README.md
        except Exception:
            pass
    elif os.path.exists(description_path):
        try:
            with open(description_path, 'r', encoding='utf-8') as f:
                return f.readline().strip()  # Use the first line of DESCRIPTION.txt
        except Exception:
            pass
    return None

def print_structure(path, base_path, indent=0):
    """Recursively print directory structure with descriptions."""
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        description = None
        
        if os.path.isdir(item_path):
            description = extract_directory_description(item_path)
            print(f"{' ' * indent}📁 {item}/ {f'# {description}' if description else ''}")
            print_structure(item_path, base_path, indent + 4)
        else:
            description = extract_file_description(item_path)
            print(f"{' ' * indent}📄 {item} {f'# {description}' if description else ''}")

def main():
    url = input("Enter GitHub repository URL: ")
    try:
        extracted_path, temp_dir = download_repo(url)
        print("\nFile Structure:")
        print_structure(extracted_path, extracted_path)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        temp_dir.cleanup()

if __name__ == "__main__":
    main()

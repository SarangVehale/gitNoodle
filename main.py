import os
import requests
import zipfile
import tempfile
import ollama
from urllib.parse import urlparse
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# ASCII Art for GitNoodle
GITNOODLE_ART = f"""
{Fore.CYAN}   ____ _ _   _   _       _      _ 
  / ___(_) |_| | | |_   _| | ___| |
 | |  _| | __| |_| | | | | |/ _ \\ |
 | |_| | | |_|  _  | |_| | |  __/_|
  \\____|_|\\__|_| |_|\\__,_|_|\\___(_)
{Style.RESET_ALL}
"""

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

def generate_description_with_ollama(content):
    """Generate a simple, one-line description using Ollama."""
    try:
        response = ollama.generate(
            model="llama3.2",  # Use the desired Ollama model
            prompt=f"Describe the purpose of the following code or file in one short sentence:\n\n{content}\n\nDescription:"
        )
        return response["response"].strip()
    except Exception as e:
        print(f"Error generating description with Ollama: {e}")
        return None

def extract_file_description(file_path):
    """Extract a simple description from file content using Ollama."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate a simple description using Ollama
        description = generate_description_with_ollama(content)
        return description
    except Exception:
        return None

def extract_directory_description(dir_path):
    """Extract a simple description from a README.md or DESCRIPTION.txt file."""
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

def print_structure(path, base_path, indent=0, score=0):
    """Recursively print directory structure with simple descriptions and update score."""
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        description = None
        
        if os.path.isdir(item_path):
            description = extract_directory_description(item_path)
            print(f"{' ' * indent}{Fore.GREEN}📁 {item}/{Style.RESET_ALL} {Fore.YELLOW}{f'# {description}' if description else ''}{Style.RESET_ALL}")
            score = print_structure(item_path, base_path, indent + 4, score + 1)
        else:
            description = extract_file_description(item_path)
            print(f"{' ' * indent}{Fore.BLUE}📄 {item}{Style.RESET_ALL} {Fore.YELLOW}{f'# {description}' if description else ''}{Style.RESET_ALL}")
            score += 1
    
    return score

def main():
    print(GITNOODLE_ART)
    print(f"{Fore.MAGENTA}Welcome to {Fore.CYAN}GitNoodle{Fore.MAGENTA}! Let's explore your repository.{Style.RESET_ALL}\n")
    
    url = input(f"{Fore.CYAN}Enter GitHub repository URL: {Style.RESET_ALL}")
    try:
        extracted_path, temp_dir = download_repo(url)
        print(f"\n{Fore.CYAN}File Structure:{Style.RESET_ALL}")
        score = print_structure(extracted_path, extracted_path)
        
        print(f"\n{Fore.GREEN}🎉 You scored {Fore.YELLOW}{score} points{Fore.GREEN}! 🎉{Style.RESET_ALL}")
        if score > 50:
            print(f"{Fore.CYAN}Wow, you're a GitNoodle master! 🏆{Style.RESET_ALL}")
        elif score > 20:
            print(f"{Fore.CYAN}Great job! You're getting the hang of it. 🌟{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Nice start! Keep exploring. 🚀{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    finally:
        temp_dir.cleanup()

if __name__ == "__main__":
    main()

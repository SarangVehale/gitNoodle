# GitHub Repository Structure Extractor

## Overview

The **GitHub Repository Structure Extractor** is a Python script that downloads a GitHub repository, extracts its file and directory structure, and generates concise descriptions for each file and directory. The script uses **Ollama**, an AI model, to dynamically generate descriptions based on the content of files and directories. This tool is particularly useful for quickly understanding the structure and purpose of a repository without manually inspecting each file.

---

## Features

- **Repository Download**: Automatically downloads a GitHub repository as a ZIP file.
- **Structure Extraction**: Extracts the file and directory structure of the repository.
- **Dynamic Descriptions**: Uses Ollama to generate **simple, one-line descriptions** for files and directories.
- **Directory Descriptions**: Reads `README.md` or `DESCRIPTION.txt` files in directories to provide descriptions.
- **Open Source and Offline**: Works offline once the repository is downloaded.
- **Language-Agnostic**: Supports repositories in any programming language or framework.

---

## Prerequisites

Before using the script, ensure you have the following installed:

1. **Python 3.7+**: Download and install Python from [python.org](https://www.python.org/).
2. **Ollama**: Install Ollama and ensure it is running locally or accessible via an API endpoint.
   - Install the `ollama` Python package:
     ```bash
     pip install ollama
     ```
3. Install any of the ollama models : 
    ```
    ollama run <model-name>
    ```
3. **GitHub Repository URL**: The script requires a valid GitHub repository URL as input.

---

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/SarangVehale/gitNoodle
   cd gitNoodle
   ```

2. Install the required Python packages:
   ```bash
   pip install requests
   ```

---

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Enter the GitHub repository URL when prompted:
   ```
   Enter GitHub repository URL: https://github.com/username/repository
   ```

3. The script will:
   - Download the repository.
   - Extract its structure.
   - Generate descriptions for files and directories.
   - Print the structure with descriptions.

### Example Output

For a repository with the following structure:
```
.
├── src/
│   ├── components/
│   │   └── README.md          # "UI components for the application"
│   ├── pages/
│   │   └── README.md          # "Page components for routing"
│   ├── context/
│   │   └── README.md          # "React context providers"
│   ├── hooks/
│   │   └── README.md          # "Custom React hooks"
│   └── lib/
│       └── README.md          # "Utility functions"
├── backend/
│   ├── main.py                # """FastAPI application entry point"""
│   └── requirements.txt       # "Python dependencies"
└── public/                    # "Static files served to the client"
```

The script will output:
```
File Structure:
📁 src/
    📁 components/ # UI components for the application
    📁 pages/ # Page components for routing
    📁 context/ # React context providers
    📁 hooks/ # Custom React hooks
    📁 lib/ # Utility functions
📁 backend/
    📄 main.py # FastAPI application entry point
    📄 requirements.txt # Python dependencies
📁 public/ # Static files served to the client
```

---

## How It Works

1. **Repository Download**:
   - The script converts the GitHub URL into a ZIP download link and downloads the repository.

2. **Structure Extraction**:
   - The repository is extracted to a temporary directory, and its file and directory structure is traversed.

3. **Description Generation**:
   - For **files**, the script reads the content and sends it to Ollama with a prompt to generate a **one-sentence description**.
   - For **directories**, the script looks for a `README.md` or `DESCRIPTION.txt` file and uses its first line as the description.

4. **Output**:
   - The script prints the repository structure with descriptions in a tree-like format.

---

## Customization

### Adding Descriptions for Specific Files or Directories

If you want to provide custom descriptions for specific files or directories, you can:

1. Add a `README.md` or `DESCRIPTION.txt` file to the directory.
2. Ensure the first line of the file contains the description.

### Modifying the Ollama Prompt

To change the format or style of the descriptions, modify the `generate_description_with_ollama` function in the script. For example, you can update the prompt to:
```python
prompt = f"Provide a one-line description of the following code or file:\n\n{content}\n\nDescription:"
```

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature or fix"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request and describe your changes.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Ollama**: For providing the AI model used to generate descriptions.
- **GitHub**: For hosting repositories and providing ZIP download functionality.

---

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/your-username/github-repo-structure-extractor/issues).

---

Enjoy exploring GitHub repositories with ease! 🚀

---

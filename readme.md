## This is just a tool I'm tinkering with, so YMMV

# Hugging Face Model Importer for Ollama

This project provides a Python script to import a specific model file from a Hugging Face repository into Ollama. The script allows you to list available files in the repository, select a specific file to download, and create a metafile required by Ollama. You can choose to run the `ollama create` command directly from the script or manually after editing the metafile.

## Features

- Prompts for a Hugging Face model ID and lists available files in the repository.
- Allows the user to select a specific file to download.
- Checks if the file already exists locally and prompts whether to redownload or skip.
- Creates a metafile required by Ollama with appropriate parameters.
- Prompts the user to confirm running the `ollama create` command.
- Allows the user to specify a name for the model when running `ollama create`.
- Convert Hugging Face Safe Tensor models to Guff then import into Ollama.

## Requirements

- Python 3.10 or higher
- `huggingface_hub` library
- `subprocess` module (part of Python standard library)
- `ollama` command-line tool

For SafeTensors conversion, llama.cpp is required but the script will offer to install it automatically.

## Installation

### Option 1: Using UV (Recommended)

[UV](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install UV if you haven't already:
   ```sh
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Create a virtual environment and install dependencies:
   ```sh
   uv venv

   # On macOS/Linux
   source .venv/bin/activate

   # On Windows
   .venv\Scripts\activate
   ```

3. Install the package:
   ```sh
   # For GGUF import only (minimal installation)
   uv pip install -e .

   # For GGUF import + SafeTensors conversion (includes PyTorch, transformers)
   uv pip install -e ".[convert]"

   # Or using requirements.txt
   uv pip install -r requirements.txt
   ```

4. Ensure you have the `ollama` command-line tool installed and properly configured.

**CPU-Only Installation (smaller download):**
   ```sh
   # Install PyTorch CPU-only version from custom index
   uv pip install -e ".[convert]" --extra-index-url https://download.pytorch.org/whl/cpu
   ```

### Option 2: Using Conda

1. Install the conda environment:
   ```sh
   conda env create -f condaenv.yml
   conda activate olguff
   ```

2. Ensure you have the `ollama` command-line tool installed and properly configured.

**CPU-Only Installation (smaller download):**
   ```sh
   # Modify condaenv.yml: add 'cpuonly' package after pytorch line
   # Then create environment as normal
   conda env create -f condaenv.yml
   conda activate olguff
   ```

### Option 3: Using pip (Traditional)

1. Create a virtual environment (recommended):
   ```sh
   python -m venv .venv

   # On macOS/Linux
   source .venv/bin/activate

   # On Windows
   .venv\Scripts\activate
   ```

2. Install the required Python library:
   ```sh
   pip install huggingface_hub

   # For SafeTensors conversion, also install:
   pip install torch transformers safetensors
   ```

3. Ensure you have the `ollama` command-line tool installed and properly configured.

**CPU-Only Installation (smaller download):**
   ```sh
   # Install PyTorch CPU-only version from custom index
   pip install torch transformers safetensors --extra-index-url https://download.pytorch.org/whl/cpu
   ```

## Configuration (Optional)

You can customize the tool's behavior by creating a `.env` file in the project root:

```sh
# Copy the example file
cp .env.example .env

# Edit .env to set your preferences
```

**Available settings:**
- `LLAMACPP_PATH` - Custom path to llama.cpp installation (if not using default `./llama.cpp`)
- `GGUF_DOWNLOAD_DIR` - Custom directory for GGUF downloads (default: `./dl`)
- `SAFETENSORS_DOWNLOAD_DIR` - Custom directory for SafeTensors downloads (default: `./sf`)

Example `.env`:
```
LLAMACPP_PATH=/usr/local/llama.cpp
```

## Usage

> **Note for Windows users**: Use `python` (not `python3`) when running scripts in the conda environment. The `python3` command may point to a different Python installation.

### Quick Start

Simply run the main script and choose your model type:

```sh
python main.py
```

The script will ask you whether you want to import:
1. **GGUF file** - For models already in GGUF format from Hugging Face
2. **SafeTensors model** - For models that need to be converted to GGUF first

Then follow the prompts to complete the import.

### For GGUF Models

When you select option 1 (GGUF file):

1. Enter the Hugging Face model ID when prompted
2. Select the GGUF file you want to download from the list
3. If the file already exists locally, decide whether to redownload it or skip
4. Confirm if you want to run the `ollama create` command:
   - If yes, provide a name for the model
   - If no, the script will print the command for you to run manually after editing the `metafile.txt`

### For SafeTensors Models

When you select option 2 (SafeTensors model):

1. Enter the Hugging Face model ID when prompted
2. The script will check for llama.cpp and offer to clone it if needed
3. The entire model repository will be downloaded
4. The model will be converted to GGUF format using llama.cpp
5. You'll be asked if you want to import the converted GGUF file into Ollama

### Advanced: Running Scripts Directly

You can also run the individual scripts directly:

**For GGUF files:**
```sh
python gufftoollama.py

# Or with a local GGUF file:
python gufftoollama.py path/to/model.gguf
```

**For SafeTensors conversion:**
```sh
python sftoguff.py
```


## Example

```sh
$ python main.py
============================================================
Ollama Model Importer
============================================================

This tool helps you import Hugging Face models into Ollama.

What type of model do you want to import?
1. GGUF file (already in GGUF format)
2. SafeTensors model (will be converted to GGUF)

Enter your choice (1 or 2): 1

============================================================
Starting GGUF to Ollama import...
============================================================

Enter the Hugging Face model ID: TheBloke/Llama-2-7B-GGUF
Available files in the repository:
1. .gitattributes
2. README.md
3. llama-2-7b.Q4_K_M.gguf
4. llama-2-7b.Q5_K_M.gguf
...
Enter the number of the file you want to download: 3
Enter the Ollama name for the model (default: llama-2-7b.Q4_K_M): llama2-7b
Do you want to proceed with the 'ollama create' command? (y/[n]): y
Model imported successfully!
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Contact

For any questions or issues, please post an issue on this repository.

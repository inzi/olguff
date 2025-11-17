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

## Attributions

## Requirements

- Python 3.10 or higher
- `huggingface_hub` library
- `subprocess` module (part of Python standard library)
- `ollama` command-line tool

For sftoguff.py, you'll need llama.cpp installed and functional on your system.

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
   # For main.py only (GGUF import)
   uv pip install -e .

   # For both main.py and sftoguff.py (includes conversion tools)
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

   # For sftoguff.py, also install:
   pip install torch transformers safetensors
   ```

3. Ensure you have the `ollama` command-line tool installed and properly configured.

**CPU-Only Installation (smaller download):**
   ```sh
   # Install PyTorch CPU-only version from custom index
   pip install torch transformers safetensors --extra-index-url https://download.pytorch.org/whl/cpu
   ```

## Usage

> **Note for Windows users**: Use `python` (not `python3`) when running scripts in the conda environment. The `python3` command may point to a different Python installation.

1. Run the script:
   ```sh
   python main.py
   ```

2. Enter the Hugging Face model ID when prompted.

3. Select the file you want to download from the list of available files.

4. If the file already exists locally, decide whether to redownload it or skip.

5. Confirm if you want to run the `ollama create` command:
   - If yes, provide a name for the model (default is the model name without the `.guff` extension).
   - If no, the script will print the command for you to run manually after editing the `metafile.txt`.

### For SafeTensors models like microsoft/Phi-3-mini-128k-instruct

1. Run the script:
   ```sh
   python sftoguff.py
   ```

2. Enter the Hugging Face model ID when prompted.

3. The script will download and convert the model to a .guff file.

4. It will ask you if want to import into ollama, and if so, it'll launch main.py


## Example

```sh
$ python main.py
Enter the Hugging Face model ID: bert-base-uncased
Available files in the repository:
1. config.json
2. pytorch_model.bin
3. vocab.txt
Enter the number of the file you want to download: 2
File 'pytorch_model.bin' already exists. Do you want to redownload it? (yes/no): no
Do you want to proceed with the 'ollama create' command? (yes/no): yes
Enter the name for the model (default: pytorch_model): my_custom_model
Model imported successfully!
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Contact

For any questions or issues, please post an issue on this repository.

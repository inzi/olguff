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

- Python 3.x
- `huggingface_hub` library
- `subprocess` module (part of Python standard library)
- `ollama` command-line tool

For sftoguff.py, you'll need llama.cpp installed and functional on your system.

## Installation

1. Install the required Python library:
   ```sh
   pip install huggingface_hub
   ```

2. Ensure you have the `ollama` command-line tool installed and properly configured.

## Usage

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

For sftoguff.py - 

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

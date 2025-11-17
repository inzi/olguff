import os
import subprocess
import webbrowser
from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import RepositoryNotFoundError, EntryNotFoundError

print(f"Current working directory: {os.getcwd()}")

llamacpp = "llama.cpp/"
llamacpp_dir = os.path.join(os.getcwd(), "llama.cpp")
llamacppconvert = os.path.join(llamacpp_dir, "convert_hf_to_gguf.py")
llamacppconvert = os.path.abspath(llamacppconvert)

if not os.path.exists(llamacppconvert):
    print(f"\nllama.cpp not found at: {llamacpp_dir}")
    print("This tool requires llama.cpp for converting SafeTensor models to GGUF format.")

    clone_repo = input("\nWould you like to clone the llama.cpp repository now? (y/[n]): ").strip().lower()
    clone_repo = clone_repo[0] if clone_repo else 'n'

    if clone_repo == 'y':
        print(f"\nCloning llama.cpp repository to {llamacpp_dir}...")
        try:
            subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", llamacpp_dir], check=True)
            print("Successfully cloned llama.cpp!")

            # Verify the converter script exists after cloning
            if not os.path.exists(llamacppconvert):
                print(f"Error: convert_hf_to_gguf.py not found after cloning.")
                print(f"Expected location: {llamacppconvert}")
                exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning llama.cpp repository: {e}")
            print("Please clone it manually: git clone https://github.com/ggerganov/llama.cpp.git")
            exit(1)
        except FileNotFoundError:
            print("Error: 'git' command not found. Please install git first.")
            print("Or clone llama.cpp manually to: " + llamacpp_dir)
            exit(1)
    else:
        print("\nTo use this tool, you need llama.cpp installed.")
        print(f"Clone it manually to: {llamacpp_dir}")
        print("Command: git clone https://github.com/ggerganov/llama.cpp.git")
        exit(1)

# Prompt the user for the model ID
model_id = input("Enter the Hugging Face model ID: ")

# Check if the model exists on Hugging Face
api = HfApi()
try:
    model_info = api.model_info(model_id)
    model_name = model_info.modelId.split("/")[-1]
except RepositoryNotFoundError:
    print(f"Model '{model_id}' not found on Hugging Face.")
    exit(1)

# Generate the local directory name from the model name
local_dir = os.path.join(os.getcwd(),"sf", model_name)
dodownload = True
if os.path.exists(local_dir):
        redownload = input(f"'{local_dir}' already exists. Do you want to redownload it? (y/[n]): ").strip().lower()
        redownload = redownload[0] if redownload else 'n'
        if redownload != 'y':
            print(f"Skipping download of '{model_name}'.")
            dodownload = False

if dodownload:
    from huggingface_hub import snapshot_download
    model_id=model_id
    snapshot_download(repo_id=model_id, local_dir=local_dir,
                    local_dir_use_symlinks=False, revision="main")

# run python llama.cpp/convert.py 
guff_folder = os.path.join(os.getcwd(),"sf", f"{model_name}-guff")
guff_folder = os.path.abspath(guff_folder)
guff_file = os.path.join(os.getcwd(),"sf", guff_folder, f"{model_name}.guff")
guff_file = os.path.abspath(guff_file)
dogulffile=True
if not os.path.exists(guff_folder):
    guff_dir = os.path.dirname(guff_file)
    print(f"Creating Guff folder: {guff_dir}")
    os.makedirs(guff_dir, exist_ok=True)

if os.path.exists(guff_file):
    regenerateguff = input(f"'{guff_file}' already exists. Do you want to recreate it? (y/[n]): ").strip().lower()
    regenerateguff = regenerateguff[0] if regenerateguff else 'n'
    if regenerateguff != 'y':
        print(f"Skipping generation of '{guff_file}'.")
        dogulffile=False

if dogulffile:
    print(f"Generating Guff file: {guff_file}")
    command = f"python {llamacppconvert} {local_dir} --outfile {guff_file}"
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)
#python llama.cpp/convert.py local_dir --outfile {model_name}.gguf --outtype q8_0
mainpy = os.path.join(os.getcwd(),"main.py")
mainpy = os.path.abspath(mainpy)
if os.path.exists(mainpy):

    proceed = input("Do you want to run import the guff file into ollama? (y/[n]]): ").strip().lower()
    proceed = proceed[0] if proceed else 'n'

    if proceed == 'y':
        print (f"GGUF file: {guff_file}")
        command = f"python {mainpy} {guff_file}"
        print (f"Running command: {command}")
        # Run the command to import the GGUF model into Ollama
        #command = f"ollama create {model_name} -f {model_name}.gguf"
        subprocess.run(command, shell=True)
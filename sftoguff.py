import os
import subprocess
import webbrowser
from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import RepositoryNotFoundError, EntryNotFoundError

print(f"Current working directory: {os.getcwd()}")
print(f"You need to ensure you have llama.cpp installed and in your PATH.")
print(f"Otherwise, set the path to your llama.cpp executable below.")

llamacpp = "llama.cpp/"

llamacppconvert = os.path.join(os.getcwd(),"llama.cpp", "convert_hf_to_gguf.py")
llamacppconvert = os.path.abspath(llamacppconvert)
if not os.path.exists(llamacppconvert):
    print("Error: convert_hf_to_gguf.py not found in llama.cpp directory.")
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
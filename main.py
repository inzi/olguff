import os
import subprocess
import webbrowser
from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import RepositoryNotFoundError, EntryNotFoundError

# Prompt the user for the model ID
model_id = input("Enter the Hugging Face model ID: ")

# Check if the model exists on Hugging Face
api = HfApi()
try:
    model_info = api.model_info(model_id)
    model_name = model_info.modelId.split("/")[-1]
    # List all files in the repository
    print("Available files in the repository:")
    files = api.list_repo_files(model_id)
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
except RepositoryNotFoundError:
    print(f"Model '{model_id}' not found on Hugging Face.")
    exit(1)

# Prompt the user to select a file to download
file_index = int(input("Enter the number of the file you want to download: ")) - 1
if file_index < 0 or file_index >= len(files):
    print("Invalid selection.")
    exit(1)
file_name = files[file_index]

# Generate the local directory name from the model name
local_dir = os.path.join(os.getcwd(), model_name)

# Create the local directory if it doesn't exist
os.makedirs(local_dir, exist_ok=True)

# Check if the file already exists
file_path = os.path.join(local_dir, file_name)
if os.path.exists(file_path):
    redownload = input(f"File '{file_name}' already exists. Do you want to redownload it? (yes/no): ").strip().lower()
    if redownload != 'yes':
        print(f"Skipping download of '{file_name}'.")
    else:
        # Download the specific model file from Hugging Face
        try:
            file_path = hf_hub_download(repo_id=model_id, filename=file_name, local_dir=local_dir)
        except EntryNotFoundError:
            print(f"File '{file_name}' not found in the repository '{model_id}'.")
            exit(1)
else:
    # Download the specific model file from Hugging Face
    try:
        file_path = hf_hub_download(repo_id=model_id, filename=file_name, local_dir=local_dir)
    except EntryNotFoundError:
        print(f"File '{file_name}' not found in the repository '{model_id}'.")
        exit(1)

# Create the metafile for Ollama
meta_file_content = f"""
## Metafile for the model
FROM {file_path}

## SYSTEM
## The system message used to specify custom behavior.
# SYSTEM You are Mario from super mario bros, acting as an assistant.

## ADAPTER 
## The ADAPTER instruction is an optional instruction that specifies any LoRA adapter that should apply to the base model. The value of this instruction should be an absolute path or a path relative to the Modelfile and the file must be in a GGML file format. The adapter should be tuned from the base model otherwise the behaviour is undefined.
# ADAPTER ./ollama-lora.bin

## LICENSE
## The LICENSE instruction allows you to specify the legal license under which the model used with this Modelfile is shared or distributed.
# LICENSE "" <license text> ""


## MESSAGE
## The MESSAGE instruction allows you to specify a message history for the model to use when responding. Use multiple iterations of the MESSAGE command to build up a conversation which will guide the model to answer in a similar way.
# MESSAGE <role> <message>

## Valid Roles: 
# user An example message of what the user could have asked.
# system An example message of what the user could have asked.
# assistant An example message of how the model should respond.

## mirostat
## Enable Mirostat sampling for controlling perplexity. (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)
# PARMETER mirostat 0

## mirostat_eta
## Influences how quickly the algorithm responds to feedback from the generated text. A lower learning rate will result in slower adjustments, while a higher learning rate will make the algorithm more responsive. (Default: 0.1)
# PARAMETER mirostat_eta 0.1

## mirostat_tau
## Controls the balance between coherence and diversity of the output. A lower value will result in more focused and coherent text. (Default: 5.0)
# PARAMETER mirostat_tau 5.0

## num_ctx
## Sets the size of the context window used to generate the next token. (Default: 2048)
# PARAMETER num_ctx 2048

## repeat_last_n
## Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)
# PARAMETER repeat_last_n 64

## repeat_penalty
## Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)
# PARAMETER repeat_penalty 1.1

## temperature
## The temperature of the model. Increasing the temperature will make the model answer more creatively. (Default: 0.8)
# PARAMETER temperature 0.8

## seed
## Sets the random number generator seed to use for generation. Setting this to a specific value will make the model generate the same text for the same prompt. (Default: 0, 0 = random)
# PARAMETER seed 0

## stop
## Sets the stop sequences to use. When generating text, the model will stop at the first occurrence of any of these strings. (Default: ["<|im_end|>"])
# PARAMETER stop ["<|im_end|>", "User:", "System:"]

## tfs_z
## Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting. (default: 1)
# PARAMETER tfs_z 1

## num_prediict
## Maximum number of tokens to predict when generating text. (Default: 128, -1 = infinite generation, -2 = fill context)
# PARAMETER num_predict 128

## top_k
## Reduces the probability of generating nonsense. A higher value (e.g. 50) will give more diverse answers, while a lower value (e.g. 10) will make answers more focused and deterministic. (Default: 40)
# PARAMETER top_k 40

## top_p
## Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)
# PARAMETER top_p 0.9

## TEMPLATE ""{{{{ if .System }}}}system {{{{ .System }}}}{{{{ end }}}}{{{{ if .Prompt }}}}user {{{{ .Prompt }}}}{{{{ end }}}}assistant {{{{ .Response }}}}""

"""

meta_file_content = meta_file_content + "\n"
meta_file_content = meta_file_content + """TEMPLATE {{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""

meta_file_path = os.path.join(local_dir, "metafile.txt")
with open(meta_file_path, "w") as meta_file:
    meta_file.write(meta_file_content)

# Ask the user if they want to proceed with the ollama create command
proceed = input("Do you want to proceed with the 'ollama create' command? (yes/no): ").strip().lower()
command = f"ollama create --meta {meta_file_path}"
if proceed == 'yes':
    default_model_name = os.path.splitext(file_name)[0]
    model_name_input = input(f"Enter the name for the model (default: {default_model_name}): ").strip()
    model_name = model_name_input if model_name_input else default_model_name
    command = f"ollama create {model_name} --file {meta_file_path}"
    subprocess.run(command, shell=True)
    print("Model imported successfully!")

else:
    print(f"To create the model manually, run the following command:\n{command}")
    print("\n")
    print(f"The metafile has been saved to {meta_file_path}. You can use it with the 'ollama create' command.\n")
    print(f"For more information on the metafile, you can refer to the following link:\nhttps://github.com/ollama/ollama/blob/main/docs/modelfile.md\n")
    print(f"Parameters can vary depending on the model and its capabilities.\n")
    print(f"To find the parameters for your chosen model, visit the model's page on Hugging Face:\nhttps://huggingface.co/models?pipeline_tag=text-generation&sort=downloads&search={model_name}\n")
    print(f"If the model is supported by other tools, such as lmstudio, you may be able to get information about its parameters from there.\n")
    print(f"To learn more about the parameters, you can refer to the following link:\nhttps://github.com/ggerganov/llama.cpp#model-parameters\n")
    # # Ask if they want to open the links in a browser
    # open_links = input("Do you want to open these links in your default web browser? (yes/no): ").strip().lower()
    # # List of URLs to open
    # urls = [
    #     "https://github.com/ollama/ollama/blob/main/docs/modelfile.md",
    #     f"https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads&search={model_name}",
    #     "https://github.com/ggerganov/llama.cpp#model-parameters"
    # ]
    # # Open the links in a browser if the user confirms
    # if open_links == 'yes':
    #     for url in urls:
    #         webbrowser.open(url)
    #         print("\n")



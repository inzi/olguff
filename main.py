import os
import subprocess
import sys

def main():
    print("=" * 60)
    print("Ollama Model Importer")
    print("=" * 60)
    print("\nThis tool helps you import Hugging Face models into Ollama.")
    print("\nWhat type of model do you want to import?")
    print("1. GGUF file (already in GGUF format)")
    print("2. SafeTensors model (will be converted to GGUF)")
    print()

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        # Run gufftoollama.py for GGUF files
        print("\n" + "=" * 60)
        print("Starting GGUF to Ollama import...")
        print("=" * 60 + "\n")

        gufftoollama = os.path.join(os.path.dirname(__file__), "gufftoollama.py")
        if os.path.exists(gufftoollama):
            # Pass any command-line arguments to gufftoollama.py
            subprocess.run([sys.executable, gufftoollama] + sys.argv[1:])
        else:
            print(f"Error: gufftoollama.py not found at {gufftoollama}")
            exit(1)

    elif choice == "2":
        # Run sftoguff.py for SafeTensors models
        print("\n" + "=" * 60)
        print("Starting SafeTensors to GGUF conversion...")
        print("=" * 60 + "\n")

        sftoguff = os.path.join(os.path.dirname(__file__), "sftoguff.py")
        if os.path.exists(sftoguff):
            subprocess.run([sys.executable, sftoguff])
        else:
            print(f"Error: sftoguff.py not found at {sftoguff}")
            exit(1)
    else:
        print("\nInvalid choice. Please run the script again and enter 1 or 2.")
        exit(1)

if __name__ == "__main__":
    main()

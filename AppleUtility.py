import os
import glob
import json
import time
import sys
import shutil

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[36m'

print(f"""{Colors.HEADER}{Colors.BOLD}Apple Utility - PBR Artist Help Tool{Colors.ENDC}""")

def loading_animation():
    animation = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    for _ in range(1):
        for frame in animation:
            sys.stdout.write(f'{Colors.OKBLUE}\r{frame}{Colors.ENDC}')
            sys.stdout.flush()
            time.sleep(0.5)

def confirm_continue():
    while True:
        choice = input(f"\n{Colors.WARNING}Do you want to save it? (y/n): {Colors.ENDC}").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            print(f"{Colors.FAIL}Exiting...{Colors.ENDC}")
            return False
        else:
            print(f"\n{Colors.FAIL}Invalid choice. Please enter 'y' or 'n'.{Colors.ENDC}")

def create_folders_and_file():
    required_folders = ["input", "mer", "heightmap", "normalmap", "JSON_files"]
    for folder in required_folders:
        os.makedirs(folder, exist_ok=True)
        print(f"{Colors.OKGREEN}Checked or created folder: {folder}{Colors.ENDC} ✓")

    if not os.path.exists("output.txt"):
        with open("output.txt", 'w') as f:
            pass  # Create an empty output.txt file
        print(f"{Colors.OKGREEN}Created output.txt file.{Colors.ENDC}")

def copy_and_rename_images(source_folder, destination_folder, suffix):
    if not os.path.exists(source_folder):
        print(f"{Colors.FAIL}Error: The folder '{source_folder}' does not exist.{Colors.ENDC}")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"{Colors.OKGREEN}Created folder: {destination_folder}{Colors.ENDC}")

    for filename in os.listdir(source_folder):
        if filename.endswith(".png"):
            new_filename = os.path.splitext(filename)[0] + suffix
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, new_filename)
            print(f"{Colors.OKBLUE}Copying '{source_path}' to '{destination_path}'{Colors.ENDC}")
            shutil.copy2(source_path, destination_path)
            print(f"{Colors.OKGREEN}Copied and renamed '{filename}' to '{new_filename}' in '{destination_folder}'{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Skipping non-PNG file: {filename}{Colors.ENDC}")

def get_image_names(folder_path):
    image_files = glob.glob(os.path.join(folder_path, '*.jpg')) + \
                  glob.glob(os.path.join(folder_path, '*.jpeg')) + \
                  glob.glob(os.path.join(folder_path, '*.png')) + \
                  glob.glob(os.path.join(folder_path, '*.gif')) + \
                  glob.glob(os.path.join(folder_path, '*.bmp')) + \
                  glob.glob(os.path.join(folder_path, '*.tif')) + \
                  glob.glob(os.path.join(folder_path, '*.tiff'))
    image_names = [os.path.basename(image_file) for image_file in image_files]
    return image_names

def write_image_names_to_file(image_names, file_path):
    with open(file_path, 'w') as file:
        for name in image_names:
            file.write(name + '\n')
    print(f"{Colors.OKGREEN}Image names have been written to {file_path}{Colors.ENDC}")

def remove_extension(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = [line.strip().replace('.png', '') for line in lines]
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')
    print(f"{Colors.OKGREEN}File extensions removed from the {file_path} file.{Colors.ENDC}")

def create_json_file_height(image_name, output_folder):
    data = {
        "format_version": "1.16.100",
        "minecraft:texture_set": {
            "color": image_name,
            "metalness_emissive_roughness": f"{image_name}_mer",
            "heightmap": f"{image_name}_heightmap"
        }
    }
    json_file_path = os.path.join(output_folder, f"{image_name}.texture_set.json")
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"{Colors.OKGREEN}JSON file created for '{image_name}'.{Colors.ENDC}")

def create_json_file_normal(image_name, output_folder):
    data = {
        "format_version": "1.16.100",
        "minecraft:texture_set": {
            "color": image_name,
            "metalness_emissive_roughness": f"{image_name}_mer",
            "normal": f"{image_name}_normal"
        }
    }
    json_file_path = os.path.join(output_folder, f"{image_name}.texture_set.json")
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"{Colors.OKGREEN}JSON file created for '{image_name}'.{Colors.ENDC}")

def process_output_file(output_file_path, output_folder):
    with open(output_file_path, 'r') as file:
        image_names = file.read().splitlines()

    print("\nSelect the type of map for the JSON files:")
    print(f"{Colors.OKBLUE}1. Height Map{Colors.ENDC}")
    print(f"{Colors.OKBLUE}2. Normal Map{Colors.ENDC}")
    map_choice = input(f"{Colors.OKGREEN}Enter your choice (1/2): {Colors.ENDC}")

    if map_choice == '1':
        for image_name in image_names:
            create_json_file_height(image_name, output_folder)
    elif map_choice == '2':
        for image_name in image_names:
            create_json_file_normal(image_name, output_folder)
    else:
        print(f"{Colors.FAIL}Invalid choice. Please select either 1 or 2.{Colors.ENDC}")
        return

    print(f"{Colors.OKGREEN}JSON files have been created.{Colors.ENDC}")

def show_help():
    help_text = f"""
    {Colors.OKGREEN}Apple Utility - PBR Artist Help Tool{Colors.ENDC}

    This program helps you create a PBR texture pack by performing the following steps:
    1. Rename images with specific suffixes ({Colors.WARNING}_mer{Colors.ENDC}, {Colors.WARNING}_heightmap{Colors.ENDC}, and {Colors.WARNING}_normal{Colors.ENDC}).
    2. Extract image names and save them to {Colors.WARNING}output.txt{Colors.ENDC}.
    3. Remove file extensions from {Colors.WARNING}output.txt{Colors.ENDC}.
    4. Create JSON files for block names based on the content of {Colors.WARNING}output.txt{Colors.ENDC}.

    {Colors.OKBLUE}Usage:{Colors.ENDC}
    1. Ensure your images are placed in the '{Colors.WARNING}input{Colors.ENDC}' folder.
    2. Run the program and follow the prompts to select the desired operations.

    {Colors.OKBLUE}Folder Structure:{Colors.ENDC}
    PBRTexturePack/
    ├── {Colors.WARNING}input/{Colors.ENDC}
    │   ├── {Colors.WARNING}[your_images.png]{Colors.ENDC}
    ├── {Colors.WARNING}mer/{Colors.ENDC}
    ├── {Colors.WARNING}heightmap/{Colors.ENDC}
    ├── {Colors.WARNING}normalmap/{Colors.ENDC}
    ├── {Colors.WARNING}output.txt{Colors.ENDC}
    ├── {Colors.WARNING}JSON_files/{Colors.ENDC}
    └── {Colors.WARNING}script.py{Colors.ENDC}

    {Colors.OKBLUE}Options:{Colors.ENDC}
    1. Copy and rename images with {Colors.WARNING}_mer{Colors.ENDC} suffix.
    2. Copy and rename images with {Colors.WARNING}_heightmap{Colors.ENDC} suffix.
    3. Copy and rename images with {Colors.WARNING}_normal{Colors.ENDC} suffix.
    4. Extract image names to {Colors.WARNING}output.txt{Colors.ENDC}.
    5. Remove .png extension from {Colors.WARNING}output.txt{Colors.ENDC}.
    6. Create JSON files from {Colors.WARNING}output.txt{Colors.ENDC}.
    7. Show help.
    8. Exit.

    {Colors.OKBLUE}Example:{Colors.ENDC}
    python script.py

    {Colors.CYAN}Author: 0x4a4b{Colors.ENDC}
    """
    print(help_text)



def main():
    create_folders_and_file()

    while True:
        print("\nSelect an option:")
        print(f"{Colors.OKBLUE}1. Copy and rename images with _mer suffix{Colors.ENDC}")
        print(f"{Colors.OKBLUE}2. Copy and rename images with _heightmap suffix{Colors.ENDC}")
        print(f"{Colors.OKBLUE}3. Copy and rename images with _normal suffix{Colors.ENDC}")
        print(f"{Colors.OKBLUE}4. Extract image names to output.txt{Colors.ENDC}")
        print(f"{Colors.OKBLUE}5. Remove .png extension from output.txt{Colors.ENDC}")
        print(f"{Colors.OKBLUE}6. Create JSON files from output.txt{Colors.ENDC}")
        print(f"{Colors.OKBLUE}7. Show help{Colors.ENDC}")
        print(f"{Colors.OKBLUE}8. Exit{Colors.ENDC}")

        choice = input(f"{Colors.HEADER}{Colors.BOLD}Apple Utility ~ $ {Colors.ENDC}{Colors.ENDC} {Colors.OKGREEN}Enter your choice (1-8): {Colors.ENDC}")

        if choice == '1':
            loading_animation()
            if confirm_continue():
                source_folder = "input"
                destination_folder = "mer"
                copy_and_rename_images(source_folder, destination_folder, "_mer.png")
        elif choice == '2':
            loading_animation()
            if confirm_continue():
                source_folder = "input"
                destination_folder = "heightmap"
                copy_and_rename_images(source_folder, destination_folder, "_heightmap.png")
        elif choice == '3':
            loading_animation()
            if confirm_continue():
                source_folder = "input"
                destination_folder = "normalmap"
                copy_and_rename_images(source_folder, destination_folder, "_normal.png")
        elif choice == '4':
            loading_animation()
            if confirm_continue():
                image_names = get_image_names('input')
                write_image_names_to_file(image_names, 'output.txt')
        elif choice == '5':
            loading_animation()
            if confirm_continue():
                remove_extension('output.txt')
        elif choice == '6':
            loading_animation()
            if confirm_continue():
                output_folder = 'JSON_files'
                process_output_file('output.txt', output_folder)
        elif choice == '7':
            show_help()
        elif choice == '8':
            print(f"{Colors.FAIL}Exiting...{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}Invalid choice. Please select a valid option.{Colors.ENDC}")

if __name__ == "__main__":
    main()
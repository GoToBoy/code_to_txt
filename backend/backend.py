import os

def compress_spaces(content):
    # Remove extra spaces and tabs
    compressed_content = ' '.join(content.split())
    return compressed_content

def read_files_in_directory(directory_path, output_file_path,extensions, prefix='', ignore_folders=None, ignore_filetypes=None ):
    ignore_folders = ignore_folders or []
    with open(output_file_path, 'a', encoding='utf-8', errors='ignore') as output_file:
        for root, dirs, files in os.walk(directory_path):
            if any(ignore_folder in root for ignore_folder in ignore_folders):
                print(f"Skipping directory: {root}")
                continue  # Skip processing files in "libs\echarts" directory
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if any(ignore_filetype in file_name for ignore_filetype in ignore_filetypes):
                    print(f"Skipping file: {file_path}")
                    continue  # Skip processing files with certain file extensions
                else:
                    # if file_path.endswith(extensions):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as input_file:
                            file_content = input_file.read()
                            compressed_content = compress_spaces(file_content)
                            output_file.write(f"{prefix}{file_path}:\n")
                            output_file.write(compressed_content)
                            output_file.write('\n')
                    except UnicodeDecodeError:
                        print(f"Error reading file: {file_path}. Skipping.")
                        continue

def generate_file_tree(directory_path, output_file_path,project_name):
    with open(output_file_path, 'w',encoding='utf-8') as output_file:
        output_file.write(f"{project_name}:\n")
        for root, dirs, files in os.walk(directory_path):
            level = root.replace(directory_path, '').count(os.sep)
            indent = '  ' * (level - 1)
            output_file.write(f"{indent}+ {os.path.basename(root)}/\n")
            sub_indent = '  ' * level
            for file_name in files:
                output_file.write(f"{sub_indent}- {file_name}\n")

src_directory = '../../lachesis/iron_service/pharmacy_service'
output_file_path = './pharmacy_service.txt'   
project_name = 'pharmacy_service'

#  frontend
# extensions_to_read = ['.js', '.ts', '.tsx', '.jsx', '.vue'] 
# ignore_folders = ["libs\\echarts", "libs\\gojs"] 
# generate_file_tree(src_directory, output_file_path,project_name)
# read_files_in_directory(src_directory, output_file_path,extensions_to_read, prefix='// file path: ', ignore_folders=ignore_folders)

#  backend
ignore_folders = ["src\\main\\resources","src\\main\\webapp","dao",
                  "src\\main\\java\\com\\iron\\fast\\reflect",
                  "utils",
                  "beans",
                  "module",
                  "tempuri2",
                  "iron\\fast\\property",
                  "iron\\fast\\util",
                  "iron\\fast\\mongo",
                  "fast\\repository\\dialect",
                  "pharmacy_service\\fast-repository\\src\\main\\java\\com\\iron\\fast\\repositor",
                  "pharmacy_service\\fast-core\\src\\main\\java\\com\\iron\\fast\\log"]
ignore_filetypes = ['bat','xml','iml','log','data','lock','properties']

generate_file_tree(src_directory, output_file_path,project_name)
read_files_in_directory(src_directory, output_file_path,extensions=(), prefix='// path:', ignore_folders=ignore_folders,ignore_filetypes=ignore_filetypes)

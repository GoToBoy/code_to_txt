import os
import re

def compress_spaces(content):
    # Remove extra spaces and tabs
    compressed_content = ' '.join(content.split())
    return compressed_content

def read_files_in_directory(directory_path, output_file_path,extensions, prefix='', ignore_folders=None ):
    ignore_folders = ignore_folders or []
    with open(output_file_path, 'a', encoding='utf-8', errors='ignore') as output_file:
        for root, dirs, files in os.walk(directory_path):
            if any(ignore_folder in root for ignore_folder in ignore_folders):
                continue  # Skip processing files in "libs\echarts" directory
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_path.endswith(tuple(extensions)):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as input_file:
                            file_lines = input_file.readlines()
                            filtered_lines = filter_comments(file_lines)
                            filtered_content = ''.join(filtered_lines)
                            filtered_content = filter_using_statements(filtered_content)
                            if not filtered_content.strip():  # Check if content is empty after filtering
                                print(f"Filtered file: {file_path}. Skipping.")
                                continue  # Skip file if content is empty
                            compressed_content = compress_spaces(filtered_content)
                            output_file.write(f"{prefix}{file_path.replace(directory_path,'')}:\n")
                            output_file.write(compressed_content)
                            output_file.write('\n')
                    except UnicodeDecodeError:
                        print(f"Error reading file: {file_path}. Skipping.")
                        continue

def filter_comments(lines):
    filtered_lines = []
    for line in lines:
        # Remove // comments
        line_without_comments = re.sub(r'//.*', '', line)
        filtered_lines.append(line_without_comments)
    return filtered_lines

def filter_using_statements(content):
    # Use regular expression to remove 'using' statements
    pattern = r'^.*?(\bnamespace\b)'
    return re.sub(pattern, r'\1', content, flags=re.DOTALL)

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

src_directory = '../../lachesis/iron_client/pis_client'
output_file_path = './pis_client.txt'   
project_name = 'pis_client'
extensions_to_read = ['.cs', '.txt'] 
ignore_folders = ["obj\\Debug","logs","Themes","Demo","Binary\\Debug","Properties"] 

generate_file_tree(src_directory, output_file_path,project_name)
read_files_in_directory(src_directory, output_file_path,extensions_to_read, prefix='// path: ', ignore_folders=ignore_folders)

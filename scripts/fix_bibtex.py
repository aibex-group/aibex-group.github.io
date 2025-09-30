import os
import re

def fix_author_field(author_str):
    # Replace ', and' or ',and' with ' and' to normalize
    author_str = re.sub(r',\s*and\s*', ' and ', author_str)

    # Split the string into parts using ',' as separator
    parts = [p.strip() for p in author_str.split(',')]

    # Rejoin using ' and '
    return ' and '.join(parts)

def process_bib_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_author = False
    buffer = ''
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith('author ='):
            in_author = True
            buffer = line
            if '}' in line:
                # Single-line author field
                content = re.search(r'{(.*)}', line).group(1)
                fixed = fix_author_field(content)
                new_line = re.sub(r'{.*}', '{' + fixed + '}', line)
                new_lines.append(new_line)
                in_author = False
            continue

        if in_author:
            buffer += line
            if '}' in line:
                # End of multi-line author field
                content = re.search(r'{(.*)}', buffer, re.DOTALL).group(1)
                fixed = fix_author_field(content)
                new_line = re.sub(r'{.*}', '{' + fixed + '}', buffer, flags=re.DOTALL)
                new_lines.append(new_line)
                in_author = False
            continue

        new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.bib'):
                full_path = os.path.join(root, filename)
                print(f'Processing: {full_path}')
                process_bib_file(full_path)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Fix author fields in .bib files.")
    parser.add_argument('directory', help='Directory containing .bib files')

    args = parser.parse_args()
    process_directory(args.directory)

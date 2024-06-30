import os
import sys
import json
from collections import Counter

def extract_tuple_from_line(line):
    # Regex pattern to match the format: 1. **Alexandra (Werewolf) (Fake Claim):**
    try:
        l = line.split(':')[0].split('*')[-1]
        name, role, lie_type = l.split('(')
        player = name.strip()
        role = role.split(')')[0].strip()
        claim_type = lie_type.split(')')[0].strip()
        return (role, claim_type)
    except ValueError:
        return None

def parse_markdown(markdown_lines):
    l = []
    try:
        try:
            index = markdown_lines.index('# DECEPTION:\n')
        except ValueError:
            index = markdown_lines.index('## DECEPTION:\n')
    except ValueError:
        return(l)
    markdown_lines = markdown_lines[index+1:]
    for line in markdown_lines:
        if extract_tuple_from_line(line):
            l.append(extract_tuple_from_line(line))
    return(l)

def main():
    file_names = []
    path = sys.argv[1]
    for file in os.listdir(path):
        if file.endswith('.md'):
            file_names.append(file)
    agg = []
    for file_name in file_names:
        with open(f'{path}/{file_name}', 'r') as file:
            markdown_content = file.readlines()
            markdown_content = [line for line in markdown_content if line.strip() != '']
            agg.extend(parse_markdown(markdown_content))
    
    d = {}
    for role, claim_type in agg:
        if role not in d:
            d[role] = {}
        if claim_type not in d[role]:
            d[role][claim_type] = 0
        d[role][claim_type] += 1
    
    output_path = sys.argv[2]
    with open(output_path, 'w') as file:
        json.dump(d, file, indent=4)

if __name__ == '__main__':
    main()


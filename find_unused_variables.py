import yaml
import os
import re

def load_yaml_file(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def find_used_variables_in_templates(template_dir):
    used_variables = set()
    pattern = re.compile(r'\.Values\.([a-zA-Z0-9_\.]+)')
    for root, _, files in os.walk(template_dir):
        for filename in files:
            if filename.endswith('.yaml') or filename.endswith('.tpl'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r') as file:
                    content = file.read()
                    matches = pattern.findall(content)
                    used_variables.update(matches)
    return used_variables

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def main():
    values_file = 'values.yaml'
    templates_dir = 'templates'
    
    values = load_yaml_file(values_file)
    used_variables = find_used_variables_in_templates(templates_dir)

    flattened_values = flatten_dict(values)
    defined_variables = set(flattened_values.keys())

    unused_variables = defined_variables - used_variables

    print("Defined variables:", defined_variables)
    print("Used variables:", used_variables)
    print("Unused variables:", unused_variables)

if __name__ == "__main__":
    main()
  

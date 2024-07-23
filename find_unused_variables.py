import os
import yaml

def load_yaml_file(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def find_used_variables_in_templates(templates_dir):
    used_variables = set()
    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".yaml"):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    used_variables.update(set(var for var in content.split() if var.startswith(".Values.")))
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
    charts_dir = 'charts'
    for root, _, files in os.walk(charts_dir):
        if 'values.yaml' in files:
            values_file = os.path.join(root, 'values.yaml')
            templates_dir = os.path.join(root, 'templates')
            if os.path.isdir(templates_dir):
                values = load_yaml_file(values_file)
                used_variables = find_used_variables_in_templates(templates_dir)

                flattened_values = flatten_dict(values)
                defined_variables = set(flattened_values.keys())

                unused_variables = defined_variables - used_variables

                print(f"Chart: {os.path.basename(root)}")
                print("Defined variables:", defined_variables)
                print("Used variables:", used_variables)
                print("Unused variables:", unused_variables)
                print("")

if __name__ == "__main__":
    main()

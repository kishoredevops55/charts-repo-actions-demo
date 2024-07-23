import os
import yaml

def load_yaml_file(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def find_unused_variables(values, used_variables, parent_key=''):
    unused_vars = []
    for key, value in values.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            unused_vars.extend(find_unused_variables(value, used_variables, full_key))
        elif full_key not in used_variables:
            unused_vars.append(full_key)
    return unused_vars

def parse_templates_for_variables(template_dir):
    used_variables = set()
    for root, _, files in os.walk(template_dir):
        for file in files:
            if file.endswith(('.yaml', '.tpl')):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    for line in content.splitlines():
                        if "{{ .Values." in line:
                            start = line.find("{{ .Values.") + 10
                            end = line.find("}}", start)
                            var_path = line[start:end].strip()
                            used_variables.add(var_path.split()[0])
    return used_variables

def main():
    chart_dir = 'charts'
    for root, _, files in os.walk(chart_dir):
        if 'values.yaml' in files:
            values_file = os.path.join(root, 'values.yaml')
            template_dir = os.path.join(root, 'templates')

            values = load_yaml_file(values_file)
            used_variables = parse_templates_for_variables(template_dir)
            unused_vars = find_unused_variables(values, used_variables)

            if unused_vars:
                print(f"Unused variables in {values_file}:")
                for var in unused_vars:
                    print(f"  - {var}")
            else:
                print(f"No unused variables found in {values_file}")

if __name__ == "__main__":
    main()

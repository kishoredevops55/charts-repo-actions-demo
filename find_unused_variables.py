import os
import yaml

class LineNumberLoader(yaml.Loader):
    def __init__(self, stream):
        super().__init__(stream)
        self.line_numbers = {}

    def construct_mapping(self, node, mapping=None, **kwargs):
        if mapping is None:
            mapping = super().construct_mapping(node, **kwargs)
        if node.start_mark:
            self.line_numbers[node.start_mark.line] = node
        return mapping

def load_yaml_file(filepath):
    try:
        with open(filepath, 'r') as file:
            loader = LineNumberLoader(file)
            data = yaml.load(file, Loader=LineNumberLoader)
            return data, loader.line_numbers
    except Exception as e:
        print(f"Error loading YAML file {filepath}: {e}")
        return None, {}

def find_unused_variables(values, used_variables, parent_key='', line_numbers=None):
    if values is None:
        return []
        
    unused_vars = []
    for key, value in values.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            unused_vars.extend(find_unused_variables(value, used_variables, full_key, line_numbers))
        elif full_key not in used_variables:
            line = line_numbers.get(full_key, 'unknown') if line_numbers else 'unknown'
            unused_vars.append((full_key, line))
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

            values, line_numbers = load_yaml_file(values_file)
            used_variables = parse_templates_for_variables(template_dir)

            print(f"Used Variables in {values_file}: {used_variables}")  # Debug output
            unused_vars = find_unused_variables(values, used_variables, line_numbers=line_numbers)

            if unused_vars:
                print(f"Unused variables in {values_file}:")
                for var, line in unused_vars:
                    print(f"  - {var} (line {line})")
            else:
                print(f"No unused variables found in {values_file}")

if __name__ == "__main__":
    main()
    

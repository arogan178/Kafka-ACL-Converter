import yaml
import glob
import os

class OrderedDumper(yaml.SafeDumper):
    def _dict_representer(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data.items())

OrderedDumper.add_representer(dict, OrderedDumper._dict_representer)

def merge_operations_by_resource(yaml_file):
    """
    Merge operations by resource in the given YAML file.

    Args:
        yaml_file (str): The path to the YAML file.

    Returns:
        dict: The modified data with merged operations.
    """
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    if 'authorization' not in data.get('spec', {}):
        return None

    merged_items = {}
    for item in data['spec']['authorization']['acls']:
        if 'operation' not in item:
            print(f"Skipping item {item} because it doesn't have an 'operation' File: {os.path.basename(yaml_file)}")
            return None  # skip this item if it doesn't have an 'operation' key

        resource = item['resource']
        resource_name = resource['name']
        resource_type = resource['type']
        resource_key = f"{resource_name}_{resource_type}"

        if resource_key in merged_items:
            merged_items[resource_key]['operations'].append(item['operation'])
        else:
            merged_items[resource_key] = {
                'resource': resource,
                'operations': [item['operation']]
            }

    merged_operations = list(merged_items.values())
    data['spec']['authorization']['acls'] = merged_operations
    return data



path ='<PATH TO FILE>/*.yaml'


for file in glob.glob(path):
    print(f"Processing file: {file}")
    with open(file, 'r') as f:
        original_data = yaml.safe_load(f)
    merged_data = merge_operations_by_resource(file)
    
    output_filename = os.path.basename(file)

    # Point to local directory to test
    if merged_data is None:
        print(f"Skipping file {file} because it doesn't have an 'operation' key")
        continue
    else:
        with open(file, 'w') as file:
            yaml.dump(merged_data, file, Dumper=OrderedDumper)

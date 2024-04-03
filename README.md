# Kafka User ACL Converter (Strimzi 0.30 Migration Tool)
This script converts Kafka user ACL YAML files to a format where operations are merged by resource. This addresses a change introduced in Kafka Strimzi 0.30, where the YAML format for ACLs no longer requires separate entries for each operation on a resource. This script helps migrate your existing ACL configurations to the new format.

## How it Works
(The functionality remains the same as before)

The script iterates through all YAML files in the specified directory (<PATH TO FILE>/*.yaml).
For each file, it reads the YAML content and checks if the authorization.acls section exists.

If the authorization.acls section exists, it iterates through each ACL entry.
If an ACL entry doesn't have an operation key, the script prints a warning message and skips processing that entry.
Otherwise, it extracts the resource name and type from the ACL entry and creates a unique key by combining them (e.g., topic_test).

The script then merges operations for the same resource. If an entry for the resource key already exists, the operation is appended to the list of operations for that resource. Otherwise, a new entry is created with the resource information and a list containing the operation.

Finally, the script overwrites the original YAML file with the modified data, where ACL entries have merged operations by resource.
Note: If a file doesn't have any ACL entries with the operation key, the entire file is skipped.

## Usage

- Replace <PATH TO FILE> with the actual path to the directory containing your Kafka user ACL YAML files.
- Save the script as a Python file (e.g., kafka_acl_converter.py).
- Run the script from your terminal:

```
python kafka_acl_converter.py
```

This will process all YAML files in the specified directory and convert them to the new format compatible with Kafka Strimzi 0.30.

## Dependencies
Python 3
PyYAML library: You can install it using pip install pyyaml.

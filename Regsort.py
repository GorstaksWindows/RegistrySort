def read_registry_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def parse_registry_entries(lines):
    parsed_entries = {}
    current_key = None

    for line in lines:
        line = line.strip()
        if line.startswith("["):
            current_key = line
            if current_key not in parsed_entries:
                parsed_entries[current_key] = []
        elif current_key:
            parsed_entries[current_key].append(line)

    return parsed_entries

def sort_and_combine_entries(parsed_entries):
    sorted_combined_entries = {}

    for key, entries in parsed_entries.items():
        if key.startswith("[["):
            continue  # Skip sections starting with [[
        current_dict = sorted_combined_entries
        key_parts = key[1:-1].split("][")
        for part in key_parts:
            current_dict = current_dict.setdefault(part, {})

        for entry in entries:
            entry_parts = entry.split("=")
            if len(entry_parts) == 2:
                current_dict[entry_parts[0]] = entry_parts[1]

    # Remove empty dictionaries
    def remove_empty_dicts(d):
        keys_to_delete = [key for key, value in d.items() if isinstance(value, dict) and not value]
        for key in keys_to_delete:
            del d[key]
        for value in d.values():
            if isinstance(value, dict):
                remove_empty_dicts(value)
    
    remove_empty_dicts(sorted_combined_entries)

    return sorted_combined_entries

def write_registry_file(sorted_entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        write_entries(file, sorted_entries)

def write_entries(file, entries, depth=0):
    for key, value in entries.items():
        if isinstance(value, dict):
            if value:  # Only write non-empty sections
                file.write(f"[{key}]\n")
                write_entries(file, value, depth + 1)
                file.write("\n")  # Add a new line after each section
        else:
            file.write(f"{key}={value}\n")

# Example usage
file_path = 'C:\\Users\\Gorstak\\Documents\\GSecurity.reg'
output_file = 'C:\\Users\\Gorstak\\Documents\\GSecurity_sorted.reg'

lines = read_registry_file(file_path)
parsed_entries = parse_registry_entries(lines)
sorted_combined_entries = sort_and_combine_entries(parsed_entries)
write_registry_file(sorted_combined_entries, output_file)

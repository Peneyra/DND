import json

def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found. Make sure the file path is correct.")
        return None

def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def display_data(data):
    """Display data at the current navigation level."""
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")  # Simplified display to show actual values
    elif isinstance(data, list):
        for index, item in enumerate(data):
            print(f"{index}: {item}")
    else:
        print(data)

def navigate_data(data, path, selection):
    """Navigate through data based on selection and update path."""
    if isinstance(data, dict) and selection in data:
        path.append(selection)
    elif isinstance(data, list) and selection.isdigit() and int(selection) < len(data):
        path.append(int(selection))
    else:
        print("Invalid selection.")

def edit_data(data, path, input_value=None):
    """Edit data at a specific path with an option to specify new value directly."""
    for key in path[:-1]:
        data = data[key]
    last_key = path[-1]

    if input_value is None:
        new_value = input(f"Enter new value for {last_key} or type 'cancel' to exit editing: ")
        if new_value.lower() == 'cancel':
            print("Editing canceled.")
            return
    else:
        new_value = input_value

    data[last_key] = new_value

def add_data(data, path):
    """Add a new key/value pair at the current navigation level."""
    if isinstance(data, dict):
        for key in path:
            data = data[key]
        new_key = input("Enter the key for the new data: ")
        new_value = input("Enter the value for the new data: ")
        data[new_key] = new_value
        print("Data added.")
    else:
        print("Adding data is only supported at dictionary levels.")

clipboard = {}

def copy_data(data, path):
    """Copy a key/value pair to clipboard."""
    for key in path[:-1]:
        data = data[key]
    last_key = path[-1]
    clipboard['key'] = last_key
    clipboard['value'] = data[last_key]
    print(f"Copied '{last_key}': '{data[last_key]}'")

def paste_data(data, path):
    """Paste a copied key/value pair at the current navigation level."""
    if 'key' in clipboard:
        for key in path:
            data = data[key]
        data[clipboard['key']] = clipboard['value']
        print(f"Pasted '{clipboard['key']}': '{clipboard['value']}'")
    else:
        print("No data in clipboard.")

def main():
    filename = input("Enter the path to the JSON file: ")
    data = load_data(filename)
    if data is None:
        return  # Exit if no data loaded

    path = []

    while True:
        print("\nCurrent location: ", " -> ".join(map(str, path)) if path else "ROOT")
        current_data = data
        for p in path:
            current_data = current_data[p]
        display_data(current_data)

        print("\nOptions:")
        print("1. Navigate [key/index]")
        print("2. Edit current [new value]")
        print("3. Add new key/value")
        print("4. Copy current key/value")
        print("5. Paste key/value here")
        print("6. Save and Exit")
        print("7. Discard Changes and Exit")
        choice = input("Enter your choice (e.g., '1 key', '2 value'): ")

        if choice.startswith('1 '):
            _, selection = choice.split(maxsplit=1)
            navigate_data(current_data, path, selection)
        elif choice.startswith('2 '):
            _, new_value = choice.split(maxsplit=1)
            if path:
                edit_data(data, path, new_value)
            else:
                print("Cannot edit root directly.")
        elif choice == '3':
            if path:
                add_data(data, path)
            else:
                print("Cannot add at the root level.")
        elif choice == '4':
            if path:
                copy_data(data, path)
            else:
                print("No key/value selected to copy.")
        elif choice == '5':
            if path:
                paste_data(data, path)
            else:
                print("Cannot paste at the root level.")
        elif choice == '6':
            save_data(filename, data)
            print("Changes saved. Exiting program.")
            break
        elif choice == '7':
            print("Changes discarded. Exiting program.")
            break
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()

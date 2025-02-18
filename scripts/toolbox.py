import json
import os

class Toolbox:

    @staticmethod
    def print_dict(data):
        print(json.dumps(data, indent=4))

    @staticmethod
    def save_to_json(obj, filename):
        """Saves an object with a to_dict() method to a JSON file."""
        with open(filename, "w") as f:
            json.dump(obj.to_dict(), f, indent=4)

    @staticmethod
    def load_obj_from_json(obj, filename):
        """Loads a JSON file and reconstructs a Portfolio object."""
        with open(filename, "r") as f:
            data = json.load(f)
        return obj.from_dict(data)

    @staticmethod
    def is_json_file_empty(filename):
        """Checks if a JSON file is empty or contains only whitespace."""
        with open(filename, "r") as f:
            content = f.read().strip()
            return len(content) == 0
        



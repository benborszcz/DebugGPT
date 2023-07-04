# Importing the required modules and classes
from .function import Function
import os

# Defining a class EditFile which inherits from the Function class
class EditFile(Function):

    # Initialising the class with the required attributes
    def __init__(self):
        self.name="edit_file"
        self.description="allows for the editing of files"
        self.parameters={
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "name of the file",
                },
                "new_contents": {
                    "type": "string",
                    "description": "new contents of the file, you must write the entire file",
                },
            },
            "required": ["file", "new_contents"],
        }
        # Calling the parent class's __init__ method
        super().__init__(self.name, self.description, self.parameters)       

    # Defining a method to process the instruction
    def process_instruction(self, function_args) -> str:
        # Getting the file name and new contents from the function arguments
        file = function_args.get('file')
        new_contents = function_args.get('new_contents')

        # Checking if the file exists
        if not os.path.exists(file):
            return f"File {file} does not exist."

        try:
            # Opening the file in write mode and writing the new contents
            with open(file, 'w') as f:
                f.write(new_contents)

            # Deleting the specific .pyc file in __pycache__ if it exists
            pycache_file = os.path.join(os.path.dirname(file), "__pycache__", os.path.basename(file).split('.')[0] + ".cpython-XX.pyc")
            # Replacing XX with the current python version
            pycache_file = pycache_file.replace("XX", str(os.sys.version_info.major) + str(os.sys.version_info.minor))
            # Checking if the pycache file exists and removing it
            if os.path.exists(pycache_file):
                os.remove(pycache_file)

            # Returning a success message
            return f"File {file} has been successfully edited and associated .pyc file deleted."
        except Exception as e:
            # Returning an error message in case of an exception
            return "Error: "+str(e)
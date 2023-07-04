# Importing the required modules and classes
from .function import Function
import os

# Defining a class GetFiles which inherits from the Function class
class GetFiles(Function):

    # Initialising the class with the required attributes
    def __init__(self):
        self.name="get_files"
        self.description="Gets the files asked for"
        self.parameters={
            "type": "object",
            "properties": {
                "files": {
                    "type": "string",
                    "description": "names of the files required, separated by spaces.",
                }
            },
            "required": ["files"],
        }
        # Calling the parent class's __init__ method
        super().__init__(self.name, self.description, self.parameters)       

    # Defining a method to process the instruction
    def process_instruction(self, function_args) -> str:
        # Getting the file names from the function arguments and splitting them into a list
        files = function_args.get('files', "").split()
        result = ""

        # Looping through each file
        for file in files:
            # Checking if the file exists
            if os.path.exists(file):
                # Opening the file in read mode and reading its contents
                with open(file, 'r') as f:
                    content = f.read()
                # Adding the file name and its contents to the result string
                result += f"# {file}\n```{file.split('.')[-1]}\n{content}\n```\n\n"
            else:
                # If the file does not exist, adding a file not found message to the result string
                result += f"# {file}\n```File not found```\n\n"

        # Returning the result string
        return result

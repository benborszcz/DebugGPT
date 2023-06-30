from function import Function
import os

class EditFile(Function):

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
        super().__init__(self.name, self.description, self.parameters)       


    def process_instruction(self, function_args) -> str:
        file = function_args.get('file')
        new_contents = function_args.get('new_contents')

        if not os.path.exists(file):
            return f"File {file} does not exist."

        try:
            with open(file, 'w') as f:
                f.write(new_contents)
            return f"File {file} has been successfully edited."
        except Exception as e:
            return "Error: "+str(e)
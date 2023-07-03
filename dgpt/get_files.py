from .function import Function
import os

class GetFiles(Function):

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
        super().__init__(self.name, self.description, self.parameters)       


    def process_instruction(self, function_args) -> str:
        files = function_args.get('files', "").split()
        result = ""

        for file in files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    content = f.read()
                result += f"# {file}\n```{file.split('.')[-1]}\n{content}\n```\n\n"
            else:
                result += f"# {file}\n```File not found```\n\n"

        return result



from function import Function
import os

class GetFiles(Function):

    def __init__(self):
        self.name="get_files"
        self.description="Gets the files asked for"
        self.parameters={
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "name of the file required",
                }
            },
            "required": ["file"],
        }
        super().__init__(self.name, self.description, self.parameters)       


    def process_instruction(self, function_args) -> str:
        file = function_args.get('file', "")
        result = ""

        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
            result += f"# {file}\n```{file.split('.')[-1]}\n{content}\n```\n\n"
        else:
            result += f"# {file}\n```File not found```\n\n"

        return result


    """
    def process_instruction(self, **kwargs) -> str:
        files = kwargs.get('file', [])
        result = ""

        for file in files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    content = f.read()
                result += f"# {file}\n```{file.split('.')[-1]}\n{content}\n```\n\n"
            else:
                result += f"# {file}\n```File not found```\n\n"

        return result
    """

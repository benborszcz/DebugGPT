from abc import ABC, abstractmethod

class Function(ABC):

    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
        
    @abstractmethod
    def process_instruction(self, function_args) -> str:
        pass
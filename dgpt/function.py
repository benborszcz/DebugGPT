# Importing necessary modules from abc
from abc import ABC, abstractmethod

# Creating an abstract base class named Function
class Function(ABC):

    # Initialising the class with name, description and parameters
    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    # Method to convert the class attributes to a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
        
    # Abstract method that needs to be implemented in any child class
    # This method is supposed to process instructions based on function arguments
    @abstractmethod
    def process_instruction(self, function_args) -> str:
        pass
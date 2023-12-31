# Import necessary modules and classes
from .agent import Agent
from .get_files import GetFiles
from .edit_file import EditFile


# Define the AgentManager class
class AgentManager:
    # Initialize the AgentManager with a dictionary of agents
    def __init__(self):
        self.agents = {
            "Chat": Agent("Chat"),
            "ErrorAnalysis": Agent("ErrorAnalysis", "You analyze programming error codes, identify the files invloved, and explain the error in natural language."),
            "FileRequester": Agent("FileRequester", "Given a natural language representation of a programming error code, you: request the necessary files to read to solve the error. You will be able to request multiple files in multiple steps.", functions=[GetFiles()]),
            "StepPlanner": Agent("StepPlanner", "Given a natural language representation of a programming error code and the necessary files to read, you give a step by step plan to solve the problem. The plan you are giving is to another language model that has access to edit files. It does not run code. It can edit a file by calling the tool edit_file(file, new_contents), where the new_contents are the entirety of the files contents with the error fixed. That is the ONLY thing it has access to. Solve it in the simplest way possible. The instructions should be verbal, not code."),
            "CodeModifier": Agent("CodeModifier", "Given a natural language representation of a programming error code, the necessary files, and a step by step plan to fix the error, you follow the steps and generate the necessary code to solve the problem. Generate all of the contents of the file, do not remove comments. You can only call the functions provided", functions=[EditFile()]),
            "ErrorComparison": Agent("ErrorComparison", "Given two errors, you compare them and see if progress was made in debugging."),
            "ProgressIdentifier": Agent("ProgressIdentifier", "Given a passage comparing two errors to see if progress was made identify if it was, respond 't' for yes and 'f' for no. Do NOT generate any other characters."),
            "Summarizer": Agent("Summarizer", "Given a process of degugging code you summarize what happened in 2 sentences, cover what was wrong and what was changed. Do not mention the new error, ONLY explain the old one and how it was fixed. Do this as concisely as possible."),
            "Revert": Agent("Revert")
        }

    # Generate a response using the specified agent
    def generate(self, agent_id: str, messages: list = None, model='gpt-3.5-turbo'):
        if messages == None : messages = []

        # Call the generate method of the specified agent
        response = self.agents[agent_id].generate(messages=messages, model=model)

        # Extract the response message from the response
        response_message = response['choices'][0]['message']['content']
        return response_message
# Import necessary modules
from .script_runner import ScriptRunner
from .agent_manager import AgentManager
from .change_logger import ChangeLogger
from rich.console import Console
from rich.traceback import install
import inquirer
import sys
import pathspec
import os

# Install traceback for rich library
install()

# Create a console object for rich library
console = Console()

# Create an agent manager object
manager = AgentManager()

def read_gitignore(folder_path):
    gitignore_path = os.path.join(folder_path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            return gitignore_file.read().splitlines()
    return []

def visualize_file_structure(folder_path, ignore_gitignored=False):
    gitignore_patterns = read_gitignore(folder_path) if ignore_gitignored else []
    spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore_patterns)

    output = []

    def _visualize_directory(root, prefix=''):
        nonlocal spec
        for name in os.listdir(root):
            file_path = os.path.join(root, name)
            if ignore_gitignored:
                if spec.match_file(file_path) or name in {".gitignore", ".gcloudignore", ".git"}:
                    print(f"{file_path} Skipped")
                    continue

            if os.path.isfile(file_path):
                output.append(f"{prefix}|---{name}\n")
            elif os.path.isdir(file_path):
                output.append(f"{prefix}+---{name}\n")
                _visualize_directory(file_path, prefix=prefix + '|   ')

    output.append(f"{os.path.basename(folder_path)}\n")
    _visualize_directory(folder_path)

    return ''.join(output)

# Define a function to debug a script
def debug_script(script):
    # Create a change logger object
    change_logger = ChangeLogger(os.path.dirname(os.path.abspath(script)))
    # Create a script runner object
    runner = ScriptRunner(script)
    console.print(f"-----Running {script}-----", style="bold blue")
    # Run the script and get the status and output
    status, output = runner.run_script()
    console.print(output)
    # If the script run status is not successful
    if not status:
        console.print("-----Analyzing Output-----", style="bold blue")
        # Generate error analysis output
        error_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":output}])
        console.print(error_analysis_output, style="bold red")
        console.print("-----Requesting Files-----", style="bold blue")
        # Generate file getter output
        file_getter_output = manager.generate("FileRequester", [{"role":"user","content":str(error_analysis_output)+"\n\n"+str(visualize_file_structure(os.getcwd()))}])
        console.print(file_getter_output, style="bold green")
        console.print("-----Planning Solution-----", style="bold blue")
        # Generate step planner output
        step_planner_output = manager.generate("StepPlanner", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output))}])
        console.print(step_planner_output, style="bold green")
        console.print("-----Editing Files-----", style="bold blue")
        # Generate code modifier output
        code_modifier_output = manager.generate("CodeModifier", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output)+"\n\n"+str(step_planner_output))}])
        console.print(code_modifier_output, style="bold green")
        change_logger.check_changes()
        console.print(f"-----Running {script}-----", style="bold blue")
        # Run the script again and get the new status and output
        runner = ScriptRunner(script)
        status, new_output = runner.run_script()
        console.print(new_output)
        
        progress_id_output = 'f'

        # If the new script run status is not successful
        if not status:
            console.print("DebugGPT has identified another/new error", style="bold red")
            console.print("-----Analyzing Output-----", style="bold blue")
            # Generate edit analysis output
            edit_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":new_output}])
            console.print(edit_analysis_output, style="bold red")
            console.print("-----Analyzing Progress-----", style="bold blue")
            # Generate compare errors output
            compare_errors_output = manager.generate("ErrorComparison", [{"role":"user","content":f"Old Error: {str(error_analysis_output)}\n\nNew Error:{str(edit_analysis_output)}"}])
            console.print(compare_errors_output, style="bold green")
            # Generate progress id output
            progress_id_output = manager.generate("ProgressIdentifier", [{"role":"user","content":str(compare_errors_output)}])
            # If progress was made
            if progress_id_output == 't': 
                console.print("%%DebugGPT has identified progress was made", style="bold green")
            else: 
                console.print("%%DebugGPT has identified no/reverse progress was made", style="bold red")
        
        console.print("-----Deciding Next Step-----", style="bold blue")
        console.print("***User Input Required***", style="bold yellow")
        # Display the changes in the script
        change_logger.display_changes()
        questions = [
            inquirer.List('choice',
                          message="Would you like to keep the above changes or revert?",
                          choices=['Continue', 'Revert'],
                          ),
        ]
        # Prompt the user to answer the question
        answers = inquirer.prompt(questions)
        # If the user chooses to continue
        if answers['choice'] == 'Continue':
            console.print("-----Continuing Debug-----", style="bold blue")
            # Debug the script again
            debug_script(script)
        # If the user chooses to revert
        elif answers['choice'] == 'Revert':
            console.print("-----Reverting Changes-----", style="bold blue")
            # Revert the last change in the script
            change_logger.revert_last_change()
            console.print("-----Deciding Next Step-----", style="bold blue")
            console.print("***User Input Required***", style="bold yellow")
            questions = [
                inquirer.List('choice',
                              message="Would you like to try debugging again?",
                              choices=['Yes', 'No'],
                              ),
            ]
            # Prompt the user to answer the question
            answers = inquirer.prompt(questions)
            # If the user chooses not to debug again
            if answers['choice'] == 'No': return False
            console.print("-----Continuing Debug-----", style="bold blue")
            # Debug the script again
            debug_script(script)
    return status

# Define the main function
def main():
    # If the number of command line arguments is not 2
    if len(sys.argv) != 2:
        print("Usage: dgpt file_name.py")
        # Exit the script
        sys.exit(1)

    # Get the script file from the command line arguments
    script_file = sys.argv[1]
    console.rule("[bold blue]DebugGPT")
    # Debug the script file
    debug_script(script_file)
    console.print("All Errors Solved or DebugGPT Terminated", style="italic purple")
    console.rule("[bold blue]https://github.com/benborszcz/DebugGPT")
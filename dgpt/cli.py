# Import necessary modules
from .script_runner import ScriptRunner
from .agent_manager import AgentManager
from .change_logger import ChangeLogger
from rich.console import Console
from rich.traceback import install
from rich.progress import Progress
from pyfiglet import Figlet
import argparse
import inquirer
import sys
import pathspec
import os
import re

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

def extract_filenames(text):
    # Remove everything between ```
    pattern = r'```.*?```'
    clean_text = re.sub(pattern, '', text, flags=re.DOTALL)

    # Extract filenames
    pattern = r'(?<=# )\w+\.py'
    matches = re.findall(pattern, clean_text)

    # Create output string
    output = "Files Requested:\n"
    for match in matches:
        output += match + "\n"

    return output

# Define a function to debug a script
def debug_script(script, verbose, slim):
    # Create a change logger object
    change_logger = ChangeLogger(os.path.dirname(os.path.abspath(script)))
    # Create a script runner object
    runner = ScriptRunner(script)

    # Define the steps
    steps_1 = [
        'Analyzing the output',
        'Requesting Files',
        'Planning Solution',
        'Editing Files',
    ]
    steps_2 = [
        'Analyzing the output',
        'Comparing Errors',
        'Checking Progress',
    ]

    # Create a progress bar


    console.print(f"Running {script}", style="bold blue")
    # Run the script and get the status and output
    status, output = runner.run_script()
    if not slim or verbose: console.print(output)
    # If the script run status is not successful
    if not status:
        console.print("DebugGPT has identified an error", style="bold red")
        error_analysis_output = ''
        with Progress() as progress:
            task = None
            if slim: 
                task = progress.add_task("[cyan]Processing...", total=len(steps_1))
            if not slim or verbose: console.print("Analyzing Output", style="bold blue")
            # Generate error analysis output
            error_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":output}])
            if verbose: console.print(error_analysis_output, style="bold red")
            if not slim or verbose: console.print("Requesting Files", style="bold blue")
            if slim: progress.update(task, advance=1)
            # Generate file getter output
            file_getter_output = manager.generate("FileRequester", [{"role":"user","content":str(error_analysis_output)+"\n\n"+str(visualize_file_structure(os.getcwd()))}])
            if verbose: console.print(extract_filenames(file_getter_output), style="bold green")
            if not slim or verbose: console.print("Planning Solution", style="bold blue")
            if slim: progress.update(task, advance=1)
            # Generate step planner output
            step_planner_output = manager.generate("StepPlanner", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output))}])
            if verbose: console.print(step_planner_output, style="bold green")
            if not slim or verbose: console.print("Editing Files", style="bold blue")
            if slim: progress.update(task, advance=1)
            # Generate code modifier output
            code_modifier_output = manager.generate("CodeModifier", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output)+"\n\n"+str(step_planner_output))}])
            if verbose: console.print(code_modifier_output, style="bold green")
            if slim: 
                progress.update(task, advance=1)
                progress.stop()
        
        change_logger.check_changes()
        console.print(f"Running {script}", style="bold blue")
        # Run the script again and get the new status and output
        runner = ScriptRunner(script)
        status, new_output = runner.run_script()
        if not slim or verbose: console.print(new_output)
        
        progress_id_output = 'f'
        compare_errors_output = ''

        # If the new script run status is not successful
        if not status:
            console.print("DebugGPT has identified another/new error", style="bold red")
            with Progress() as progress:
                if slim: task = progress.add_task("[cyan]Processing...", total=len(steps_2))
                if not slim or verbose: console.print("Analyzing Output", style="bold blue")
                # Generate edit analysis output
                edit_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":new_output}])
                if verbose: console.print(edit_analysis_output, style="bold red")
                if not slim or verbose: console.print("Analyzing Progress", style="bold blue")
                if slim: progress.update(task, advance=1)
                # Generate compare errors output
                compare_errors_output = manager.generate("ErrorComparison", [{"role":"user","content":f"Old Error: {str(error_analysis_output)}\n\nNew Error:{str(edit_analysis_output)}"}])
                if verbose: console.print(compare_errors_output, style="bold green")
                if slim: progress.update(task, advance=1)
                # Generate progress id output
                progress_id_output = manager.generate("ProgressIdentifier", [{"role":"user","content":str(compare_errors_output)}])
                if slim: 
                    progress.update(task, advance=1)
                    progress.stop()
           
            # If progress was made
            if progress_id_output == 't': 
                console.print("DebugGPT has identified progress was made", style="bold green")
            else: 
                console.print("DebugGPT has identified no/reverse progress was made", style="bold red")
        
        if not slim or verbose: console.print("Deciding Next Step", style="bold blue")
        summarization_output = manager.generate("Summarizer", [{"role":"user","content":"# Original Output\n"+str(error_analysis_output)+"\n\n# Fix\n"+str(step_planner_output)+"\n\n# New Output Comparison\n"+str(compare_errors_output)+"\n\nSummarize what happened in 2 sentences, cover what was wrong and what was changed. Do not mention the new error, ONLY explain the old one and how it was fixed"}])
        console.print("\nSummarization:", style="bold green")
        console.print(summarization_output, style="green")
        console.print("\n***User Input Required***", style="bold yellow")
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
            console.print("Continuing Debug", style="bold blue")
            # Debug the script again
            debug_script(script, verbose, slim)
        # If the user chooses to revert
        elif answers['choice'] == 'Revert':
            console.print("Reverting Changes", style="bold blue")
            # Revert the last change in the script
            change_logger.revert_last_change()
            if not slim or verbose: console.print("Deciding Next Step", style="bold blue")
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
            console.print("Continuing Debug", style="bold blue")
            # Debug the script again
            debug_script(script, verbose, slim)
    return status

# Define the main function
def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Debug a Python script with DebugGPT.')
    parser.add_argument('script_file', type=str, help='The Python script to debug.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output.')
    parser.add_argument('-s', '--slim', action='store_true', help='Enable slim output.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Pass the verbose flag to the debug_script function
    console.rule("")
    f = Figlet(font='big')
    ascii_art = f.renderText('DebugGPT')
    console.print(f"[bold blue]{ascii_art}[/bold blue]")
    console.print("Welcome to DebugGPT! A Python-based debugging tool that leverages OpenAI's GPT-3.5 model to help debug Python scripts.")
    console.print("DebugGPT analyzes error codes, identifies the files involved, and explains the error in natural language. It also provides a step-by-step plan to solve the problem, generates the necessary code to fix the error, and applies the changes to the script.")
    console.print("After applying the changes, DebugGPT will re-run the script to check if the changes have improved the script or solved the errors.")
    console.print("If you're interested in supporting or contributing visit us here: https://github.com/benborszcz/DebugGPT")
    console.print("***User Input Required***", style="bold yellow")
    questions = [
        inquirer.List('choice',
                    message="Would you like to try debugging?",
                    choices=['Yes', 'No'],
                    ),
    ]
    # Prompt the user to answer the question
    answers = inquirer.prompt(questions)
    if answers['choice'] == 'Yes': debug_script(args.script_file, args.verbose, args.slim)
    console.print("All Errors Solved or DebugGPT Terminated", style="italic purple")
    console.rule("[bold blue]https://github.com/benborszcz/DebugGPT")
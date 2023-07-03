from .script_runner import ScriptRunner
from .agent_manager import AgentManager
from .change_logger import ChangeLogger
import os
from rich.console import Console
from rich.progress import Progress
from rich.traceback import install
from rich import print as rprint
import inquirer
import time

install()

console = Console()

manager = AgentManager()

def debug_script(script):
    change_logger = ChangeLogger(os.path.dirname(os.path.abspath(script)))
    runner = ScriptRunner(script)
    console.print(f"-----Running {script}-----", style="bold blue")
    status, output = runner.run_script()
    console.print(output)
    if not status:
        console.print("-----Analyzing Output-----", style="bold blue")
        error_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":output}])
        console.print(error_analysis_output, style="bold red")
        console.print("-----Requesting Files-----", style="bold blue")
        file_getter_output = manager.generate("FileRequester", [{"role":"user","content":str(error_analysis_output)}])
        console.print(file_getter_output, style="bold green")
        console.print("-----Planning Solution-----", style="bold blue")
        step_planner_output = manager.generate("StepPlanner", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output))}])
        console.print(step_planner_output, style="bold green")
        console.print("-----Editing Files-----", style="bold blue")
        code_modifier_output = manager.generate("CodeModifier", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output)+"\n\n"+str(step_planner_output))}])
        console.print(code_modifier_output, style="bold green")
        change_logger.check_changes()
        console.print(f"-----Running {script}-----", style="bold blue")
        runner = ScriptRunner(script)
        status, new_output = runner.run_script()
        console.print(new_output)
        
        progress_id_output = 'f'

        if not status:
            console.print("DebugGPT has identified another/new error", style="bold red")
            console.print("-----Analyzing Output-----", style="bold blue")
            edit_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":new_output}])
            console.print(edit_analysis_output, style="bold red")
            console.print("-----Analyzing Progress-----", style="bold blue")
            compare_errors_output = manager.generate("ErrorComparison", [{"role":"user","content":f"Old Error: {str(error_analysis_output)}\n\nNew Error:{str(edit_analysis_output)}"}])
            console.print(compare_errors_output, style="bold green")
            progress_id_output = manager.generate("ProgressIdentifier", [{"role":"user","content":str(compare_errors_output)}])
            if progress_id_output == 't': console.print("%%DebugGPT has identified progress was made", style="bold green")
            else: console.print("%%DebugGPT has identified no/reverse progress was made", style="bold red")
        
        console.print("-----Deciding Next Step-----", style="bold blue")
        console.print("***User Input Required***", style="bold yellow")
        change_logger.display_changes()
        questions = [
            inquirer.List('choice',
                          message="Would you like to keep the above changes or revert?",
                          choices=['Continue', 'Revert'],
                          ),
        ]
        answers = inquirer.prompt(questions)
        if answers['choice'] == 'Continue':
            console.print("-----Continuing Debug-----", style="bold blue")
            debug_script(script)
        elif answers['choice'] == 'Revert':
            console.print("-----Reverting Changes-----", style="bold blue")
            change_logger.revert_last_change()
            console.print("-----Deciding Next Step-----", style="bold blue")
            console.print("***User Input Required***", style="bold yellow")
            questions = [
                inquirer.List('choice',
                              message="Would you like to try debugging again?",
                              choices=['Yes', 'No'],
                              ),
            ]
            answers = inquirer.prompt(questions)
            if answers['choice'] == 'No': return False
            console.print("-----Continuing Debug-----", style="bold blue")
            debug_script(script)
    return status

"""
console.rule("[bold blue]DebugGPT")
debug_script('main_errors.py')
console.print("All Errors Solved or DebugGPT Terminated", style="italic purple")
console.rule("[bold blue]https://github.com/benborszcz/DebugGPT")
"""
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: dgpt file_name.py")
        sys.exit(1)

    script_file = sys.argv[1]
    console.rule("[bold blue]DebugGPT")
    debug_script(script_file)
    console.print("All Errors Solved or DebugGPT Terminated", style="italic purple")
    console.rule("[bold blue]https://github.com/benborszcz/DebugGPT")
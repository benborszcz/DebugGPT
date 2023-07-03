from script_runner import ScriptRunner
from agent_manager import AgentManager
from change_logger import ChangeLogger
import os
from rich.console import Console
from rich.progress import track
from rich.traceback import install
from rich import print as rprint

# Install the rich traceback handler
install()

console = Console()

manager = AgentManager()

def debug_script(script):
    change_logger = ChangeLogger(os.path.dirname(os.path.abspath(script)))

    runner = ScriptRunner(script)
    console.rule("[bold red]DebugGPT")
    console.print("-----Running Script-----", style="bold blue")
    status, output = runner.run_script()
    console.print(output)
    if not status:
        console.print("-----Analyzing Output-----", style="bold blue")
        error_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":output}])
        console.print(error_analysis_output)
        console.print("-----Requesting Files-----", style="bold blue")
        file_getter_output = manager.generate("FileRequester", [{"role":"user","content":str(error_analysis_output)}])
        console.print(file_getter_output)
        console.print("-----Planning Solution-----", style="bold blue")
        step_planner_output = manager.generate("StepPlanner", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output))}])
        console.print(step_planner_output)
        console.print("-----Editing Files-----", style="bold blue")
        code_modifier_output = manager.generate("CodeModifier", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output)+"\n\n"+str(step_planner_output))}])
        console.print(code_modifier_output)
        change_logger.check_changes()
        console.print("-----Running Script-----", style="bold blue")
        status, new_output = runner.run_script()
        console.print(new_output)
        
        progress_id_output = 'f'

        if not status:
            console.print("DebugGPT has identified another/new error", style="bold red")
            console.print("-----Analyzing Output-----", style="bold blue")
            edit_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":new_output}])
            console.print(edit_analysis_output)
            console.print("-----Analyzing Progress-----", style="bold blue")
            compare_errors_output = manager.generate("ErrorComparison", [{"role":"user","content":f"Old Error: {str(error_analysis_output)}\n\nNew Error:{str(edit_analysis_output)}"}])
            console.print(compare_errors_output)
            progress_id_output = manager.generate("ProgressIdentifier", [{"role":"user","content":str(compare_errors_output)}])
            if progress_id_output == 't': console.print("DebugGPT has identified progress was made", style="bold green")
            else: console.print("DebugGPT has identified no/reverse progress was made", style="bold red")
        
        console.print("-----Deciding Next Step-----", style="bold blue")
        console.print("***User Input Required***", style="bold yellow")
        change_logger.display_changes()
        console.print("Would you like to keep the above changes or revert?", style="bold yellow")
        cont = console.input("(1)Contine or (0)Revert: ")
        if cont == '1':
            console.print("-----Continuing Debug-----", style="bold blue")
            debug_script(script)
        elif cont == '0':
            console.print("-----Reverting Changes-----", style="bold blue")
            change_logger.revert_last_change()
            console.print("-----Deciding Next Step-----", style="bold blue")
            console.print("***User Input Required***", style="bold yellow")
            console.print("Would you like to try debugging again?", style="bold yellow")
            deb = console.input("(1)Yes or (0)No: ")
            if deb == '0': return False
            console.print("-----Continuing Debug-----", style="bold blue")
            debug_script(script)
    return status

debug_script('test_script.py')
console.rule("[bold red]https://github.com/benborszcz/DebugGPT")
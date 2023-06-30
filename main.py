from script_runner import ScriptRunner
from agent_manager import AgentManager

manager = AgentManager()



def debug_script(script):
    runner = ScriptRunner(script)
    print("-----Running Script-----")
    status, output = runner.run_script()
    print(output)
    if not status:
        print("-----Analyzing Output-----")
        error_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":output}])
        print(error_analysis_output)
        print("-----Requesting Files-----")
        file_getter_output = manager.generate("FileRequester", [{"role":"user","content":str(error_analysis_output)}])
        print(file_getter_output)
        print("-----Planning Solution-----")
        step_planner_output = manager.generate("StepPlanner", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output))}])
        print(step_planner_output)
        print("-----Editing Files-----")
        code_modifier_output = manager.generate("CodeModifier", [{"role":"user","content":(str(error_analysis_output)+"\n\n"+str(file_getter_output)+"\n\n"+str(step_planner_output))}])
        print(code_modifier_output)
        print("-----Running Script-----")
        status, new_output = runner.run_script()
        print(new_output)
        if not status:
            print("-----Analyzing Output-----")
            edit_analysis_output = manager.generate("ErrorAnalysis", [{"role":"user","content":new_output}])
            print(edit_analysis_output)
            print("-----Analyzing Progress-----")
            compare_errors_output = manager.generate("ErrorComparison", [{"role":"user","content":f"Old Error: {str(error_analysis_output)}\n\nNew Error:{str(edit_analysis_output)}"}])
            print(compare_errors_output)
            print("-----Deciding Next Step-----")
            progress_id_output = manager.generate("ProgressIdentifier", [{"role":"user","content":str(compare_errors_output)}])
            print(progress_id_output)
            if progress_id_output == 't' :
                debug_script(script)
            else:
                print("revert")
    return status

debug_script('test_script.py')
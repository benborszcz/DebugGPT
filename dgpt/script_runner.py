import subprocess
import traceback

class ScriptRunner:
    # Initialize the class with the script path
    def __init__(self, script_path):
        self.script_path = script_path

    def run_script(self):
        try:
            # Run the script using subprocess and capture the output
            result = subprocess.run(['python', self.script_path], capture_output=True, text=True)
            # If the script runs successfully, return True and a success message
            if result.returncode == 0:
                return True, f"Running {self.script_path} Successful"
            # If the script fails, return False and the error message
            else:
                return False, result.stderr
        # If an exception occurs while running the script, return False and the traceback
        except Exception as e:
            return False, "".join(traceback.format_exception(type(e), e, e.__traceback__))
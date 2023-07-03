import subprocess
import traceback

class ScriptRunner:

    def __init__(self, script_path):
        self.script_path = script_path

    def run_script(self):
        try:
            result = subprocess.run(['python', self.script_path], capture_output=True, text=True)
            if result.returncode == 0:
                return True, f"Running {self.script_path} Successful"
            else:
                return False, result.stderr
        except Exception as e:
            return False, "".join(traceback.format_exception(type(e), e, e.__traceback__))
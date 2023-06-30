import traceback
import runpy

class ScriptRunner:

    def __init__(self, script_path):
        self.script_path = script_path

    def run_script(self):
        try:
            runpy.run_path(self.script_path)
            return True, f"Running {self.script_path} Successful"
        except Exception as e:
            return False, "".join(traceback.format_exception(type(e), e, e.__traceback__))
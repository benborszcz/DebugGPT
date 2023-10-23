import subprocess
import traceback
import os

class ScriptRunner:
    # Initialize the class with the script path
    def __init__(self, script_path):
        self.script_path = script_path

    def run_script(self):
        try:
            # Determine the script type by file extension
            _, extension = os.path.splitext(self.script_path)
            if extension == '.py':
                cmd = ['python', self.script_path]
            elif extension == '.java':
                # Compile the Java source file
                compile_result = subprocess.run(['javac', self.script_path], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return False, compile_result.stderr

                # Run the compiled bytecode
                # Assumes the Java file has a main method in a public class with the same name as the file
                java_class = os.path.splitext(os.path.basename(self.script_path))[0]
                cmd = ['java', '-cp', os.path.dirname(self.script_path), java_class]
            elif extension == '.js':
                cmd = ['node', self.script_path]
            elif extension == '.R':
                cmd = ['Rscript', self.script_path]
            else:
                return False, f"Unsupported script type: {extension}"

            # Check if the file exists
            if not os.path.exists(self.script_path):
                return False, f"File not found: {self.script_path}"

            # Run the script using subprocess and capture the output
            result = subprocess.run(cmd, capture_output=True, text=True)
            # If the script runs successfully, return True and a success message
            if result.returncode == 0:
                return True, f"Running {self.script_path} Successful"
            # If the script fails, return False and the error message
            else:
                return False, result.stderr
        # If an exception occurs while running the script, return False and the traceback
        except Exception as e:
            return False, "".join(traceback.format_exception(type(e), e, e.__traceback__))

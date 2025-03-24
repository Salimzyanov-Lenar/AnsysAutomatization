import subprocess


class Executor:
    """ Creating a executor object which execute command in the shell """
    def __init__(self, executor_path, project_path):
        self.command = [
            executor_path,
            "-B",
            "-F",  project_path,
            "-R", "working_config.wbjn"
        ]

    def __call__(self):
        try:
            result = subprocess.run(self.command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print("Executed successfully")

        except Exception as e:
            print(f"Error {e}")


executor = Executor(r"E:\Ansys Inc\v241\Framework\bin\Win64\RunWB2.exe", r"C:\Users\Lenar\AnsysProjects\pipe_3.wbpj")
executor()

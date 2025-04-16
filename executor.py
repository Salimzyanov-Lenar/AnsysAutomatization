import subprocess
import csv


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


def execute_with_updated_config(ansys_executor_path, ansys_project_path):
    # executor = Executor(r"E:\Ansys Inc\v241\Framework\bin\Win64\RunWB2.exe", r"C:\Users\Lenar\AnsysProjects\pipe_3.wbpj")
    # executor = Executor(executor_path, r"C:\Users\Lenar\AnsysProjects\pipe_3.wbpj")
    executor = Executor(ansys_executor_path, ansys_project_path)

    try:
        print("Start calculating")
        executor()
        print("Success")
    except Exception as e:
        print("Error", e)

    with open(r"C:\Users\Lenar\AnsysProjects\pipe_script_csv.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        data = []
        print(reader)

        for row in reader:
            if row and not row[0].startswith('#'):
                data.append(row)

        if len(data) >= 2:
            headers = data[1][0].split(',')
            values = data[2][0].split(',')

            result = {headers[i]: values[i] for i in range(2, len(headers))}
            return result
        
        return None
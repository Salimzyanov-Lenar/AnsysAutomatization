import subprocess
import csv
import re


class Executor:
    """ Creating a executor object which execute command in the shell """
    """ Создаёт объект испольнитель, который выполнил код в терминале """
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


def execute_with_updated_config(ansys_executor_path, ansys_project_path, ansys_result_path):
    """ Executing with updated params """
    """ Исполняет команду с обновленным конфигом """
    executor = Executor(ansys_executor_path, ansys_project_path)
    try:
        print("Start calculating")
        executor()
        print("Success")
    except Exception as e:
        print("Error", e)

from functions.run_python_file import run_python_file

run_cases = [
    ["../calculator","main.py","", "Running calculator with no arguments.\n"],
    ["../calculator", "main.py", ["3 + 5"], "Running calculator with arguments.\n"],
    ["../calculator", "tests.py", "", "Running calculator test harness.\n"],
    ["../calculator", "../main.py", "", "Running not found program. This should return an error.\n"],
    ["../calculator", "nonexistent.py", "", "Running non-existent program. This should return an error.\n"],
    ["../calculator", "lorem.txt", "", "Running invalid file. This should return an error.\n"],
]

#for case in run_cases:

working_dir = "calculator"
target_file = "tests.py"
args = None
header = "Running calculator test harness.\n"

result = run_python_file(working_dir, target_file, args)
    
print(f"{header}{result}")

from get_file_content import *

run_cases = [
    ["../calculator","main.py", 'Result for "main.py":\n'],
    ["../calculator", "pkg/calculator.py", 'Result for "pkg/calculator.py" file:\n'],
    ["../calculator", "/bin/cat", 'Result for "/bin/cat" file:\n'],
    ["../calculator", "pkg/does_not_exist.py", 'Result for "pkg/does_not_exist.py" file:\n']
]

# test file truncation
working_dir = "../calculator"
target_file = "lorem.txt"
header = "Result for truncation:\n"

output = get_file_content(working_dir, target_file)
if (output_length := len(output)) > 10000:
    truncation_message = output[10000:]
    message = f'    Length of {target_file}: {output_length}\n    Truncation message: {truncation_message}'
    print(f"{header}{message}")

for case in run_cases:
    working_dir = case[0]
    target_file = case[1]
    header = case[2]

    output = get_file_content(working_dir, target_file)
    
    print(f"{header}{output}")


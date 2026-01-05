from get_files_info import *

run_cases = [
    ["../calculator",".", "Result for current directory:\n"],
    ["../calculator", "pkg", "Result for 'pkg' directory:\n"],
    ["../calculator", "/bin", "Result for '/bin/ directory:\n"],
    ["../calculator", "../", "Result for '../' directory:\n"]
]

for case in run_cases:
    working_dir = case[0]
    directory = case[1]
    header = case[2]

    output = get_files_info(working_dir, directory)
    
    print(f"{header}{output}")


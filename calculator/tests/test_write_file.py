from write_file import *

run_cases = [
    ["../calculator","lorem.txt", "wait, this isn't lorem ipsum", 'Result of writing to "lorem.txt":\n'],
    ["../calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", 'Result of writing to "pkg/morelorem.txt":\n'],
    ["../calculator", "/tmp/temp.txt", "this should not be allowed", 'Result of writing to "/tmp/temp.txt":\n'],
]

for case in run_cases:
    working_dir = case[0]
    target_file = case[1]
    content = case[2]
    header = case[3]

    output = write_file(working_dir, target_file, content)
    
    print(f"{header}{output}")


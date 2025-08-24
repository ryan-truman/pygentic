from functions.get_file_content import get_file_content

# print(f"Result for lorem.txt:\n{get_file_content('calculator', 'lorem.txt')}")

print(f"Result for 'main.py':\n{get_file_content("calculator", "main.py")}")

print(f"Result for 'pkg/calculator.py':\n{get_file_content("calculator", "pkg/calculator.py")}")

print(f"Result for 'bin/cat' :\n{get_file_content("calculator", "/bin/cat")}")

print(f"Result for 'pkg/does_not_exist.py':\n{get_file_content("calculator", "pkg/does_not_exist.py")}")

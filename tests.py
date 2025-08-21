from functions.get_files_info import get_files_info

print(f"Result for Current Directory:\n{get_files_info("calculator", ".")}")

print(f"Result for 'pkg' Directory:\n{get_files_info("calculator", "pkg")}")

print(f"Result for 'bin' Directory:\n{get_files_info("calculator", "/bin")}")

print(f"Result for '../' Directory:\n{get_files_info("calculator", "../")}")

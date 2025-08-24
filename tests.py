from functions.write_file import write_file

print(f"Result for 'lorem.txt':\n{write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")}")

print(f"Result for 'pkg/morelorem.txt.':\n{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}")

print(f"Result for '/tmp/temp.txt' :\n{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}")


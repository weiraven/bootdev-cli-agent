from functions.run_python_file import run_python_file

def main():
    tests = [
        ("calculator", "main.py", None),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", None),
        ("calculator", "../main.py", None),
        ("calculator", "nonexistent.py", None),
        ("calculator", "lorem.txt", None),
    ]

    for num, (working_directory, file_path, args) in enumerate(tests, start=1):
        print(f"Result for Test #{num}:")
        result = run_python_file(working_directory, file_path, args)
        print(f"  {result}")
        print()

if __name__ == "__main__":
    main()
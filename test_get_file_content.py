from functions.get_file_content import get_file_content
from config import MAX_CHARACTERS

def main():
    print("Result for lorem.txt:")
    lorem_result = get_file_content("calculator", "lorem.txt")

    if lorem_result.startswith("Error:"):
        print(f"  {lorem_result}")
    else:
        print(f"  Length: {len(lorem_result)}")
        print(f"  Ends with truncation message: {lorem_result.endswith(f'[...File \"lorem.txt\" truncated at {MAX_CHARACTERS} characters]')}")
    print()

    tests = [
        ("main.py", "calculator", "main.py"),
        ("pkg/calculator.py", "calculator", "pkg/calculator.py"),
        ("/bin/cat", "calculator", "/bin/cat"),
        ("pkg/does_not_exist.py", "calculator", "pkg/does_not_exist.py"),
    ]

    for label, working_directory, file_path in tests:
        print(f"Result for {label}:")
        result = get_file_content(working_directory, file_path)
        print(result)
        print()

if __name__ == "__main__":
    main()
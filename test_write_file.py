from functions.write_file import write_file

def main():
    tests = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    for working_directory, file_path, content in tests:
        print(f"Result for {file_path}:")
        result = write_file(working_directory, file_path, content)
        print(f"  {result}")
        print()

if __name__ == "__main__":
    main()
from functions.get_files_info import get_files_info

def main():
    tests = [
        ("current directory", "calculator", "."),
        ("'pkg' directory", "calculator", "pkg"),
        ("'/bin' directory", "calculator", "/bin"),
        ("'../' directory", "calculator", "../"),
    ]

    for label, working_directory, directory in tests:
        print(f"Result for {label}:")
        result = get_files_info(working_directory, directory)

        if result.startswith("Error:"):
            print(f"  {result}")
        else:
            for line in result.splitlines():
                print(f"  {line}")

        print()

if __name__ == "__main__":
    main()
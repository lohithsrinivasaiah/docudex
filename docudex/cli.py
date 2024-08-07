import argparse
import os

import toml

from docudex.utils.file_utils import get_file_type


def get_version() -> str:
    """
    Reads the version from the pyproject.toml file.
    """
    try:
        with open("pyproject.toml") as file:
            pyproject_data = toml.load(file)
            return (
                pyproject_data.get("tool", {})
                .get("poetry", {})
                .get("version", "Version not found")
            )
    except FileNotFoundError:
        return "pyproject.toml not found"
    except Exception as e:
        return f"Error reading version: {e}"


def list_directory(directory: str) -> None:
    """
    Lists the contents of the specified directory.
    """
    if os.path.isdir(directory):
        print(f"Directory: {directory}")
        for item in os.listdir(directory):
            print(f" - {item}")
    else:
        print(f"{directory} is not a valid directory.")


def parse_arguments() -> argparse.ArgumentParser:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="DocuDex is a CLI tool for efficient document interaction and analysis.",
    )
    parser.add_argument("-f", "--files", type=str, help="Pass a file to check its type")
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Pass a directory to list its contents",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Display the installed version",
    )

    return parser


def main() -> None:
    """
    The main entry point of the CLI app.
    """
    parser = parse_arguments()
    args = parser.parse_args()

    if args.version:
        print(f"DocuDex {get_version()}")
    elif args.files:
        print(get_file_type(args.files))
    elif args.directory:
        list_directory(args.directory)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

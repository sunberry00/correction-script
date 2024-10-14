# Homework Extractor

This script extracts homework files for relevant students from a specified folder and copies them to an output folder. It processes student names to handle special characters and filters the homework submissions accordingly.

## Prerequisites

- Python 3.6 or higher
- Required Python packages: `argparse`, `os`, `zipfile`, `shutil`, `logging`, `typing`

## Installation

1. Clone the repository or download the script files.
2. Ensure you have Python 3.6 or higher installed.


## Usage

1. Prepare a text file (`students.txt`) containing the list of student names, one per line.
Student names should have format: Last_name, First_name (e.g., Doe, John). Separated by a comma and space.
2. Run the script with the following command:

    ```sh
    python main.py --z <path_to_zip_file> --o <path_to_output_folder>
    ```

    - `--z`: Path to the zip file containing homework submissions.
    - `--o`: Path to the output folder where the extracted homework files will be copied.

## Example

```sh
python main.py --z submissions.zip --o extracted_homeworks
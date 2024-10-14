import argparse
import os
import zipfile
import shutil
import logging
from typing import List, Tuple


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_command_line() -> Tuple[str, str]:
    """
    Parse command line arguments.

    Returns:
        Tuple[str, str]: Path to zip file and output folder.
    """
    parser = argparse.ArgumentParser(description='Extract homework only from relevant students')
    parser.add_argument('--z', type=str, required=True, help='Path to the zip file')
    parser.add_argument('--o', type=str, required=True, help='Path to the output folder')
    args = parser.parse_args()
    return args.z, args.o


def read_student_names(file: str) -> List[str]:
    """
    Reads a file containing student names, one per line, and returns a list of these names.

    Args:
        file (str): The path to the file containing student names.

    Returns:
        List[str]: A list of student names read from the file.

    Raises:
        IOError: If there is an error reading the file.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    except IOError as e:
        logging.error(f"Error reading student names file: {e}")
        raise


def unzip(file: str, output: str) -> str:
    """
    Unzips a zip file to the specified output directory.

    Args:
        file (str): The path to the zip file.
        output (str): The path to the output directory.

    Returns:
        str: The base name of the zip file without its extension.

    Raises:
        zipfile.BadZipFile: If the file is not a valid zip file.
    """
    try:
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(output)
        return os.path.splitext(os.path.basename(file))[0]
    except zipfile.BadZipFile:
        logging.error(f"Error: {file} is not a valid zip file")
        raise


def prepare_student_names(students: List[str]) -> List[str]:
    """
    Prepares a list of student names by replacing umlauts and special characters.

    Args:
        students (List[str]): A list of student names.

    Returns:
        List[str]: A list of processed student names with umlauts replaced and formatted.
    """
    umlaut_map = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    return [
        ''.join(umlaut_map.get(c, c) for c in student.replace(", ", "_").lower())
        for student in students
    ]


def extract_homeworks(folder: str, student_set: set, output_folder: str):
    """
    Extracts homework files for relevant students from a specified folder and copies them to an output folder.

    Args:
        folder (str): The path to the folder containing homework submissions.
        student_set (set): A set of student names to filter the homework submissions.
        output_folder (str): The path to the folder where the extracted homework files will be copied.

    Raises:
        FileNotFoundError: If no PDF files are found in a student's homework folder.
    """
    for homework in os.listdir(folder):
        if any(student in homework.lower() for student in student_set):
            homework_path = os.path.join(folder, homework)
            pdf_files = [f for f in os.listdir(homework_path) if f.endswith('.pdf')]
            if pdf_files:
                src = os.path.join(homework_path, pdf_files[0])
                dst = os.path.join(output_folder, pdf_files[0])
                shutil.copyfile(src, dst)
                logging.info(f"Copied {pdf_files[0]} to output folder")
            else:
                logging.warning(f"No PDF found in {homework}")


def main():
    """
    Main function to set up logging, parse command line arguments, unzip the file, read student names,
    prepare the student names, and extract homework files.

    Raises:
        FileNotFoundError: If the 'Abgaben' folder is not found in the unzipped directory.
        Exception: For any other errors that occur during the process.
    """
    setup_logging()

    zip_file, output_folder = parse_command_line()

    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    try:
        zip_name = unzip(zip_file, temp_folder)
        student_list = read_student_names("resources/students.txt")
        student_set = set(prepare_student_names(student_list))

        folder = os.path.join(temp_folder, zip_name, "Abgaben")
        if not os.path.exists(folder):
            raise FileNotFoundError(f"'Abgaben' folder not found in {folder}")

        extract_homeworks(folder, student_set, output_folder)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
            logging.info("Cleaned up temporary files")


if __name__ == "__main__":
    main()
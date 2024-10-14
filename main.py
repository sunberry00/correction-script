import zipfile

def main():
    # Unzip the file
    unzip("Hausaufgabe 00.zip", "data")


def unzip(file, output):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(output)


if __name__ == "__main__":
    main()
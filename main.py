from FileReader import FileReader


def start_reading():
    index_dir = "index"
    reader = FileReader(index_dir)
    data_path = "C:\Users\julie\OneDrive\Documents\developer.zip"

    reader.build_index(data_path)


if __name__ == "__main__":
    start_reading()

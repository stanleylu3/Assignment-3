from FileReader import FileReader


def start_reading():
    index_dir = "index"
    reader = FileReader(index_dir)
    # change this to whatever is that path to the corpus
    data_path = "C:\Users\julie\OneDrive\Documents\developer.zip"

    reader.build_index(data_path)

    # gather analytics
    num_indexed_doc = reader.num_indexed_doc
    num_unique_words = reader.num_unique_words
    total_index_size = reader.total_index_size

    print("Analytics:")
    print("Number of Indexed Documents:", num_indexed_doc)
    print("Number of Unique Tokens:", num_unique_words)
    print("Total Index Size (KB):", total_index_size)


if __name__ == "__main__":
    start_reading()

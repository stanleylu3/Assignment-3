import sys

import FileReader as f
import SearchEngine as s

def run(path):
    reader = f.FileReader()
    # path = r"C:\Users\julie\OneDrive\Documents\developer.zip"
    index, doc_info = reader.build_index(path)
    engine = s.SearchEngine(index, doc_info)
    engine.run()
    # size = reader.calculate_size(index, r"C:\Users\julie\OneDrive\Documents\developer.zip")
    #
    # print("Analytics:")
    # print(f"Number of documents: {reader.total_docs}")
    # print(f"Number of tokens: {len(index)}")
    # print(f"Size of Index: {size} KB")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python main.py path_to_zip_folder')
        sys.exit(1)
    path = sys.argv[1]
    run(path)
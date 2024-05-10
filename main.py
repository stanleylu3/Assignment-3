import FileReader as f
import sys

def run(path):
    reader = f.FileReader()
    # CHANGE PATH
    #path = "C:\\Users\sssl2\Downloads\developer.zip"
    index = reader.build_index(path)
    # CHANGE PATH
    size = reader.calculate_size(index, path)

    print("Analytics:")
    print(f"Number of documents: {reader.total_docs}")
    print(f"Number of tokens: {len(index)}")
    print(f"Size of Index: {size} KB")

if __name__ == "__main__":
    if  len(sys.argv) != 2:
        print('Usage: python main.py path_to_zip_folder')
        sys.exit(1)
    path = sys.argv[1]
    run(path)
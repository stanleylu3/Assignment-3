import FileReader as f
import Posting

def run():
    reader = f.FileReader()
    path = r"C:\Users\julie\OneDrive\Documents\developer.zip"
    index = reader.build_index(path)

    size = reader.calculate_size(index, r"C:\Users\julie\OneDrive\Documents\developer.zip")

    print("Analytics:")
    print(f"Number of documents: {reader.total_docs}")
    print(f"Number of tokens: {len(index)}")
    print(f"Size of Index: {size} KB")

if __name__ == "__main__":
    run()
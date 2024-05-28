import sys

import FileReader as f
import SearchEngine as s

def run(path, path2):
    # reader = f.FileReader()
    # reader.build_final_index(path)
    engine = s.SearchEngine(path, path2)
    engine.run()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python main.py path_to_zip_folder')
        sys.exit(1)
    path = sys.argv[1]
    path2 = sys.argv[2]
    run(path, path2)
import sys

import FileReader as f
import SearchEngine as s

def run(path, path2, path3):
    # reader = f.FileReader()
    # reader.build_final_index(path)
    # reader.create_positions_index(path, "positions_index.json")
    # reader.convert_index_to_txt(path)
    engine = s.SearchEngine(path, path2, path3)
    engine.run()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python main.py path_to_zip_folder')
        sys.exit(1)
    path = sys.argv[1]
    path2 = sys.argv[2]
    path3 = sys.argv[3]
    run(path, path2, path3)
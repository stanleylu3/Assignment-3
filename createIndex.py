import sys

import FileReader as f

def run(path):
    reader = f.FileReader()
    reader.build_final_index(path)
    reader.create_positions_index('index.json', "positions_index.json")
    reader.convert_index_to_txt('index.json')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python createIndex.py path_to_zip_folder')
        sys.exit(1)
    path = sys.argv[1]
    run(path)
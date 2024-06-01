import sys

import SearchEngine as s

def run(path, path2, path3):
    engine = s.SearchEngine(path, path2, path3)
    engine.run()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python main.py index.txt doc_info.json positions_index.json')
        sys.exit(1)
    path = sys.argv[1]
    path2 = sys.argv[2]
    path3 = sys.argv[3]
    run(path, path2, path3)
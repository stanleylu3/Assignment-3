For our search engine, you will first need to create the index by using the terminal to run the
following command:

python createIndex.py "path_to_zip_folder"

After this program is done running, you should have an index.txt, doc_info.json and positions_index.json.

To run the search engine, run the following command:

python main.py index.txt doc_info.json positions_index.json

Let the search engine start up, and when "Enter your query: " appears, you can start searching.
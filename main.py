import tkinter as tk
import os
from indexer import Indexer
from query_processor import BooleanQueryProcessor
from gui import SearchInterface


def main():
    print("Starting Boolean Retrieval System...")
    indexer = Indexer("Stopword-List.txt")

    # First run: builds inverted index from all documents and caches to disk
    if not os.path.exists("index.json"):
        print("Building index from Trump_Speeches folder...")
        indexer.build_index("Trump_Speeches")
        indexer.save_index("index.json")
    # Subsequent runs: loads cached index (much faster)
    else:
        print("Loading index from index.json...")
        indexer.load_index("index.json")

    processor = BooleanQueryProcessor(indexer.index, indexer.documents, "Stopword-List.txt")

    # Start GUI
    root = tk.Tk()
    SearchInterface(root, processor, indexer.documents)
    root.mainloop()


if __name__ == "__main__":
    main()


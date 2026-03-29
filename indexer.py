from collections import defaultdict
import os
import json
from pre_processor import Preprocessor

"""Builds and manages a position inverted index for documents."""
class Indexer:

    """Initialize the indexer with preprocessor."""
    def __init__(self, stopword_file):
        self.preprocessor = Preprocessor(stopword_file)
        
        # Nested structure: {term: {doc_id: [position1, position2, ...], ...}, ...}
        self.index = defaultdict(lambda: defaultdict(list))
        self.documents = {}

    """Build the inverted index from all text files in the folder, sorted by filename."""
    def build_index(self, folder_path):
        doc_id = 0
        
        # Sort files numerically: speech_0.txt, speech_1.txt, ..., speech_55.txt
        files = sorted(
            os.listdir(folder_path),
            key=lambda f: int(f.split('_')[1].split('.')[0]) 
                if '_' in f and f.endswith('.txt') else float('inf')
        )

        for filename in files:
            filepath = os.path.join(folder_path, filename)
            if not os.path.isfile(filepath):
                continue

            text = open(filepath, 'r', encoding='utf-8').read()
            self.documents[doc_id] = filename
            tokens = self.preprocessor.preprocess(text)

            for position, token in enumerate(tokens):
                self.index[token][doc_id].append(position)

            doc_id += 1

        print("Index built successfully!")

    """Save the index and documents to a JSON file."""
    def save_index(self, filepath):
        # Convert nested defaultdict to regular dict for JSON serialization
        serializable_index = {
            term: dict(doc_dict) 
            for term, doc_dict in self.index.items()
        }
        
        data = {
            "index": serializable_index,
            "documents": self.documents
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        print("Index saved successfully!")

    """Load the index and documents from a JSON file."""
    def load_index(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.index = defaultdict(lambda: defaultdict(list))
        
        # This ensures doc_id values match the original integer IDs from indexing
        for term, docs in data["index"].items():
            for doc_id, positions in docs.items():
                self.index[term][int(doc_id)] = positions

        # Same conversion needed for documents mapping
        self.documents = {int(key): val for key, val in data["documents"].items()}
        print("Index loaded successfully!")
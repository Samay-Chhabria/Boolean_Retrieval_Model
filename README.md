# Boolean Retrieval System for Trump Speeches

A simple information retrieval system that allows searching through a collection of Donald Trump speeches using boolean queries.

## Features

- **Boolean Search**: Use AND, OR, NOT operators to combine search terms
- **Phrase Search**: Find exact phrases by enclosing them in quotes ("united states")
- **Proximity Search**: Find terms within a specific distance (america trump /3)
- **Inverted Index**: Fast searching through pre-built index of all speeches
- **Graphical Interface**: Easy-to-use GUI for entering queries and viewing results

## How to Run

1. Make sure you have Python installed
2. Install required packages: `pip install nltk`
3. Run the main program: `python main.py`

The system will automatically build an index from the Trump speeches on first run, which may take a few minutes. Subsequent runs will load the saved index for faster startup.

## Query Examples

- `america` - Find documents containing "america"
- `america AND trump` - Find documents containing both words
- `america OR united` - Find documents containing either word
- `NOT america` - Find documents that don't contain "america"
- `"united states"` - Find exact phrase "united states"
- `america trump /2` - Find "america" and "trump" within 2 words of each other
- `(america OR united) AND trump` - Combine operators with parentheses

## Project Structure

- `main.py` - Entry point that builds index and starts GUI
- `indexer.py` - Creates inverted index from speech documents
- `query_processor.py` - Processes boolean queries
- `pre_processor.py` - Text preprocessing (stemming, stopword removal)
- `gui.py` - Graphical user interface
- `Trump_Speeches/` - Collection of speech documents
- `Stopword-List.txt` - Common words to ignore during search

## Requirements

- Python 3.x
- NLTK library for text processing
- Tkinter (usually included with Python)

## About

This project demonstrates basic information retrieval concepts including:
- Inverted indexing for efficient search
- Boolean query processing with operator precedence
- Text preprocessing and normalization
- Proximity and phrase matching algorithms

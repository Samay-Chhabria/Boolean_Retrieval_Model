import re
from pre_processor import Preprocessor


class BooleanQueryProcessor:

    """Initialize the Processor with index, documents, and preprocessor."""
    def __init__(self, index, documents, stopword_file):
        self.index = index
        self.documents = documents
        self.preprocessor = Preprocessor(stopword_file)
        self.all_docs = set(documents.keys())
        self.tokens = []
        self.pos = 0

    """Tokenize the query into operators, terms, and special tokens."""
    def tokenize(self, query):
        pattern = r'"[^"]*"|\'[^\']*\'|\(|\)|AND|OR|NOT|/\d+|[a-z0-9_]+'
        self.tokens = re.findall(pattern, query.lower())
        self.pos = 0

    def peek(self):

        # Look ahead without advancing position - allows checking what's next
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):

        # Get current token AND advance position to the next one
        token = self.peek()
        self.pos += 1
        return token

    """Get documents containing the given term."""
    def get_docs_with_term(self, term):
        processed = self.preprocessor.preprocess(term)
        if not processed:
            return set()
        stem = processed[0]
        return set(self.index.get(stem, {}).keys()) if stem in self.index else set()

    """process the query and return the set of matching document IDs."""
    def process(self, query):
        if not query.strip():
            return set()
        self.tokenize(query)
        self.pos = 0
        return self.process_or()

    def process_or(self):

        # OR has LOWEST precedence - evaluated last 
        left = self.process_and()
        while self.peek() == "or":
            self.consume()
            left = left | self.process_and()
        return left

    def process_and(self):

        # AND has MEDIUM precedence - evaluated between OR and NOT
        left = self.process_not()
        while self.peek() == "and":
            self.consume()
            left = left & self.process_not()
        return left

    def process_not(self):

        # NOT has HIGHEST precedence - evaluated first 
        if self.peek() == "not":
            self.consume()
            return self.all_docs - self.process_not()
        return self.process_primary()

    """process primary expressions: terms, phrases, parentheses, proximity."""
    def process_primary(self):
        token = self.peek()
        
        if token == "(":
            self.consume()
            result = self.process_or()
            if self.peek() == ")":
                self.consume()
            return result
        
        if token and token.startswith(('"', "'")):
            phrase = self.consume()[1:-1]
            return self.search_phrase(phrase.split())
        
        if token and token not in ["and", "or", "not", ")", None]:
            term = self.consume()
            if self.peek() and self.peek() not in ["and", "or", "not", ")", None] and not self.peek().startswith(("/", '"', "'")):
                term2 = self.consume()
                if self.peek() and self.peek().startswith("/"):
                    k_str = self.consume()
                    k = int(k_str[1:])
                    return self.search_proximity(term, term2, k)
                else:
                    # Two consecutive terms mean AND
                    return self.get_docs_with_term(term) & self.get_docs_with_term(term2)
            else:
                return self.get_docs_with_term(term)

    """Find documents where term1 and term2 appear within k words of each other."""
    def search_proximity(self, term1, term2, k):
        stem1 = self.get_stem(term1)
        stem2 = self.get_stem(term2)
        
        if not stem1 or not stem2 or stem1 not in self.index or stem2 not in self.index:
            return set()
        
        docs1 = self.index[stem1]
        docs2 = self.index[stem2]
        common_docs = set(docs1.keys()) & set(docs2.keys())
        
        result = set()
        for doc in common_docs:
            for pos1 in docs1[doc]:
                for pos2 in docs2[doc]:
                    # Check if term2 occurs within k words after term1 in the same document
                    # The '+1' adjusts for positions being 0-indexed so a gap of k words is correctly counted
                    if 0 <= (pos2 - pos1) <= k+1:
                        result.add(doc)
                        break  # Found term2 close enough, move to next doc
                if doc in result:
                    break  # Exit inner loop
        
        return result
    
    """Find documents containing the exact phrase."""
    """A small catch is that we need to write the query in quotes like example: "Hillary Clinton" to search for the exact phrase. 
       Otherwise, it will be treated as two separate terms with an implicit AND between them."""
    def search_phrase(self, terms):
        if not terms:
            return set()
        
        stems = []
        for term in terms:
            stem = self.get_stem(term)
            if not stem:
                return set()
            stems.append(stem)
        
        # Check if all terms exist in index
        for stem in stems:
            if stem not in self.index:
                return set()
        
        # Find documents containing all terms
        common_docs = set(self.index[stems[0]].keys())
        for stem in stems[1:]:
            common_docs &= set(self.index[stem].keys())
        
        if not common_docs:
            return set()
        
        result = set()
        for doc in common_docs:
            positions = [self.index[stem][doc] for stem in stems]
            
            # Check if terms appear consecutively: if first word at position 10,
            # then second must be at 11 etc.
            for start_pos in positions[0]:
                if all(start_pos + i in positions[i] for i in range(1, len(stems))):
                    result.add(doc)
                    break
        
        return result

    """Get the stemmed version of a term."""
    def get_stem(self, term):
        processed = self.preprocessor.preprocess(term)
        return processed[0] if processed else None
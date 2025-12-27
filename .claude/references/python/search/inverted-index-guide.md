---
title: "Inverted Index Implementation Guide"
description: "Complete guide to building inverted indexes for fast full-text search"
type: "concept-guide"
tags: ["python", "inverted-index", "search", "indexing", "data-structures", "algorithms"]
category: "python"
subcategory: "search"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
sources:
  - name: "Whoosh Documentation"
    url: "https://whoosh.readthedocs.io/"
related: ["tf-idf-implementation-guide.md"]
author: "unknown"
contributors: []
---

# Inverted Index Implementation Guide

An inverted index is a data structure that maps terms to the documents containing them, enabling fast full-text search. It's the core data structure powering search engines, from Google to local document search. ([Whoosh Docs][1])

## Core Concept

### Forward vs. Inverted Index

**Forward Index** (Document → Terms):
```
doc1: ["python", "programming", "language"]
doc2: ["python", "data", "science"]
doc3: ["java", "programming", "language"]
```

**Inverted Index** (Term → Documents):
```
"python":      {doc1, doc2}
"programming": {doc1, doc3}
"language":    {doc1, doc3}
"data":        {doc2}
"science":     {doc2}
"java":        {doc3}
```

The inverted index allows immediate lookup: "Which documents contain 'python'?" → `{doc1, doc2}` ([Whoosh Docs][1])

### Why "Inverted"?

Traditional indexing maps documents to their contents (like a book's table of contents). An inverted index reverses this: it maps contents to documents (like a book's index at the back).

## Basic Implementation

### Simple Inverted Index

```python
from collections import defaultdict
from typing import Dict, Set, List

class InvertedIndex:
    """Basic inverted index for full-text search."""

    def __init__(self):
        # Maps term -> set of document IDs
        self.index: Dict[str, Set[str]] = defaultdict(set)
        # Maps document ID -> original text
        self.documents: Dict[str, str] = {}

    def tokenize(self, text: str) -> List[str]:
        """Simple tokenization: lowercase and split."""
        return text.lower().split()

    def add_document(self, doc_id: str, text: str):
        """Add document to index."""
        # Store original document
        self.documents[doc_id] = text

        # Extract unique terms
        terms = set(self.tokenize(text))

        # Update inverted index
        for term in terms:
            self.index[term].add(doc_id)

    def search(self, query: str) -> Set[str]:
        """Find documents containing all query terms (AND query)."""
        query_terms = self.tokenize(query)

        if not query_terms:
            return set()

        # Start with documents containing first term
        results = self.index.get(query_terms[0], set()).copy()

        # Intersect with documents containing other terms
        for term in query_terms[1:]:
            results &= self.index.get(term, set())

        return results

    def search_or(self, query: str) -> Set[str]:
        """Find documents containing any query term (OR query)."""
        query_terms = self.tokenize(query)
        results = set()

        for term in query_terms:
            results |= self.index.get(term, set())

        return results


# Usage
index = InvertedIndex()
index.add_document("doc1", "Python is a programming language")
index.add_document("doc2", "Python is used for data science")
index.add_document("doc3", "Java is a programming language")

# AND search: documents containing both terms
results = index.search("Python programming")
print(results)  # {'doc1'}

# OR search: documents containing either term
results = index.search_or("Python Java")
print(results)  # {'doc1', 'doc2', 'doc3'}
```

## Enhanced Implementation

### With Positional Information

Track term positions for phrase queries and proximity search:

```python
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class PositionalIndex:
    """Inverted index with term positions."""

    def __init__(self):
        # Maps term -> {doc_id: [positions]}
        self.index: Dict[str, Dict[str, List[int]]] = defaultdict(lambda: defaultdict(list))
        self.documents: Dict[str, str] = {}

    def add_document(self, doc_id: str, text: str):
        """Index document with term positions."""
        self.documents[doc_id] = text
        terms = self.tokenize(text)

        for position, term in enumerate(terms):
            self.index[term][doc_id].append(position)

    def phrase_search(self, phrase: str) -> Set[str]:
        """Find documents containing exact phrase."""
        terms = self.tokenize(phrase)

        if not terms:
            return set()

        # Get documents containing all terms
        candidates = set(self.index[terms[0]].keys())
        for term in terms[1:]:
            candidates &= set(self.index[term].keys())

        # Check if terms appear consecutively
        results = set()
        for doc_id in candidates:
            if self._has_phrase(doc_id, terms):
                results.add(doc_id)

        return results

    def _has_phrase(self, doc_id: str, terms: List[str]) -> bool:
        """Check if terms appear consecutively in document."""
        # Get positions of first term
        first_positions = self.index[terms[0]][doc_id]

        for start_pos in first_positions:
            # Check if subsequent terms appear at consecutive positions
            match = True
            for i, term in enumerate(terms[1:], start=1):
                expected_pos = start_pos + i
                if expected_pos not in self.index[term][doc_id]:
                    match = False
                    break

            if match:
                return True

        return False

    def proximity_search(self, term1: str, term2: str, max_distance: int) -> Set[str]:
        """Find documents where terms appear within max_distance of each other."""
        docs1 = set(self.index[term1].keys())
        docs2 = set(self.index[term2].keys())
        candidates = docs1 & docs2

        results = set()
        for doc_id in candidates:
            positions1 = self.index[term1][doc_id]
            positions2 = self.index[term2][doc_id]

            # Check if any positions are within distance
            for pos1 in positions1:
                for pos2 in positions2:
                    if abs(pos1 - pos2) <= max_distance:
                        results.add(doc_id)
                        break

        return results


# Usage
index = PositionalIndex()
index.add_document("doc1", "Python is a programming language for beginners")
index.add_document("doc2", "Python programming is fun")

# Exact phrase search
results = index.phrase_search("programming language")
print(results)  # {'doc1'}

# Proximity search (terms within 2 words)
results = index.proximity_search("Python", "programming", max_distance=2)
print(results)  # {'doc1', 'doc2'}
```

### With Term Frequencies

Store term frequencies for TF-IDF scoring:

```python
from collections import defaultdict, Counter
from typing import Dict, Counter as CounterType

class FrequencyIndex:
    """Inverted index with term frequencies."""

    def __init__(self):
        # Maps term -> {doc_id: frequency}
        self.index: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.documents: Dict[str, str] = {}
        self.doc_lengths: Dict[str, int] = {}

    def add_document(self, doc_id: str, text: str):
        """Index document with term frequencies."""
        self.documents[doc_id] = text
        terms = self.tokenize(text)
        self.doc_lengths[doc_id] = len(terms)

        # Count term frequencies
        term_counts: CounterType[str] = Counter(terms)

        # Update index
        for term, count in term_counts.items():
            self.index[term][doc_id] = count

    def get_term_frequency(self, term: str, doc_id: str) -> int:
        """Get frequency of term in document."""
        return self.index[term].get(doc_id, 0)

    def get_document_frequency(self, term: str) -> int:
        """Get number of documents containing term."""
        return len(self.index[term])

    def get_postings(self, term: str) -> Dict[str, int]:
        """Get all document IDs and frequencies for term."""
        return dict(self.index[term])
```

## Workbench Search API Implementation

The project uses an in-memory inverted index for Phase 2:

```python
from collections import defaultdict
from pathlib import Path
from typing import Dict, Set

class SearchIndex:
    """In-memory inverted index for workbench files."""

    def __init__(self, workbench_path: Path, allowed_dirs: list[str]):
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.documents: Dict[str, Document] = {}
        self.workbench_path = workbench_path
        self.allowed_dirs = allowed_dirs

    def build_index(self):
        """Build index from workbench files."""
        for dir_name in self.allowed_dirs:
            dir_path = self.workbench_path / dir_name

            for file_path in dir_path.rglob("*"):
                if not file_path.is_file():
                    continue

                try:
                    # Read file content
                    content = file_path.read_text(encoding="utf-8")

                    # Extract metadata
                    metadata = extract_file_metadata(file_path)

                    # Tokenize and index
                    tokens = self._tokenize(content)
                    term_frequencies = self._calculate_term_frequency(tokens)

                    # Store document
                    doc_id = str(file_path.relative_to(self.workbench_path))
                    self.documents[doc_id] = Document(
                        path=doc_id,
                        name=file_path.name,
                        content=content,
                        metadata=metadata,
                        term_frequencies=term_frequencies,
                        modified_time=file_path.stat().st_mtime,
                        is_file=True
                    )

                    # Update inverted index
                    for term in term_frequencies.keys():
                        self.inverted_index[term].add(doc_id)

                except Exception as e:
                    logger.warning(f"Error indexing {file_path}: {e}")

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into searchable terms."""
        # Lowercase
        text = text.lower()

        # Remove punctuation (keep alphanumeric and hyphens)
        text = re.sub(r'[^a-z0-9\s\-]', ' ', text)

        # Split and filter
        tokens = [
            token for token in text.split()
            if len(token) > 1  # Filter single characters
        ]

        return tokens
```

**Design Decisions**:
- **In-memory**: Fast access, acceptable for <1000 files (~1-2MB per 100 files)
- **Simple tokenization**: Lowercase + alphanumeric + hyphens
- **Term-document pairs only**: No positional info (simplifies implementation)
- **Metadata integration**: Store FileMetadata with each document for filtering

([Project Phase 2 Spec])

## Advanced Features

### Compressed Posting Lists

For large-scale indexes, compress document ID lists:

```python
def encode_postings(doc_ids: List[int]) -> bytes:
    """Compress sorted document IDs using delta encoding."""
    if not doc_ids:
        return b''

    deltas = [doc_ids[0]]
    for i in range(1, len(doc_ids)):
        deltas.append(doc_ids[i] - doc_ids[i-1])

    # Use variable-byte encoding
    return variable_byte_encode(deltas)

def variable_byte_encode(numbers: List[int]) -> bytes:
    """Encode integers using variable-byte encoding."""
    result = bytearray()
    for num in numbers:
        while num >= 128:
            result.append((num % 128) | 0x80)
            num //= 128
        result.append(num)
    return bytes(result)
```

### Skip Lists

Optimize intersection of large posting lists:

```python
class SkipList:
    """Skip list for efficient posting list traversal."""

    def __init__(self, postings: List[int], skip_distance: int = 3):
        self.postings = postings
        self.skip_pointers = self._build_skip_pointers(skip_distance)

    def _build_skip_pointers(self, distance: int) -> Dict[int, int]:
        """Build skip pointers every 'distance' elements."""
        pointers = {}
        for i in range(0, len(self.postings), distance):
            if i + distance < len(self.postings):
                pointers[i] = i + distance
        return pointers

    def intersect(self, other: 'SkipList') -> List[int]:
        """Intersect two posting lists using skip pointers."""
        result = []
        i, j = 0, 0

        while i < len(self.postings) and j < len(other.postings):
            if self.postings[i] == other.postings[j]:
                result.append(self.postings[i])
                i += 1
                j += 1
            elif self.postings[i] < other.postings[j]:
                # Try to skip ahead
                if i in self.skip_pointers and self.postings[self.skip_pointers[i]] <= other.postings[j]:
                    i = self.skip_pointers[i]
                else:
                    i += 1
            else:
                if j in other.skip_pointers and other.postings[other.skip_pointers[j]] <= self.postings[i]:
                    j = other.skip_pointers[j]
                else:
                    j += 1

        return result
```

### Field-Specific Indexing

Index different document fields separately:

```python
class FieldedIndex:
    """Inverted index with field-specific search."""

    def __init__(self):
        self.indexes: Dict[str, Dict[str, Set[str]]] = {
            'title': defaultdict(set),
            'content': defaultdict(set),
            'tags': defaultdict(set)
        }

    def add_document(self, doc_id: str, title: str, content: str, tags: List[str]):
        """Index document with separate fields."""
        # Index title
        for term in self.tokenize(title):
            self.indexes['title'][term].add(doc_id)

        # Index content
        for term in self.tokenize(content):
            self.indexes['content'][term].add(doc_id)

        # Index tags (exact match)
        for tag in tags:
            self.indexes['tags'][tag.lower()].add(doc_id)

    def search_field(self, field: str, query: str) -> Set[str]:
        """Search specific field only."""
        terms = self.tokenize(query)
        results = set()
        for term in terms:
            results |= self.indexes[field].get(term, set())
        return results

    def search_boosted(self, query: str) -> List[Tuple[str, float]]:
        """Search with field-specific boosting."""
        terms = self.tokenize(query)
        scores: Dict[str, float] = defaultdict(float)

        for term in terms:
            # Title matches: 3x weight
            for doc_id in self.indexes['title'].get(term, set()):
                scores[doc_id] += 3.0

            # Content matches: 1x weight
            for doc_id in self.indexes['content'].get(term, set()):
                scores[doc_id] += 1.0

            # Tag matches: 2x weight
            for doc_id in self.indexes['tags'].get(term, set()):
                scores[doc_id] += 2.0

        # Sort by score
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

## Performance Optimization

### Memory-Efficient Storage

Use sets for posting lists (faster membership testing):

```python
# Good: O(1) membership test
inverted_index: Dict[str, Set[str]] = defaultdict(set)

# Bad: O(n) membership test
inverted_index: Dict[str, List[str]] = defaultdict(list)
```

### Incremental Indexing

Add documents without rebuilding entire index:

```python
class IncrementalIndex:
    """Support incremental document additions."""

    def add_document(self, doc_id: str, text: str):
        """Add single document to existing index."""
        terms = set(self.tokenize(text))

        for term in terms:
            self.index[term].add(doc_id)

        self.documents[doc_id] = text

    def remove_document(self, doc_id: str):
        """Remove document from index."""
        if doc_id not in self.documents:
            return

        # Remove from posting lists
        terms = set(self.tokenize(self.documents[doc_id]))
        for term in terms:
            self.index[term].discard(doc_id)

            # Clean up empty posting lists
            if not self.index[term]:
                del self.index[term]

        # Remove document
        del self.documents[doc_id]

    def update_document(self, doc_id: str, text: str):
        """Update existing document."""
        self.remove_document(doc_id)
        self.add_document(doc_id, text)
```

### Posting List Compression

For disk-based indexes, compress posting lists:

```python
import pickle
import gzip

def save_index(index: Dict[str, Set[str]], filepath: str):
    """Save compressed index to disk."""
    with gzip.open(filepath, 'wb') as f:
        pickle.dump(index, f)

def load_index(filepath: str) -> Dict[str, Set[str]]:
    """Load compressed index from disk."""
    with gzip.open(filepath, 'rb') as f:
        return pickle.load(f)
```

## Common Patterns

### AND Query (All Terms Required)

```python
def search_and(index: Dict[str, Set[str]], query_terms: List[str]) -> Set[str]:
    """Documents containing all query terms."""
    if not query_terms:
        return set()

    # Start with smallest posting list (optimization)
    sorted_terms = sorted(query_terms, key=lambda t: len(index.get(t, set())))

    results = index.get(sorted_terms[0], set()).copy()
    for term in sorted_terms[1:]:
        results &= index.get(term, set())

    return results
```

### OR Query (Any Term Matches)

```python
def search_or(index: Dict[str, Set[str]], query_terms: List[str]) -> Set[str]:
    """Documents containing any query term."""
    results = set()
    for term in query_terms:
        results |= index.get(term, set())
    return results
```

### NOT Query (Exclude Terms)

```python
def search_not(
    index: Dict[str, Set[str]],
    include_terms: List[str],
    exclude_terms: List[str],
    all_docs: Set[str]
) -> Set[str]:
    """Documents containing include_terms but not exclude_terms."""
    # Get documents with include terms
    results = search_and(index, include_terms)

    # Remove documents with exclude terms
    for term in exclude_terms:
        results -= index.get(term, set())

    return results
```

## Best Practices

1. **Use sets for posting lists** — O(1) membership testing and set operations
2. **Sort terms by posting list size** — Process smallest lists first for faster AND queries
3. **Store term frequencies** — Required for TF-IDF and other ranking algorithms
4. **Handle encoding errors** — Gracefully skip files with encoding issues
5. **Log index statistics** — Monitor number of terms, documents, and index size
6. **Consider disk vs memory** — In-memory for <10k docs, disk-based for larger corpora
7. **Tokenize consistently** — Use same tokenization for indexing and querying
8. **Clean posting lists** — Remove empty posting lists to save memory

## Troubleshooting

### Issue: Memory Usage Too High

**Solution**: Use disk-based index (Whoosh) or compressed posting lists:

```python
# Instead of storing all documents
# Store only document IDs and fetch content on demand
class ExternalStorage:
    def get_document(self, doc_id: str) -> str:
        return Path(doc_id).read_text()
```

### Issue: Slow AND Queries

**Solution**: Process smallest posting list first:

```python
# Sort terms by posting list size
sorted_terms = sorted(terms, key=lambda t: len(index[t]))
```

### Issue: Index Not Updating

**Solution**: Clear IDF cache when documents change:

```python
def add_document(self, doc_id: str, text: str):
    # ... index document ...
    self.idf_cache.clear()  # Invalidate cached IDF values
```

## References

[1]: https://whoosh.readthedocs.io/ "Whoosh Full-Text Search Documentation"

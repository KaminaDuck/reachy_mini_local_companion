---
title: "TF-IDF Implementation Guide for Python"
description: "Comprehensive guide to TF-IDF algorithms for text search and relevance ranking"
type: "concept-guide"
tags: ["python", "tf-idf", "search", "information-retrieval", "ranking", "text-analysis"]
category: "python"
subcategory: "search"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
sources:
  - name: "Scikit-learn TfidfVectorizer"
    url: "https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html"
  - name: "Whoosh Documentation"
    url: "https://whoosh.readthedocs.io/"
related: ["inverted-index-guide.md"]
author: "unknown"
contributors: []
---

# TF-IDF Implementation Guide for Python

TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic used in information retrieval to measure how important a term is to a document within a collection. This guide covers both custom implementations and library-based approaches. ([Scikit-learn Docs][1])

## Core Concepts

### Term Frequency (TF)

**Definition**: Measures how frequently a term appears in a document.

**Basic Formula**:
```
TF(term, doc) = (number of times term appears in doc) / (total number of terms in doc)
```

**Variants**:
- **Raw Count**: Simply count occurrences
- **Boolean**: 1 if present, 0 if absent
- **Logarithmic**: `1 + log(frequency)` if frequency > 0
- **Augmented**: Prevents bias toward longer documents

**Example**:
```python
# Document: "the cat sat on the mat"
# Term "the" appears 2 times out of 6 words
TF("the") = 2 / 6 = 0.333
```

### Inverse Document Frequency (IDF)

**Definition**: Measures how rare or common a term is across all documents.

**Formula**:
```
IDF(term) = log(total_documents / (1 + documents_containing_term))
```

The `+1` in the denominator prevents division by zero (smoothing). ([Scikit-learn Docs][1])

**Interpretation**:
- **High IDF**: Term is rare, more discriminative
- **Low IDF**: Term is common (like "the"), less useful for distinguishing documents

**Example**:
```python
# 100 total documents, term "python" appears in 10 documents
IDF("python") = log(100 / (1 + 10)) = log(9.09) ≈ 2.21

# Term "the" appears in 95 documents
IDF("the") = log(100 / (1 + 95)) = log(1.04) ≈ 0.04
```

### TF-IDF Score

**Combined Formula**:
```
TF-IDF(term, doc) = TF(term, doc) × IDF(term)
```

**Result**: High scores for terms that are frequent in specific documents but rare across the corpus.

## Custom Implementation

### Basic TF-IDF from Scratch

For lightweight applications with minimal dependencies:

```python
import math
from collections import Counter, defaultdict
from typing import Dict, List, Set

class SimpleTFIDF:
    """Simple TF-IDF implementation with inverted index."""

    def __init__(self):
        self.documents: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.idf_cache: Dict[str, float] = {}
        self.total_docs = 0

    def tokenize(self, text: str) -> List[str]:
        """Basic tokenization: lowercase and split."""
        return text.lower().split()

    def add_document(self, doc_id: str, text: str):
        """Add document to index."""
        tokens = self.tokenize(text)
        self.documents[doc_id] = tokens
        self.total_docs += 1

        # Update inverted index
        for token in set(tokens):
            self.inverted_index[token].add(doc_id)

        # Invalidate IDF cache
        self.idf_cache.clear()

    def calculate_tf(self, term: str, doc_id: str) -> float:
        """Calculate term frequency."""
        tokens = self.documents[doc_id]
        if not tokens:
            return 0.0
        return tokens.count(term) / len(tokens)

    def calculate_idf(self, term: str) -> float:
        """Calculate inverse document frequency with smoothing."""
        if term in self.idf_cache:
            return self.idf_cache[term]

        doc_count = len(self.inverted_index.get(term, set()))
        idf = math.log(self.total_docs / (1 + doc_count))
        self.idf_cache[term] = idf
        return idf

    def calculate_tfidf(self, term: str, doc_id: str) -> float:
        """Calculate TF-IDF score."""
        tf = self.calculate_tf(term, doc_id)
        idf = self.calculate_idf(term)
        return tf * idf

    def search(self, query: str, top_k: int = 10) -> List[tuple]:
        """Search documents and return ranked results."""
        query_terms = self.tokenize(query)

        # Find candidate documents (contain at least one query term)
        candidates = set()
        for term in query_terms:
            candidates.update(self.inverted_index.get(term, set()))

        # Calculate scores
        scores = []
        for doc_id in candidates:
            score = sum(
                self.calculate_tfidf(term, doc_id)
                for term in query_terms
            )
            scores.append((doc_id, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# Usage
index = SimpleTFIDF()
index.add_document("doc1", "Python is a programming language")
index.add_document("doc2", "Python is used for data science")
index.add_document("doc3", "Java is a programming language")

results = index.search("Python programming")
# Returns: [('doc1', score1), ('doc2', score2), ...]
```

### Enhanced Implementation with Normalization

For production use, add vector normalization:

```python
import math
from collections import Counter
from typing import Dict, List

class TFIDFWithNormalization:
    """TF-IDF with L2 normalization for fair comparison."""

    def calculate_document_vector(
        self, doc_id: str, query_terms: List[str]
    ) -> Dict[str, float]:
        """Calculate TF-IDF vector for document."""
        vector = {}
        for term in query_terms:
            tf = self.calculate_tf(term, doc_id)
            idf = self.calculate_idf(term)
            vector[term] = tf * idf
        return vector

    def normalize_vector(self, vector: Dict[str, float]) -> Dict[str, float]:
        """Apply L2 normalization to vector."""
        # Calculate L2 norm (Euclidean length)
        magnitude = math.sqrt(sum(v ** 2 for v in vector.values()))

        if magnitude == 0:
            return vector

        # Normalize each component
        return {term: score / magnitude for term, score in vector.items()}

    def cosine_similarity(
        self, vec1: Dict[str, float], vec2: Dict[str, float]
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        # Dot product
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0) for term in vec1)

        # Magnitudes
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)
```

Normalization ensures longer documents don't automatically score higher. ([Scikit-learn Docs][1])

## Library-Based Implementations

### Scikit-learn TfidfVectorizer

Best for machine learning pipelines and document classification:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create corpus
documents = [
    "Python is a programming language",
    "Python is used for data science",
    "Java is a programming language",
    "Machine learning uses Python",
]

# Initialize vectorizer
vectorizer = TfidfVectorizer(
    lowercase=True,           # Convert to lowercase
    stop_words='english',     # Remove common words
    max_df=0.8,              # Ignore terms in >80% of docs
    min_df=2,                # Require term in >=2 docs
    ngram_range=(1, 2),      # Unigrams and bigrams
    smooth_idf=True,         # Add 1 to document frequencies
    sublinear_tf=False,      # Use raw term frequency
    norm='l2'                # L2 normalization (default)
)

# Fit and transform documents
tfidf_matrix = vectorizer.fit_transform(documents)

# Get vocabulary
vocabulary = vectorizer.get_feature_names_out()
print(vocabulary)
# ['data', 'java', 'language', 'learning', 'machine', 'programming', 'python', 'science', 'used']

# Search with query
query = "Python programming"
query_vector = vectorizer.transform([query])

# Calculate similarities
similarities = cosine_similarity(query_vector, tfidf_matrix)
ranked_indices = similarities.argsort()[0][::-1]

for idx in ranked_indices:
    print(f"Doc {idx}: {documents[idx]} (score: {similarities[0][idx]:.3f})")
```

**Key Parameters**:
- `max_df`: Filter terms appearing in too many documents (e.g., 0.8 = 80%)
- `min_df`: Filter rare terms (absolute count or fraction)
- `max_features`: Limit vocabulary size to top N terms
- `ngram_range`: Capture phrases (1,1)=unigrams, (1,2)=unigrams+bigrams
- `smooth_idf`: Prevents division by zero with +1 smoothing
- `sublinear_tf`: Use log(TF) instead of raw TF
- `norm`: Vector normalization ('l2', 'l1', or None)

([Scikit-learn Docs][1])

### Whoosh Full-Text Search

Best for standalone search applications with rich query language:

```python
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import scoring

# Define schema
schema = Schema(
    id=ID(stored=True),
    content=TEXT(stored=True)
)

# Create index
import os
os.makedirs("indexdir", exist_ok=True)
ix = create_in("indexdir", schema)

# Add documents
writer = ix.writer()
writer.add_document(id="1", content="Python is a programming language")
writer.add_document(id="2", content="Python is used for data science")
writer.add_document(id="3", content="Java is a programming language")
writer.commit()

# Search with TF-IDF scoring
with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
    query = QueryParser("content", ix.schema).parse("Python programming")
    results = searcher.search(query, limit=10)

    for result in results:
        print(f"{result['id']}: {result['content']} (score: {result.score})")
```

**Scoring Options**:
- `scoring.TF_IDF()` — Classic TF-IDF
- `scoring.BM25F()` — BM25 (default, better than TF-IDF)
- `scoring.Frequency()` — Raw term frequency
- `scoring.Cosine()` — Cosine similarity

Whoosh provides a complete search engine with query parsing, highlighting, and faceting. ([Whoosh Docs][2])

## Implementation Comparison

| Approach | Pros | Cons | Use Case |
|----------|------|------|----------|
| **Custom** | Full control, no dependencies, lightweight | Manual implementation, missing features | Simple search, learning, minimal deps |
| **Scikit-learn** | Battle-tested, ML integration, efficient | Requires numpy/scipy, overkill for simple search | Document classification, similarity |
| **Whoosh** | Complete search engine, query language, pure Python | Heavier, disk-based index | Standalone search, rich queries |

## Workbench Search API Implementation

Phase 2 uses a custom in-memory implementation for simplicity and zero external dependencies:

```python
class SearchIndex:
    """In-memory inverted index with TF-IDF scoring."""

    def __init__(self, workbench_path: Path, allowed_dirs: list[str]):
        self.inverted_index: dict[str, set[str]] = defaultdict(set)
        self.documents: dict[str, Document] = {}
        self.workbench_path = workbench_path
        self.allowed_dirs = allowed_dirs

    def _calculate_tf_idf(self, term: str, doc_id: str) -> float:
        """Calculate TF-IDF score for term in document."""
        doc = self.documents[doc_id]

        # Term frequency
        tf = doc.term_frequencies.get(term, 0)

        # Document frequency
        df = len(self.inverted_index.get(term, set()))

        # Inverse document frequency with smoothing
        idf = math.log(len(self.documents) / (1 + df))

        return tf * idf

    def search(self, query: str, limit: int = 20) -> list[SearchResult]:
        """Search index and return ranked results."""
        query_terms = self._tokenize(query)

        # Find candidate documents
        candidates = set()
        for term in query_terms:
            candidates.update(self.inverted_index.get(term, set()))

        # Score and rank
        scores = []
        for doc_id in candidates:
            score = sum(
                self._calculate_tf_idf(term, doc_id)
                for term in query_terms
            )
            scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:limit]
```

**Design Decisions**:
1. **In-memory** — Fast queries, acceptable for <1000 files
2. **No normalization** — Simpler implementation, acceptable for similar-length docs
3. **Additive scoring** — Sum TF-IDF scores across query terms
4. **Smoothing** — +1 in IDF denominator prevents division by zero

([Project Phase 2 Spec])

## Advanced Techniques

### Sublinear TF Scaling

For very long documents, use logarithmic TF:

```python
def sublinear_tf(raw_count: int) -> float:
    """Apply logarithmic scaling to term frequency."""
    if raw_count == 0:
        return 0
    return 1 + math.log(raw_count)
```

This prevents long documents from dominating scores. ([Scikit-learn Docs][1])

### Query Expansion

Improve recall by expanding queries with synonyms:

```python
def expand_query(query: str, synonyms: dict) -> list[str]:
    """Expand query with synonyms."""
    terms = query.lower().split()
    expanded = []
    for term in terms:
        expanded.append(term)
        expanded.extend(synonyms.get(term, []))
    return expanded

# Example
synonyms = {
    "python": ["py", "cpython"],
    "search": ["find", "query", "lookup"]
}
expanded = expand_query("python search", synonyms)
# ['python', 'py', 'cpython', 'search', 'find', 'query', 'lookup']
```

### Phrase Boosting

Give higher weight to exact phrase matches:

```python
def calculate_phrase_bonus(query: str, doc_text: str) -> float:
    """Bonus for exact phrase match."""
    if query.lower() in doc_text.lower():
        return 2.0  # Boost by 2x
    return 1.0

score = base_tfidf_score * calculate_phrase_bonus(query, doc.content)
```

### Field Boosting

Weight different document fields differently:

```python
# Title matches more valuable than body matches
title_score = tfidf(term, doc.title) * 3.0
body_score = tfidf(term, doc.body) * 1.0
total_score = title_score + body_score
```

## Performance Optimization

### Precompute IDF Values

Cache IDF calculations:

```python
class SearchIndex:
    def __init__(self):
        self.idf_cache: dict[str, float] = {}

    def calculate_idf(self, term: str) -> float:
        if term not in self.idf_cache:
            df = len(self.inverted_index.get(term, set()))
            self.idf_cache[term] = math.log(self.total_docs / (1 + df))
        return self.idf_cache[term]
```

Rebuild cache only when documents change.

### Limit Candidate Documents

For large corpora, filter candidates early:

```python
def search_with_threshold(self, query: str, min_score: float = 0.1):
    """Only return results above threshold."""
    candidates = self._get_candidates(query)

    results = []
    for doc_id in candidates:
        score = self._calculate_score(query, doc_id)
        if score >= min_score:
            results.append((doc_id, score))

    return sorted(results, key=lambda x: x[1], reverse=True)
```

### Use Sparse Data Structures

Store only non-zero TF values:

```python
from collections import defaultdict

# Instead of dense array
term_frequencies = defaultdict(int)  # Only stores non-zero counts
```

## Common Pitfalls

### Issue: All Scores Are Similar

**Cause**: Not enough variation in document lengths or term distributions.

**Solution**: Add normalization or use BM25 instead of TF-IDF:

```python
# BM25 formula (better than TF-IDF for varying document lengths)
def bm25_score(tf, df, doc_length, avg_doc_length, k1=1.5, b=0.75):
    idf = math.log((total_docs - df + 0.5) / (df + 0.5))
    normalized_tf = tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc_length / avg_doc_length))
    return idf * normalized_tf
```

### Issue: Common Words Rank Too High

**Cause**: Not filtering stopwords or very common terms.

**Solution**: Use stopword lists and max_df filtering:

```python
STOPWORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'}

def tokenize(text):
    tokens = text.lower().split()
    return [t for t in tokens if t not in STOPWORDS]
```

### Issue: Poor Phrase Matching

**Cause**: TF-IDF treats queries as bag-of-words.

**Solution**: Add phrase detection or use bigrams:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Unigrams + bigrams
```

## Best Practices

1. **Always use smoothing** — Add +1 to document frequencies to avoid division by zero
2. **Normalize vectors** — Use L2 normalization for fair comparison across document lengths
3. **Filter common terms** — Remove stopwords or use max_df parameter
4. **Cache IDF values** — Precompute and store IDF values for faster queries
5. **Consider BM25** — Often performs better than TF-IDF for search applications
6. **Use sparse matrices** — Essential for large vocabularies (thousands of terms)
7. **Validate on real data** — Test with actual documents from your corpus
8. **Monitor query performance** — Profile slow queries and optimize candidate selection

## References

[1]: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html "Scikit-learn TfidfVectorizer Documentation"
[2]: https://whoosh.readthedocs.io/ "Whoosh Full-Text Search Documentation"

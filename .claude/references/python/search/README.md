---
author: unknown
category: python
contributors: []
description: Index of search algorithms, ranking functions, and indexing data structures
last_updated: '2025-11-03'
related:
- README.md
sources: []
status: stable
subcategory: search
tags:
- python
- search
- ranking
- indexing
- information-retrieval
- index
title: Python Search & Information Retrieval Index
type: meta
version: '1.0'
---

# Python Search & Information Retrieval

Reference documentation for implementing search functionality, ranking algorithms, and indexing data structures in Python.

## Available References

### Ranking Algorithms

**[TF-IDF Implementation Guide](tf-idf-implementation-guide.md)**
Comprehensive guide to Term Frequency-Inverse Document Frequency for text search and relevance ranking. Covers custom implementations, scikit-learn TfidfVectorizer, and Whoosh integration.

**Topics:**
- TF-IDF formula and concepts
- Custom implementation from scratch
- Scikit-learn TfidfVectorizer usage
- Whoosh full-text search
- Normalization techniques
- Performance optimization

**[BM25 Ranking Algorithm Guide](bm25-ranking-guide.md)**
Complete guide to BM25 (Best Matching 25) probabilistic ranking function. The industry standard for modern search engines with superior document length normalization.

**Topics:**
- BM25 formula and parameters (k₁, b)
- Advantages over TF-IDF
- Custom implementation
- rank-bm25 and BM25S libraries
- BM25 variants (BM25+, BM25F)
- Parameter tuning strategies

### Data Structures

**[Inverted Index Implementation Guide](inverted-index-guide.md)**
Complete guide to building inverted indexes for fast full-text search. The core data structure powering search engines from Google to local document search.

**Topics:**
- Inverted index concept and structure
- Basic implementation
- Positional indexing for phrase search
- Term frequency tracking
- Advanced features (skip lists, compression)
- Field-specific indexing
- Incremental updates

## Quick Comparison

### Ranking Functions

| Algorithm | Best For | Strengths | Weaknesses |
|-----------|----------|-----------|------------|
| **TF-IDF** | Classification, similarity | Simple, interpretable | No length normalization |
| **BM25** | Document retrieval | Length normalization, tunable | More complex |
| **BM25+** | Mixed-length docs | Improved lower bound | Additional parameter |
| **BM25F** | Multi-field docs | Field-specific weights | Complex setup |

### Python Libraries

| Library | Purpose | Dependencies | Performance |
|---------|---------|--------------|-------------|
| **scikit-learn** | TF-IDF for ML | numpy, scipy | Good |
| **rank-bm25** | BM25 variants | None (pure Python) | Moderate |
| **BM25S** | High-perf BM25 | numpy, scipy | Excellent |
| **Whoosh** | Full-text search | Pure Python | Good |

## Implementation Patterns

### Simple Search (No Dependencies)

For lightweight applications:

```python
from collections import defaultdict, Counter
import math

class SimpleSearch:
    """Minimal search with TF-IDF."""

    def __init__(self):
        self.inverted_index = defaultdict(set)
        self.documents = {}

    def add_document(self, doc_id, text):
        tokens = text.lower().split()
        self.documents[doc_id] = tokens
        for token in set(tokens):
            self.inverted_index[token].add(doc_id)

    def search(self, query):
        query_tokens = query.lower().split()
        candidates = set()
        for token in query_tokens:
            candidates.update(self.inverted_index.get(token, set()))

        # Simple scoring
        scores = []
        for doc_id in candidates:
            score = sum(
                1 for token in query_tokens
                if token in self.documents[doc_id]
            )
            scores.append((doc_id, score))

        return sorted(scores, key=lambda x: x[1], reverse=True)
```

### Production Search (BM25 + Inverted Index)

For Workbench Search API Phase 2:

```python
from collections import defaultdict
import math

class SearchIndex:
    """Production-ready search with BM25."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.inverted_index = defaultdict(set)
        self.documents = {}
        self.doc_lengths = {}
        self.avgdl = 0

    def build_index(self, documents):
        """Build inverted index from documents."""
        total_length = 0

        for doc_id, text in documents.items():
            tokens = self.tokenize(text)
            self.documents[doc_id] = Counter(tokens)
            self.doc_lengths[doc_id] = len(tokens)
            total_length += len(tokens)

            for token in set(tokens):
                self.inverted_index[token].add(doc_id)

        self.avgdl = total_length / len(documents)

    def search(self, query, top_k=10):
        """Search with BM25 ranking."""
        query_tokens = self.tokenize(query)

        # Get candidates
        candidates = set()
        for token in query_tokens:
            candidates.update(self.inverted_index.get(token, set()))

        # Score candidates
        scores = []
        for doc_id in candidates:
            score = self.calculate_bm25(query_tokens, doc_id)
            scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def calculate_bm25(self, query_tokens, doc_id):
        """Calculate BM25 score."""
        score = 0.0
        doc_len = self.doc_lengths[doc_id]

        for token in query_tokens:
            if token not in self.documents[doc_id]:
                continue

            tf = self.documents[doc_id][token]
            df = len(self.inverted_index[token])
            idf = math.log((len(self.documents) - df + 0.5) / (df + 0.5) + 1)

            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)

            score += idf * (numerator / denominator)

        return score
```

### Using Libraries

For rapid development:

```python
from rank_bm25 import BM25Okapi

# Tokenize corpus
corpus = [
    ["python", "programming", "language"],
    ["python", "data", "science"],
    ["java", "programming"],
]

# Create and query
bm25 = BM25Okapi(corpus)
query = ["python", "programming"]
scores = bm25.get_scores(query)
top_docs = bm25.get_top_n(query, corpus, n=10)
```

## Common Use Cases

### Document Retrieval

Use **BM25** for ranking search results:

```python
from rank_bm25 import BM25Okapi

documents = [...]  # Your document collection
tokenized = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized)

query = "search term"
results = bm25.get_top_n(query.split(), documents, n=10)
```

### Document Classification

Use **TF-IDF** with machine learning:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_documents)
X_test = vectorizer.transform(test_documents)

clf = MultinomialNB()
clf.fit(X_train, train_labels)
predictions = clf.predict(X_test)
```

### Content Recommendation

Use **TF-IDF** + cosine similarity:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Find similar documents
similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
similar_docs = similarities.argsort()[0][-5:][::-1]
```

## Workbench Search API

Phase 2 uses custom in-memory BM25 implementation:

**Design:**
- In-memory inverted index
- BM25 ranking with standard parameters (k₁=1.5, b=0.75)
- Simple tokenization (lowercase + alphanumeric)
- Metadata filtering integration
- Fast for <1000 documents

**Files:**
- `agentenv_api/services/search_index.py` - Search index implementation
- `agentenv_api/models/search.py` - Search result models (Phase 1)
- `agentenv_api/services/metadata_parser.py` - Metadata extraction (Phase 1)

See `specs/workbench-search-api/02-backend-search-engine.md` for details.

## Performance Guidelines

### Small Collections (<1,000 docs)
- **Use:** Custom in-memory implementation
- **Ranking:** BM25 or simple TF-IDF
- **Index:** Dict-based inverted index

### Medium Collections (1,000-100,000 docs)
- **Use:** rank-bm25 or BM25S library
- **Ranking:** BM25 with tuned parameters
- **Index:** In-memory with compression

### Large Collections (>100,000 docs)
- **Use:** Whoosh or Elasticsearch
- **Ranking:** BM25F for multi-field
- **Index:** Disk-based with caching

## Selection Guide

**Choose TF-IDF when:**
- Implementing document classification
- Computing document similarity
- Simple, interpretable scores needed
- Integrating with scikit-learn pipelines

**Choose BM25 when:**
- Building search/retrieval systems
- Documents vary in length
- Need production-quality ranking
- Want tunable parameters

**Choose Inverted Index when:**
- Need fast term lookup
- Implementing search from scratch
- Optimizing query performance
- Building custom search features

## Related References

- [PyYAML Library Guide](../yaml/pyyaml-library-guide.md) - For parsing configuration
- [Python-Frontmatter Guide](../yaml/python-frontmatter-library-guide.md) - For document metadata
- [Pydantic Library Guide](../pydantic/pydantic-library-guide.md) - For data validation
- [Python Index](../README.md) - Main Python references

## External Resources

### Documentation
- [Scikit-learn Text Feature Extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
- [Whoosh Documentation](https://whoosh.readthedocs.io/)
- [rank-bm25 GitHub](https://github.com/dorianbrown/rank_bm25)
- [BM25S Documentation](https://bm25s.github.io/)

### Research Papers
- Robertson & Zaragoza (2009) - "The Probabilistic Relevance Framework: BM25 and Beyond"
- Manning et al. (2008) - "Introduction to Information Retrieval"

### Tutorials
- [Scikit-learn TF-IDF Tutorial](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
- [Understanding BM25](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)
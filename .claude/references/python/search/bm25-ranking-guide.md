---
title: "BM25 Ranking Algorithm Guide"
description: "Complete guide to BM25 (Best Matching 25) for document ranking and search"
type: "concept-guide"
tags: ["python", "bm25", "search", "ranking", "information-retrieval", "okapi"]
category: "python"
subcategory: "search"
version: "1.0"
last_updated: "2025-11-03"
status: "stable"
sources:
  - name: "Wikipedia - Okapi BM25"
    url: "https://en.wikipedia.org/wiki/Okapi_BM25"
  - name: "rank-bm25 PyPI"
    url: "https://pypi.org/project/rank-bm25/"
  - name: "BM25S Documentation"
    url: "https://bm25s.github.io/"
related: ["tf-idf-implementation-guide.md", "inverted-index-guide.md"]
author: "unknown"
contributors: []
---

# BM25 Ranking Algorithm Guide

BM25 (Best Matching 25), also known as Okapi BM25, is a probabilistic ranking function used to estimate document relevance for search queries. It's the industry standard for modern search engines, improving upon TF-IDF with better document length normalization and term frequency saturation. ([Wikipedia BM25][1])

## Overview

BM25 was developed in the 1970s-80s by Stephen E. Robertson, Karen Spärck Jones, and others as part of the probabilistic retrieval framework. The name "Okapi" comes from the search system where it was first implemented at City University London. ([Wikipedia BM25][1])

**Key Advantages over TF-IDF:**
- **Length normalization** - Prevents longer documents from unfairly dominating rankings
- **Term frequency saturation** - Diminishing returns for repeated terms
- **Probabilistic foundation** - Based on Binary Independence Model, not heuristics
- **Tunable parameters** - Adjustable for different document collections

## Core Formula

The BM25 score for a document D given query Q is:

```
score(D, Q) = Σ IDF(qi) × [f(qi, D) × (k₁ + 1)] / [f(qi, D) + k₁ × (1 - b + b × |D| / avgdl)]
```

**Components:**
- `qi` - Each term in the query
- `f(qi, D)` - Frequency of term qi in document D
- `|D|` - Length of document D (in words)
- `avgdl` - Average document length in the corpus
- `k₁` - Term frequency saturation parameter (typically 1.2 to 2.0)
- `b` - Length normalization parameter (typically 0.75)

([Wikipedia BM25][1])

### IDF Component

BM25 uses a probabilistic IDF formula:

```
IDF(qi) = ln[(N - n(qi) + 0.5) / (n(qi) + 0.5) + 1]
```

Where:
- `N` - Total number of documents
- `n(qi)` - Number of documents containing term qi

This differs slightly from classic TF-IDF's IDF calculation. ([Wikipedia BM25][1])

## Parameters Explained

### k₁ (Term Frequency Saturation)

**Range:** Typically 1.2 to 2.0
**Default:** 1.5 or 1.2

Controls how quickly additional term occurrences contribute diminishing value:

- **k₁ = 0**: Binary weighting (term present or absent)
- **Low k₁ (< 1.0)**: Rapid saturation, additional occurrences matter less
- **High k₁ (> 2.0)**: Slower saturation, similar to raw TF

**Example:**
```python
# With k₁ = 1.2
Term appears 1 time:  score contribution ≈ 0.545
Term appears 2 times: score contribution ≈ 0.727  (+33%)
Term appears 5 times: score contribution ≈ 0.882  (+21%)
Term appears 10 times: score contribution ≈ 0.917  (+4%)

# Saturation effect: going from 5→10 adds less than going from 1→2
```

### b (Length Normalization)

**Range:** 0.0 to 1.0
**Default:** 0.75

Controls how much document length affects the score:

- **b = 0**: No length normalization (like classic TF)
- **b = 1**: Full length normalization (strongly penalize long docs)
- **b = 0.75**: Balanced normalization (most common)

**When to adjust:**
- **Increase b** (closer to 1.0) - If long documents are ranking too high
- **Decrease b** (closer to 0.0) - If short documents are unfairly favored
- **b = 0.5** - Good for collections with similar-length documents

([Wikipedia BM25][1])

## Custom Implementation

### Basic BM25 from Scratch

```python
import math
from collections import Counter, defaultdict
from typing import List, Dict, Set

class BM25:
    """Basic BM25 implementation for document ranking."""

    def __init__(self, corpus: List[List[str]], k1: float = 1.5, b: float = 0.75):
        """
        Initialize BM25 with document corpus.

        Args:
            corpus: List of tokenized documents (list of word lists)
            k1: Term frequency saturation parameter (1.2-2.0)
            b: Length normalization parameter (0.0-1.0)
        """
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.corpus_size = len(corpus)
        self.avgdl = sum(len(doc) for doc in corpus) / self.corpus_size
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = [len(doc) for doc in corpus]

        # Calculate document frequencies and IDF
        self._calc_idf()

    def _calc_idf(self):
        """Calculate IDF for all terms in corpus."""
        # Count document frequencies
        df = defaultdict(int)
        for doc in self.corpus:
            unique_terms = set(doc)
            for term in unique_terms:
                df[term] += 1

        # Calculate IDF using BM25 formula
        for term, freq in df.items():
            self.idf[term] = math.log(
                (self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0
            )

    def score(self, query: List[str], doc_idx: int) -> float:
        """
        Calculate BM25 score for a document given a query.

        Args:
            query: Tokenized query (list of terms)
            doc_idx: Index of document in corpus

        Returns:
            BM25 score
        """
        score = 0.0
        doc = self.corpus[doc_idx]
        doc_len = self.doc_len[doc_idx]

        # Count term frequencies in document
        term_freqs = Counter(doc)

        for term in query:
            if term not in term_freqs:
                continue

            # Get term frequency and IDF
            tf = term_freqs[term]
            idf = self.idf.get(term, 0)

            # BM25 formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (
                1 - self.b + self.b * doc_len / self.avgdl
            )

            score += idf * (numerator / denominator)

        return score

    def get_scores(self, query: List[str]) -> List[float]:
        """Calculate BM25 scores for all documents."""
        return [self.score(query, i) for i in range(self.corpus_size)]

    def get_top_n(self, query: List[str], n: int = 10) -> List[tuple]:
        """
        Get top N documents for query.

        Returns:
            List of (doc_idx, score) tuples, sorted by score descending
        """
        scores = self.get_scores(query)
        scored_docs = [(i, score) for i, score in enumerate(scores)]
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:n]


# Usage
corpus = [
    ["python", "is", "a", "programming", "language"],
    ["python", "is", "used", "for", "data", "science"],
    ["java", "is", "a", "programming", "language"],
    ["machine", "learning", "uses", "python"],
]

bm25 = BM25(corpus)
query = ["python", "programming"]
scores = bm25.get_scores(query)
print(scores)  # [score1, score2, score3, score4]

# Get top results
top_docs = bm25.get_top_n(query, n=2)
print(top_docs)  # [(0, 2.45), (1, 1.23)]
```

### BM25 with Preprocessing

Include tokenization and preprocessing:

```python
import re
from typing import List

class BM25WithPreprocessing(BM25):
    """BM25 with built-in text preprocessing."""

    STOPWORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
        'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on',
        'that', 'the', 'to', 'was', 'will', 'with'
    }

    def __init__(
        self,
        documents: List[str],
        k1: float = 1.5,
        b: float = 0.75,
        use_stopwords: bool = True
    ):
        """
        Initialize with raw text documents.

        Args:
            documents: List of raw text documents
            k1: Term frequency saturation
            b: Length normalization
            use_stopwords: Whether to filter stopwords
        """
        self.use_stopwords = use_stopwords
        corpus = [self.tokenize(doc) for doc in documents]
        super().__init__(corpus, k1, b)

    def tokenize(self, text: str) -> List[str]:
        """Tokenize and preprocess text."""
        # Lowercase
        text = text.lower()

        # Remove punctuation, keep alphanumeric and hyphens
        text = re.sub(r'[^a-z0-9\s\-]', ' ', text)

        # Split into tokens
        tokens = text.split()

        # Filter stopwords and short tokens
        if self.use_stopwords:
            tokens = [
                t for t in tokens
                if len(t) > 1 and t not in self.STOPWORDS
            ]
        else:
            tokens = [t for t in tokens if len(t) > 1]

        return tokens

    def search(self, query_text: str, n: int = 10) -> List[tuple]:
        """
        Search with raw text query.

        Args:
            query_text: Raw query string
            n: Number of results to return

        Returns:
            List of (doc_idx, score) tuples
        """
        query_tokens = self.tokenize(query_text)
        return self.get_top_n(query_tokens, n)


# Usage
documents = [
    "Python is a high-level programming language",
    "Python is widely used for data science and machine learning",
    "Java is an object-oriented programming language",
    "Machine learning models are built with Python libraries",
]

bm25 = BM25WithPreprocessing(documents)
results = bm25.search("Python programming")

for idx, score in results:
    print(f"Doc {idx} (score: {score:.3f}): {documents[idx]}")
```

## Library-Based Implementations

### rank-bm25 Library

Most popular BM25 library for Python:

```python
from rank_bm25 import BM25Okapi

# Tokenize documents
corpus = [
    ["python", "is", "programming", "language"],
    ["python", "used", "data", "science"],
    ["java", "is", "programming", "language"],
]

# Create BM25 object
bm25 = BM25Okapi(corpus)

# Score a query
query = ["python", "programming"]
scores = bm25.get_scores(query)
print(scores)

# Get top N documents
top_docs = bm25.get_top_n(query, corpus, n=2)
print(top_docs)
```

**Available BM25 Variants:**
- `BM25Okapi` - Standard BM25 (most common)
- `BM25L` - BM25L variant with different normalization
- `BM25Plus` - BM25+ with improved lower bound
- `BM25Adpt` - Adaptive BM25

([rank-bm25 PyPI][2])

### BM25S - High Performance

For production applications requiring high performance:

```python
import bm25s
import numpy as np

# Create corpus (can use raw strings)
corpus = [
    "Python is a programming language",
    "Python is used for data science",
    "Java is a programming language",
]

# Tokenize (BM25S has built-in tokenizer)
corpus_tokens = bm25s.tokenize(corpus, stopwords="english")

# Create BM25 index
retriever = bm25s.BM25()

# Index the corpus
retriever.index(corpus_tokens)

# Query
query = "Python programming"
query_tokens = bm25s.tokenize(query, stopwords="english")

# Get top-k results
results, scores = retriever.retrieve(query_tokens, k=3)

for i, (doc_idx, score) in enumerate(zip(results[0], scores[0])):
    print(f"{i+1}. {corpus[doc_idx]} (score: {score:.3f})")
```

**BM25S Advantages:**
- Orders of magnitude faster than rank-bm25
- Uses scipy sparse matrices for efficiency
- Minimal dependencies (numpy, scipy)
- Comparable to Elasticsearch on single node

([BM25S Docs][3])

## BM25 Variants

### BM25+ (BM25 Plus)

Addresses lower-bound issues in standard BM25:

```
score = Σ IDF(qi) × [δ + (tf × (k₁ + 1)) / (tf + k₁ × (1 - b + b × |D| / avgdl))]
```

Adds parameter `δ` (typically 0.5-1.0) to prevent zero scores. ([Wikipedia BM25][1])

```python
class BM25Plus(BM25):
    """BM25+ with improved lower bound."""

    def __init__(self, corpus, k1=1.5, b=0.75, delta=0.5):
        super().__init__(corpus, k1, b)
        self.delta = delta

    def score(self, query, doc_idx):
        score = 0.0
        doc = self.corpus[doc_idx]
        doc_len = self.doc_len[doc_idx]
        term_freqs = Counter(doc)

        for term in query:
            tf = term_freqs.get(term, 0)
            idf = self.idf.get(term, 0)

            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)

            # BM25+ adds delta
            score += idf * (self.delta + numerator / denominator)

        return score
```

### BM25F (BM25 for Fields)

Handles multi-field documents with different weights:

```python
class BM25F:
    """BM25F for multi-field documents."""

    def __init__(self, corpus, field_weights=None, k1=1.5, b=0.75):
        """
        Args:
            corpus: List of dicts with field names as keys
                    e.g., [{"title": [...], "body": [...]}]
            field_weights: Dict of field weights (e.g., {"title": 3.0, "body": 1.0})
        """
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.field_weights = field_weights or {"title": 1.0, "body": 1.0}

        # Calculate average lengths per field
        self.avg_field_lens = {}
        for field in self.field_weights:
            lengths = [len(doc.get(field, [])) for doc in corpus]
            self.avg_field_lens[field] = sum(lengths) / len(corpus)

        # Build IDF (across all fields)
        self._calc_idf()

    def score(self, query, doc_idx):
        """Score document considering all fields."""
        score = 0.0
        doc = self.corpus[doc_idx]

        for term in query:
            idf = self.idf.get(term, 0)
            weighted_tf = 0.0

            # Aggregate TF across fields with weights
            for field, weight in self.field_weights.items():
                field_terms = doc.get(field, [])
                tf = field_terms.count(term)
                doc_len = len(field_terms)
                avg_len = self.avg_field_lens[field]

                if tf > 0:
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (
                        1 - self.b + self.b * doc_len / avg_len
                    )
                    weighted_tf += weight * (numerator / denominator)

            score += idf * weighted_tf

        return score


# Usage
corpus = [
    {
        "title": ["python", "tutorial"],
        "body": ["python", "is", "a", "programming", "language"]
    },
    {
        "title": ["java", "basics"],
        "body": ["java", "is", "object", "oriented"]
    }
]

bm25f = BM25F(
    corpus,
    field_weights={"title": 3.0, "body": 1.0}  # Title 3x more important
)
```

## Parameter Tuning

### Finding Optimal k₁ and b

Use grid search with validation set:

```python
def tune_bm25_parameters(train_corpus, queries, relevance_labels):
    """Find optimal k1 and b parameters."""
    best_score = 0
    best_params = (1.5, 0.75)

    # Grid search
    for k1 in [1.0, 1.2, 1.5, 2.0]:
        for b in [0.0, 0.25, 0.5, 0.75, 1.0]:
            bm25 = BM25(train_corpus, k1=k1, b=b)

            # Evaluate on validation queries
            total_score = 0
            for query, labels in zip(queries, relevance_labels):
                results = bm25.get_top_n(query, n=10)
                score = evaluate_ranking(results, labels)
                total_score += score

            avg_score = total_score / len(queries)

            if avg_score > best_score:
                best_score = avg_score
                best_params = (k1, b)

    return best_params

# Example: evaluate with NDCG
def evaluate_ranking(results, relevance_labels):
    """Calculate NDCG@10 for ranking."""
    dcg = sum(
        (2 ** relevance_labels.get(doc_idx, 0) - 1) / math.log2(i + 2)
        for i, (doc_idx, _) in enumerate(results)
    )
    return dcg
```

### Domain-Specific Guidelines

**Short documents (tweets, titles):**
- Lower b (0.3-0.5) - Less length normalization
- Lower k₁ (1.0-1.2) - Faster saturation

**Long documents (articles, books):**
- Higher b (0.75-0.9) - More length normalization
- Higher k₁ (1.5-2.0) - Slower saturation

**Mixed-length collections:**
- Standard values (k₁=1.5, b=0.75)
- Consider BM25+ for better handling

## BM25 vs. TF-IDF Comparison

| Aspect | BM25 | TF-IDF |
|--------|------|--------|
| **Term Frequency** | Saturating (diminishing returns) | Linear or log |
| **Length Normalization** | Tunable via parameter b | Often absent or crude |
| **IDF Formula** | Probabilistic | Logarithmic |
| **Parameters** | Tunable (k₁, b) | Fixed |
| **Performance** | Better for most IR tasks | Simpler, faster |
| **Use Case** | Search engines, document ranking | Document classification, clustering |

**When to use BM25:**
- Document retrieval and ranking
- Varying document lengths
- Need for tuning
- Modern search applications

**When to use TF-IDF:**
- Document similarity
- Text classification
- Simpler implementations
- Well-understood corpus

## Integration with Search Systems

### Combining with Inverted Index

```python
from collections import defaultdict

class BM25Search:
    """BM25 search with inverted index for efficiency."""

    def __init__(self, documents, k1=1.5, b=0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b

        # Build inverted index
        self.inverted_index = defaultdict(set)
        self.corpus = []

        for doc_id, text in enumerate(documents):
            tokens = self.tokenize(text)
            self.corpus.append(tokens)

            # Update inverted index
            for token in set(tokens):
                self.inverted_index[token].add(doc_id)

        # Initialize BM25
        self.bm25 = BM25(self.corpus, k1, b)

    def search(self, query_text, n=10):
        """Search using inverted index for candidate selection."""
        query_tokens = self.tokenize(query_text)

        # Get candidate documents (contain at least one query term)
        candidates = set()
        for token in query_tokens:
            candidates.update(self.inverted_index.get(token, set()))

        if not candidates:
            return []

        # Score only candidates
        scored_docs = [
            (doc_id, self.bm25.score(query_tokens, doc_id))
            for doc_id in candidates
        ]

        # Sort and return top N
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:n]
```

## Best Practices

1. **Use standard parameters initially** - Start with k₁=1.5, b=0.75
2. **Tune on validation data** - Adjust parameters based on actual queries
3. **Preprocess consistently** - Same tokenization for indexing and querying
4. **Filter stopwords** - Remove common words for better relevance
5. **Consider BM25+** - For collections with very short documents
6. **Use BM25F for structured docs** - When fields have different importance
7. **Combine with inverted index** - For efficient candidate selection
8. **Cache IDF values** - Recalculate only when corpus changes
9. **Monitor query performance** - Profile and optimize slow queries
10. **Compare with TF-IDF** - Validate that BM25 actually improves results

## Common Issues

### Issue: All Scores Too Similar

**Cause**: Parameters not tuned for corpus characteristics.

**Solution**: Adjust k₁ and b:
```python
# Increase differentiation
bm25 = BM25(corpus, k1=2.0, b=0.9)
```

### Issue: Short Documents Rank Too Low

**Cause**: Excessive length normalization.

**Solution**: Decrease b parameter:
```python
# Less length penalty
bm25 = BM25(corpus, k1=1.5, b=0.3)
```

### Issue: Long Documents Dominate

**Cause**: Insufficient length normalization.

**Solution**: Increase b parameter:
```python
# More length penalty
bm25 = BM25(corpus, k1=1.5, b=0.9)
```

### Issue: Poor Performance on Multi-Field Documents

**Cause**: Using standard BM25 on structured documents.

**Solution**: Use BM25F with field weights.

## References

[1]: https://en.wikipedia.org/wiki/Okapi_BM25 "Wikipedia - Okapi BM25"
[2]: https://pypi.org/project/rank-bm25/ "rank-bm25 on PyPI"
[3]: https://bm25s.github.io/ "BM25S Documentation"

# H2LooP KG 2.0

### 1 Overview
The system was evaluated on a curated set of high-quality technical documents including datasheets, specifications, and technical manuals.

### 2 Baseline Systems

| System | Description |
|--------|-------------|
| **RLM (DSPy)** | Full document context stuffed into prompt. Uses DSPy framework with structured signatures (DirectAnswer/RefineAnswer). Powered by minimax-m2. Configured with depth=1, iterations=1 |
| **Naive RAG** | Fixed 512-token chunking with 50-token overlap. Embeddings via all-MiniLM-L6-v2 (384-dim, local). Cosine similarity top-5 retrieval, in-memory. Generation via minimax-m2 |
| **Standalone Model** | Full document context stuffed into prompt. Single-shot completion via minimax-m2. No retrieval, no refinement |

### 3 Performance Results

#### Overall Performance

![H2LooP KG 2.0 Overall Performance](plots/kg_overall_performance.png)

| System | Final Score | Avg Response Time |
|--------|-------------|-------------------|
| **H2LooP KG 2.0** | **81.5%** | 55.1s |
| RLM | 65.4% | 47.0s |
| Naive RAG | 61.5% | 7.4s |
| Standalone Model | 59.1% | 36.7s |

H2LooP KG 2.0 outperforms baseline approaches by significant margins:
- **24.7% better** than Standalone Model
- **20.0% better** than Naive RAG
- **16.1% better** than RLM

#### Performance by Metric

![H2LooP KG 2.0 Performance by Metric](plots/kg_performance_by_metric.png)

| Metric | H2LooP KG 2.0 | RLM | Naive RAG | Standalone Model |
|--------|---------------|-----------|-----------|------------------------|
| Numerical Precision | **91.7%** | 66.7% | 60.4% | 60.4% |
| Completeness | **95.8%** | 81.2% | 70.8% | 77.1% |
| Citation Quality | **35.4%** | 10.4% | 27.1% | 20.8% |
| No Hallucination | **83.3%** | 70.8% | 60.4% | 60.4% |
| Relevance | 66.7% | 87.5% | **91.7%** | 95.8% |
| Faithfulness | 93.8% | 79.2% | 70.8% | 66.7% |

#### Performance by Question Complexity

![H2LooP KG 2.0 Performance by Question Complexity](plots/kg_performance_by_complexity.png)

| Category | H2LooP KG 2.0 | RLM | Naive RAG | Standalone Model |
|----------|---------------|-----------|-----------|------------------------|
| Fact-based | **85.6%** | 81.2% | 67.5% | 65.0% |
| Single-hop reasoning | **81.2%** | 58.1% | 53.4% | 66.9% |
| Multi-hop reasoning | **77.5%** | 53.7% | 59.4% | 50.3% |

### 4 Key Strengths

- **Exceptional Numerical Precision**: 91.7% accuracy in extracting exact technical specifications
- **Superior Completeness**: 95.8% coverage of all required information
- **Reduced Hallucinations**: 83.3% hallucination-free responses with better grounding in actual content
- **Enhanced Citation Quality**: Explicitly references tables, sections, and page numbers for verification
- **Strong Multi-hop Reasoning**: 77.5% accuracy on complex questions requiring cross-document reasoning
- **No Context Length Limitation**: Handles arbitrarily large document collections

---

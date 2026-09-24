"""
Curriculum Transformer for RAG & Vector Databases Track.
Transforms raw topic headings into high-caliber interview questions, structured answers,
and production-ready Python vector search / indexing / RAG code.
"""

def transform_rag_topic(topic_title: str, level: str, sec_slug: str, sec_name: str) -> dict:
    t = topic_title.strip()
    question_title = format_rag_question(t, level)
    short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes = generate_rag_dna(t, level, sec_slug, sec_name, question_title)
    
    return {
        "title": question_title,
        "short_answer": short_ans,
        "interview_ready_answer": ready_ans,
        "deep_explanation": deep_exp,
        "code_example": code_ex,
        "architecture_notes": arch_flow,
        "why_interviewer_asks": why_ask,
        "interviewer_intent": f"Tests deep architectural comprehension of high-throughput vector indexing, chunking strategies, hybrid reranking, and hallucination guardrails at {level} depth.",
        "production_considerations": f"In production RAG systems, ensure {t} has P99 latency monitoring, index quantization to manage RAM costs, and automated context precision evaluations.",
        "failure_modes": fail_modes,
        "tradeoffs": tradeoffs,
        "common_mistakes": mistakes
    }

def format_rag_question(topic: str, level: str) -> str:
    mappings = {
        "Recursive Character Text Splitting": "How does Recursive Character Text Splitting work in RAG pipelines, and why is it preferred over naive fixed-character splitting?",
        "Chunk Size and Chunk Overlap": "How do you determine optimal chunk size and chunk overlap for embedding generation, and what are the trade-offs on retrieval recall vs LLM context limits?",
        "Fixed-Size vs Semantic Chunking": "What are the structural trade-offs between fixed-size chunking and semantic boundary chunking in dense vector retrieval?",
        "Markdown and Header Aware Chunking": "How do you preserve hierarchical document context using markdown and header-aware chunking in technical documentation RAG?",
        "Token Counting vs Character Length": "Why is token-aware chunking essential compared to character-based length when preparing text for embedding models?",
        "Document Metadata Enrichment": "How does metadata enrichment (e.g., author, timestamp, doc type) enhance filtered vector search and prevent cross-tenant data leaks?",
        "PDF Parsing Strategies": "What are the most robust PDF parsing strategies for extracting clean structured text and tables without OCR noise in enterprise RAG?",
        "Table Extraction Challenges": "How do you handle complex multi-row and multi-column tables during chunking to maintain semantic context for embeddings?",
        "Sentence Window Chunking": "How does the Sentence Window retrieval technique decouple embedding search granularity from LLM generation context?",
        "Parent Document Retriever": "What is the Parent Document Retriever pattern, and how does it balance small vector search chunks with comprehensive context windows?",
        
        "HNSW Graph Construction Basics": "How does the Hierarchical Navigable Small World (HNSW) graph algorithm achieve logarithmic-time approximate nearest neighbor search?",
        "Cosine Similarity vs Euclidean Distance": "What is the mathematical and operational difference between Cosine Similarity, Dot Product, and Euclidean (L2) distance in normalized vector spaces?",
        "Dot Product vs Normalized Vectors": "Why is Dot Product equivalent to Cosine Similarity when vector embeddings are unit-normalized, and what are the performance advantages?",
        "Flat Index vs Approximate Search (ANN)": "What are the trade-offs between brute-force flat index search (exact k-NN) and approximate nearest neighbor (ANN) indexing in production?",
        "IVF Inverted File Indexing": "How does Inverted File (IVF) vector indexing partition high-dimensional space into Voronoi cells to accelerate search?",
        "HNSW efSearch and M Parameter Tuning": "How do the M and efSearch parameters in HNSW indexes govern the trade-off between search recall, query latency, and build time?",
        "Product Quantization (PQ) Compression": "How does Product Quantization (PQ) compress high-dimensional vector embeddings, and what is its impact on RAM consumption and retrieval accuracy?",
        "Scalar Quantization (SQ8) Memory Optimization": "How does Scalar Quantization (SQ8) reduce vector index memory footprint from 32-bit floats to 8-bit integers while preserving recall?",
        "Filtered Vector Search: Pre-Filter vs Post-Filter": "What are the performance and recall trade-offs between pre-filtering (single-stage) and post-filtering in vector databases?",
        "Matryoshka Representation Learning (MRL)": "How does Matryoshka Representation Learning (MRL) allow dynamic vector dimension truncation without re-embedding documents?",
        
        "BM25 Keyword Search Principles": "How does the BM25 probabilistic relevance algorithm calculate term frequency saturation and document length normalization?",
        "Reciprocal Rank Fusion (RRF) Formula": "How does Reciprocal Rank Fusion (RRF) combine disparate rank lists from BM25 and dense vector retrievers without score calibration?",
        "Cross-Encoder vs Bi-Encoder": "What are the architectural and computational differences between Bi-Encoder embeddings and Cross-Encoder neural rerankers?",
        "Top-N Retrieval before Top-K Rerank": "How does a two-stage retrieval pipeline (top-N candidate retrieval followed by top-K cross-encoder reranking) optimize the latency-accuracy frontier?",
        "Sparse Embeddings (SPLADE) Intro": "How do learned sparse representations like SPLADE expand document terms while maintaining inverted index efficiency?",
        
        "What is Hallucination in RAG": "What causes hallucinations in Retrieval-Augmented Generation, and how do you differentiate faithfulness failures from retrieval misses?",
        "Context Precision Metric": "How is Context Precision calculated in RAG evaluation frameworks, and why does ranking relevant chunks higher reduce generation errors?",
        "Context Recall Metric": "How do you evaluate Context Recall in RAG pipelines to verify that all necessary ground-truth facts are present in retrieved chunks?",
        "Faithfulness (Groundedness) Metric": "How does the Faithfulness metric measure whether every claim in an LLM generated answer is directly attributable to the retrieved context?",
        "Answer Relevance Definition": "What does Answer Relevance measure in the RAG Triad, and how is it evaluated independently of retrieved context accuracy?",
        "Evaluating RAG with LLM-as-a-Judge": "How do you configure and calibrate an LLM-as-a-Judge evaluation harness to prevent position bias, verbosity bias, and self-enhancement bias?"
    }
    
    if topic in mappings:
        return mappings[topic]
        
    clean = topic.replace(":", "").replace("?", "").strip()
    if clean.lower().startswith("what") or clean.lower().startswith("how") or clean.lower().startswith("why"):
        return clean + ("?" if not clean.endswith("?") else "")
        
    if level == "L1":
        return f"What is the principle of {clean} in RAG and vector retrieval, and how is it implemented?"
    else:
        return f"How do you design, optimize, and benchmark {clean} in high-throughput enterprise RAG architectures?"

from .text_utils import clean_concept_name

def generate_rag_dna(topic: str, level: str, sec_slug: str, sec_name: str, question: str):
    t_clean = clean_concept_name(topic)
    
    short_ans = (
        f"In RAG and vector database architectures ({sec_name}), {t_clean} is critical for maximizing retrieval precision and minimizing latency. "
        f"It establishes mathematical and algorithmic boundaries for document chunking, high-dimensional similarity search, "
        f"and context grounding, directly preventing information loss and hallucinations."
    )
    
    ready_ans = (
        f"When explaining **{t_clean}** in a senior AI systems interview, structure your response around three core pillars:\n\n"
        f"1. **Mathematical & Algorithmic Foundations**: {t_clean} directly addresses the fundamental trade-off between semantic search recall "
        f"and query latency. Whether partitioning vector spaces, normalizing embeddings, or fusing hybrid search scores, the objective is "
        f"to maximize the signal-to-noise ratio in retrieved context chunks.\n\n"
        f"2. **Pipeline Architecture & Performance**: In production retrieval pipelines, {t_clean} acts as a key operational stage. "
        f"Unoptimized implementations cause P99 latency spikes or exhaust memory budgets. Applying quantization, indexing heuristics, "
        f"and cache-aside patterns ensures sub-50ms query turnaround even under high concurrent QPS.\n\n"
        f"3. **Production Governance & Guardrails**: Candidates must articulate how to measure quality degradation. "
        f"Using metrics like Context Precision, Recall, and NDCG@10 allows engineering teams to continuously monitor semantic drift "
        f"and detect regressions in automated CI/CD evaluation suites."
    )
    
    deep_exp = (
        f"### Deep System Mechanics: {t_clean}\n\n"
        f"In dense vector retrieval, high-dimensional representations (typically 768 to 3072 dimensions) are queried across millions of points. "
        f"Brute-force exact k-NN computation scales at `O(N * D)` where N is corpus size and D is vector dimensionality—untenable for real-time applications.\n\n"
        f"To achieve sub-linear `O(log N)` search, approximate nearest neighbor (ANN) algorithms structure vectors into hierarchical proximity graphs "
        f"or clustered partitions. In HNSW, layered graphs allow greedy routing at top sparse layers and fine-grained exploration at dense lower layers. "
        f"Distance calculations (Cosine, Dot Product, L2) leverage SIMD instructions (AVX-512) for hardware acceleration.\n\n"
        f"When combined with lexical inverted indexes (BM25) via Reciprocal Rank Fusion, the pipeline overcomes dense vector vocabulary mismatches "
        f"(such as product SKUs, exact error codes, or acronyms), producing a resilient, high-recall candidate pool for downstream generation."
    )
    
    # Real Python RAG / Vector search code
    code_ex = (
        f"import numpy as np\n"
        f"from typing import List, Dict, Any\n\n"
        f"class ResilientVectorSearchEngine:\n"
        f"    def __init__(self, dimension: int = 1536):\n"
        f"        self.dimension = dimension\n"
        f"        self.embeddings: np.ndarray = np.empty((0, dimension), dtype=np.float32)\n"
        f"        self.metadata_store: List[Dict[str, Any]] = []\n\n"
        f"    def insert(self, vector: List[float], metadata: Dict[str, Any]):\n"
        f"        norm_vec = np.array(vector, dtype=np.float32)\n"
        f"        norm_vec = norm_vec / (np.linalg.norm(norm_vec) + 1e-9)  # Unit normalization for Cosine\n"
        f"        self.embeddings = np.vstack([self.embeddings, norm_vec])\n"
        f"        self.metadata_store.append(metadata)\n\n"
        f"    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:\n"
        f"        if len(self.metadata_store) == 0:\n"
        f"            return []\n"
        f"        q = np.array(query_vector, dtype=np.float32)\n"
        f"        q = q / (np.linalg.norm(q) + 1e-9)\n"
        f"        # Fast matrix-vector dot product across normalized vectors\n"
        f"        scores = np.dot(self.embeddings, q)\n"
        f"        top_indices = np.argsort(scores)[::-1][:top_k]\n"
        f"        return [\n"
        f"            {{\n"
        f"                'score': float(scores[idx]),\n"
        f"                'metadata': self.metadata_store[idx],\n"
        f"                'strategy': '{t_clean}'\n"
        f"            }}\n"
        f"            for idx in top_indices\n"
        f"        ]\n\n"
        f"# Demonstration execution\n"
        f"engine = ResilientVectorSearchEngine(dimension=4)\n"
        f"engine.insert([0.1, 0.8, 0.3, 0.4], {{'chunk_id': 'c1', 'text': 'Core architecture of {t_clean}'}})\n"
        f"engine.insert([0.9, 0.2, 0.1, 0.0], {{'chunk_id': 'c2', 'text': 'Unrelated context'}})\n"
        f"results = engine.search([0.1, 0.8, 0.25, 0.4], top_k=1)\n"
        f"print('Top retrieved chunk:', results[0])"
    )
    
    arch_flow = (
        f"User Query Ingress\n"
        f"  │\n"
        f"  ├───────────────┬────────────────┐\n"
        f"  ▼               ▼                ▼\n"
        f"[Dense Embedder] [BM25 Lexical]   [Metadata Filter]\n"
        f"  │ (Vector)      │ (Tokens)       │ (Tenant / ACL)\n"
        f"  ▼               ▼                ▼\n"
        f"[{t_clean} ANN Vector Search] ──► [Reciprocal Rank Fusion (RRF)]\n"
        f"                                        │\n"
        f"                                        ▼\n"
        f"                               [Cross-Encoder Reranker]\n"
        f"                                        │\n"
        f"                                        ▼\n"
        f"                               [LLM Context Window & Hallucination Guardrails]"
    )
    
    why_ask = f"Interviewers assess whether the candidate understands vector space geometry, approximate nearest neighbor trade-offs, and how to scale enterprise RAG without memory blowups."
    fail_modes = f"Quantization accuracy loss degrading recall, memory exhaustion from uncompressed high-dimensional vectors, and semantic drift between ingestion and inference embedding models."
    tradeoffs = f"Balancing embedding dimensionality and precision against RAM memory footprint, indexing throughput, and P99 query latency."
    mistakes = [
        f"Using Euclidean distance on unnormalized embeddings when the model expects cosine similarity",
        f"Neglecting metadata pre-filtering, leading to cross-tenant data leakage in multi-tenant RAG",
        f"Using monolithic chunk sizes that dilute key semantic facts with irrelevant filler text"
    ]
    
    return short_ans, ready_ans, deep_exp, code_ex, arch_flow, why_ask, fail_modes, tradeoffs, mistakes

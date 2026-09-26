"""
DSA & Algorithms Batch Expansion
Focuses on under-represented topics:
- dynamic-programming (Dynamic Programming & Memoization Patterns)
- heaps-hash-structures (Heaps, Hash Maps & Priority Queues)
- trees-graphs-traversal (Trees, Binary Search Trees & Graph Traversal)
Tiers: HARD, TOUGH, PRODUCTION_SCENARIO
All compliant with the strict 10-point Content Quality Gatekeeper.
"""

def get_dsa_expansion_batch():
    return [
        {
            "title": "How do you solve the Word Break II problem using Dynamic Programming with Memoized Depth-First Search and Trie optimization?",
            "difficulty": "HARD",
            "technology_slug": "dsa",
            "topic_slug": "dynamic-programming",
            "question_type": "ALGORITHMIC",
            "scenario_type": "ALGORITHM_DESIGN",
            "short_answer": "Solve Word Break II by combining a Trie for prefix matching with memoized DFS (top-down DP), storing the list of all valid sentence suffixes for each index to avoid redundant recomputations of overlapping subproblems.",
            "interview_ready_answer": "Word Break II requires returning all possible sentence segmentations of a string `s` where each word exists in a dictionary. A naive backtracking approach takes O(2^N) exponential time and TLEs on repeated patterns like 'aaaaaaa'. The optimal solution uses Depth-First Search with Memoization (Top-Down DP): a memoization map `memo[index]` stores all valid sentence suffixes starting at that index. At each position `i`, we test prefixes `s[i:j]`. If the prefix exists in the dictionary (or a Trie for fast prefix checks), we recursively solve for suffix starting at `j` and prepend the prefix to all returned suffix sentences. Storing intermediate lists in the memo prevents redundant exploration.",
            "deep_explanation": "The recurrence relation is: `sentences(i) = [word + (' ' + rest if rest else '') for word in dict if s[i:].startswith(word) for rest in sentences(i + len(word))]`. Base case: `sentences(len(s)) = ['']`. Using a Trie instead of a hash set reduces prefix validation from O(N) string slicing to O(1) per character transition. The worst-case time complexity is bounded by the number of valid sentences in the output, which can be exponential in pathological cases (e.g. 'aaa' with dict ['a', 'aa', 'aaa']), but memoization guarantees that every non-productive dead-end branch is visited exactly once.",
            "architecture_notes": "Classic LeetCode Hard problem (LC 140) testing state memoization, Trie integration, and combinatorial recursion.",
            "code_example": """from typing import List, Dict

def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    word_set = set(wordDict)
    memo: Dict[int, List[str]] = {}

    def dfs(index: int) -> List[str]:
        if index in memo:
            return memo[index]
        if index == len(s):
            return [""]
        
        sentences = []
        for end in range(index + 1, len(s) + 1):
            word = s[index:end]
            if word in word_set:
                for suffix in dfs(end):
                    sentences.append(word + (" " + suffix if suffix else ""))
        
        memo[index] = sentences
        return sentences

    return dfs(0)""",
            "why_interviewer_asks": "Evaluates candidate's mastery of dynamic programming on strings, memoization data structures, and handling combinatorial output spaces.",
            "production_considerations": "In production search tokenizers (e.g. Japanese/Chinese morphological analyzers), use a Trie or Aho-Corasick automaton with Viterbi DP to find the most probable segmentation rather than generating all combinations.",
            "failure_modes": "Omitting the memoization table causes exponential call stack explosion (O(2^N)) and Time Limit Exceeded (TLE) on strings with dense repetitive prefixes.",
            "tradeoffs": "Memoization caches intermediate sentence lists, trading O(N * 2^N) auxiliary heap memory for massive pruning of non-viable branches.",
            "common_mistakes": [
                "Using pure backtracking without memoization, leading to exponential time complexity.",
                "Slicing strings repeatedly inside loops without checking maximum dictionary word length.",
                "Forgetting to handle the base case where index reaches the end of the string."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "Why does standard backtracking repeat work when multiple prefixes lead to the same remaining suffix?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "What should the memoization map store as its key and value?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "How does storing intermediate sentence lists at `memo[i]` prune redundant DFS branches?"}
            ],
            "sources": [
                {
                    "source_name": "Introduction to Algorithms (CLRS): Dynamic Programming",
                    "source_url": "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
                    "publisher": "MIT Press"
                }
            ],
            "followups": [
                {
                    "followup_question": "How does Word Break I (boolean reachability) differ algorithmically from Word Break II (sentence generation)?",
                    "answer_guidance": "Word Break I can be solved in O(N^2) time and O(N) space using a 1D boolean array (`dp[i] = any(dp[j] and s[j:i] in dict)`), whereas Word Break II must collect combinations, which has an exponential output space."
                }
            ],
            "tags": ["DSA", "Dynamic Programming", "Recursion", "Trie", "Memoization", "Google", "Amazon"]
        },
        {
            "title": "How do you design a MedianFinder data structure supporting addNum in O(log N) and findMedian in O(1) time using Two Heaps?",
            "difficulty": "HARD",
            "technology_slug": "dsa",
            "topic_slug": "heaps-hash-structures",
            "question_type": "ALGORITHMIC",
            "scenario_type": "DATA_STRUCTURE_DESIGN",
            "short_answer": "Maintain a max-heap for the smaller half of numbers and a min-heap for the larger half, balancing them so their sizes differ by at most 1; the median is either the top of the larger heap or the average of both tops in O(1) time.",
            "interview_ready_answer": "Finding the median of a dynamically growing stream of numbers naively requires re-sorting the array on each insert (O(N log N) per query). The two-heap approach splits numbers into two halves: a max-heap (`small`) stores the lower half, and a min-heap (`large`) stores the upper half. Invariant 1: Every element in `small` is <= every element in `large`. Invariant 2: The size of `small` is either equal to `large` or contains exactly 1 more element. Inserting a number takes O(log N) heap push/pop. To query the median in O(1): if total count is odd, return `small[0]`; if even, return `(small[0] + large[0]) / 2.0`.",
            "deep_explanation": "Under the hood, in Python (which only has `heapq` min-heaps), we negate numbers to simulate a max-heap. During `addNum(num)`: 1. Push to `small` (negated). 2. Pop the largest of `small` and push to `large` to enforce ordering. 3. If `len(large) > len(small)`, pop the smallest of `large` back to `small` to enforce size balance. This guarantees that `small` always has size equal to or one greater than `large`. Time complexity: O(log N) for `addNum`, O(1) for `findMedian`. Space complexity: O(N) to store stream elements.",
            "architecture_notes": "Foundational pattern used in streaming metric aggregators, financial percentile monitors, and LeetCode Hard (LC 295).",
            "code_example": """import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (stores negated values)
        self.large = []  # Min-heap

    def addNum(self, num: int) -> None:
        # Step 1: Push to max-heap
        heapq.heappush(self.small, -num)
        # Step 2: Ensure small's max <= large's min
        heapq.heappush(self.large, -heapq.heappop(self.small))
        # Step 3: Maintain size balance (small can have at most 1 more than large)
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0""",
            "why_interviewer_asks": "Tests deep proficiency with heap properties, streaming data algorithms, balance invariants, and optimal space-time trade-offs.",
            "production_considerations": "For multi-terabyte streaming data where storing all elements in memory is impossible, use streaming quantile approximations like t-digest or Count-Min Sketch instead of exact two-heaps.",
            "failure_modes": "In integer division environments (like Java or C++), computing `(small.peek() + large.peek()) / 2` without casting to float causes integer truncation and incorrect medians.",
            "tradeoffs": "Provides exact median in O(1) time and O(log N) insert, but requires O(N) heap memory, which is unsuitable for infinite streaming telemetry without a sliding window.",
            "common_mistakes": [
                "Attempting to maintain a single sorted array with insertion sort (O(N) insert time).",
                "Failing to rebalance the heaps when numbers are inserted in strictly ascending or descending order.",
                "Forgetting that Python's heapq is strictly a min-heap, failing to negate values for max-heap behavior."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How can dividing numbers into 'lower half' and 'upper half' give you instant access to the middle elements?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "What heap types should represent the lower and upper halves respectively?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "What balancing rule ensures that the median is always at the root of one or both heaps?"}
            ],
            "sources": [
                {
                    "source_name": "Algorithms, 4th Edition (Sedgewick & Wayne): Priority Queues",
                    "source_url": "https://algs4.cs.princeton.edu/24pq/",
                    "publisher": "Addison-Wesley / Princeton University"
                }
            ],
            "followups": [
                {
                    "followup_question": "How would you modify this design to support a sliding window median of fixed size K?",
                    "answer_guidance": "Use two balanced BSTs (like red-black trees in C++ `std::multiset`) or two heaps with lazy removal of out-of-window elements using a hash map counter."
                }
            ],
            "tags": ["DSA", "Heaps", "Priority Queue", "Streaming Algorithms", "Meta", "Google"]
        },
        {
            "title": "Production Incident: A critical order-routing service experiences high-CPU thread spikes and OutOfMemoryError due to cycle-induced recursion and thread pool exhaustion in a DAG scheduler. How do you detect cycles and enforce topological execution?",
            "difficulty": "PRODUCTION_SCENARIO",
            "technology_slug": "dsa",
            "topic_slug": "trees-graphs-traversal",
            "question_type": "SCENARIO_BASED",
            "scenario_type": "PRODUCTION_INCIDENT",
            "short_answer": "Detect cycles upfront using Kahn's Algorithm (in-degree BFS) or 3-color DFS (WHITE, GRAY, BLACK) during workflow registration, rejecting circular dependencies before runtime and executing valid tasks in strict topological order.",
            "interview_ready_answer": "In DAG-based task execution engines (like Airflow or microservice order orchestration pipelines), tasks have dependency prerequisites. If a user or automated rule introduces a circular dependency (A -> B -> C -> A), recursive task runners enter infinite stack recursion or block worker threads waiting on sibling futures, causing thread starvation and OOM crashes. Immediate mitigation: 1. Kill the hung execution worker pods. 2. Implement mandatory DAG validation at configuration ingestion time: run Kahn's Algorithm (in-degree topological sort). If the number of processed nodes is less than total nodes, a cycle exists; reject the workflow immediately. 3. Return the exact cycle path using 3-color DFS so engineers can identify the offending task loop.",
            "deep_explanation": "Kahn's Algorithm operates in O(V + E) time: 1. Calculate the in-degree (number of incoming dependency edges) for every vertex. 2. Enqueue all vertices with in-degree == 0. 3. While queue is non-empty, dequeue vertex `u`, append `u` to topological order, and decrement in-degrees of all neighbors `v`. If `v` reaches in-degree == 0, enqueue `v`. 4. If `len(topological_order) != V`, the graph contains at least one directed cycle. To extract the exact cycle for incident reporting, 3-color DFS traverses nodes: WHITE (unvisited), GRAY (currently in recursion stack), BLACK (fully explored). If an edge points to a GRAY node, a back-edge (cycle) is detected.",
            "architecture_notes": "Implemented in Apache Airflow DAG parser, Bazel build graph validator, and Kubernetes controller dependency reconcilers.",
            "code_example": """from collections import deque, defaultdict
from typing import Dict, List, Tuple

def validate_and_sort_dag(num_nodes: int, dependencies: List[Tuple[int, int]]) -> Tuple[bool, List[int]]:
    \"\"\"Returns (is_valid_dag, topological_order)\"\"\"
    in_degree = [0] * num_nodes
    adj = defaultdict(list)
    for u, v in dependencies:  # u -> v (u must execute before v)
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If order does not contain all nodes, a cycle exists!
    is_valid = len(order) == num_nodes
    return is_valid, order if is_valid else []""",
            "why_interviewer_asks": "Evaluates candidate's ability to apply fundamental graph theory (topological sorting, cycle detection) to solve real-world infrastructure and orchestrator outages.",
            "production_considerations": "Always execute DAG cycle validation during workflow authoring/deployment time, preventing malformed dependency graphs from ever reaching production task workers.",
            "failure_modes": "Missing cycle validation in async workflow orchestrators leads to deadlock where worker threads indefinitely await completion of mutual dependencies.",
            "tradeoffs": "O(V + E) graph validation adds sub-millisecond validation overhead at deployment time, completely eliminating catastrophic circular runtime deadlocks.",
            "common_mistakes": [
                "Executing workflow tasks dynamically without validating the entire graph topology beforehand.",
                "Using simple 2-state visited sets (visited/unvisited) for cycle detection, which fails on directed graphs (must use 3-color state).",
                "Allowing recursive task dispatch without max recursion depth safety guards."
            ],
            "hints": [
                {"hint_level": 1, "hint_type": "CONCEPTUAL", "content": "How does Kahn's in-degree algorithm detect whether a graph has cycles?"},
                {"hint_level": 2, "hint_type": "IMPLEMENTATION", "content": "What does it mean if the queue becomes empty before all nodes are processed in Kahn's algorithm?"},
                {"hint_level": 3, "hint_type": "ARCHITECTURE", "content": "How do you extract the exact cycle path using 3-color DFS (WHITE, GRAY, BLACK)?"}
            ],
            "sources": [
                {
                    "source_name": "Kahn's Algorithm for Topological Sorting (Communications of the ACM)",
                    "source_url": "https://dl.acm.org/doi/10.1145/368996.369025",
                    "publisher": "ACM"
                }
            ],
            "followups": [
                {
                    "followup_question": "How do you execute independent topological nodes in parallel across multiple worker threads?",
                    "answer_guidance": "Whenever multiple nodes reach in-degree == 0 simultaneously, submit them concurrently to an ExecutorService or asyncio task group."
                }
            ],
            "tags": ["DSA", "Graphs", "Topological Sort", "Cycle Detection", "Production Incident", "Kahn's Algorithm"]
        }
    ]

# Pymetheus
Synthetic Dataset of Python Code for Reinforcement Learning

This repository has more than 10K coding examples. All of these are stored in four subfolders in the `data` folder. 
* `good_quality` has good quality data, the Python code and unit tests all compile and the json file adheres to the `schema` highlighted below. 
* `invalid_python_code` contains jsons that are well formatted but their python code has errors 
* `invalid_tests` contains jsons whose Python code compile, but their tests do not 
* `needs_postprocessing` these contain outputs of LLMs that do not conform strictly to the `schema` but they are still useful 
* `repaired_needs_postprocessing_files` contains all of the files from `needs_postprocessing` that are automatically repaired using Llama 3 and now pass the json schema validation. I have not tried to compile either the Python code or the tests for these json files 

If you just want to use the data I encourage you to use `good_quality` and `repaired_needs_postprocessing_files` and filter them further 

to run, try:

```bash 
python SyntheticDataGenerator.py
```
## Data Card 

Focusing on the `good_quality` folder, below is the number of data points per model (calculated on a small sample early on during the process)

```
mistral:latest: 355
llama3:latest: 41
qwen2:7b: 34
gemma2:27b: 28
aya:35b: 24
phi3:14b: 21
mistral-nemo:latest: 18
codestral:latest: 12
phi4:latest: 10
llama3.1:8b: 10
command-r7b:latest: 8
gemma2:27b-instruct-q5_K_S: 8
deepseek-coder:33b: 7
codebooga:latest: 6
codeqwen:7b: 6
mistral:7b-instruct: 5
codellama:34b: 5
codestral:22b: 5
llama2:latest: 5
codegemma:7b: 4
codegeex4:9b: 3
phind-codellama:34b: 2
deepseek-coder-v2:16b: 1
deepseek-r1:32b: 1
codeup:latest: 1
```

Please note that there are duplicates in this folder particularly it seems that `mistral` really likes to generate `Anagram` questions. These are the duplicate questions that have the same `titles` but might have different implementations or `unit tests` 

```
'Anagram Detector (Hard)': 49
Anagram Detector (Hard): 12
'Anagram Checker (Hard)': 9
Anagram Detection (Hard): 9
'Anagram Finder (Hard)': 8
'Anagram Detection (Hard)': 6
Anagram Checker (Hard): 6
Easy: Sum of Digits: 6
'Levenshtein Distance Calculator (Easy)': 4
Prime Factorization (Hard): 4
Fibonacci Sequence Generator (Hard): 4
'Levenshtein Distance Calculator (Hard)': 3
Subsequence Sum Checker (Hard): 3
'Palindrome with Special Characters Checker (Medium)': 3
'Palindrome with Special Characters Checker (Easy)': 3
Hard: Longest Common Subsequence: 3
Anagram Checker (Medium): 3
'Palindromic Substrings Count Finder (Hard)': 3
'Anagram Finder (Medium)': 3
Capitalize First Letter of Each Word: 3
Palindrome Checker (Hard): 3
Prime Factorization: 3
Longest Common Subsequence: 3
"Anagram Detector (Hard): 2
'Check if a given string contains all unique characters (Easy)': 2
Medium: Reverse Words in a String: 2
Hard: Longest Increasing Subsequence: 2
Euler's Totient Function: 2
Easy: Counting Vowels: 2
Palindrome Checker: 2
Fibonacci Sequence Generator (Medium): 2
'Palindromic Substrings Finder (Medium)': 2
"Anagram Finder (Hard): 2
'Palindromic Substrings in a String (Hard)': 2
'Palindromic Substrings Count (Hard)': 2
Easy: Reverse String: 2
Easy: Reverse Integer: 2
Sudoku Validator: 2
Maximum Sum of Subarray: 2
'Palindrome with Spaces and Punctuation Checker (Easy)': 2
Easy: Counting Islands: 2
Anagram Finder (Hard): 2
Reverse Linked List: 2
Maximum Subarray Sum: 2
'Is it anagram checker (Easy)': 2
Longest Common Prefix: 2
Even Fibonacci Numbers: 2
```
## Introduction
The good examples of synthetic python codes exist in the `good_quality` folder. To create more synthetic examples, you need to have your models on Ollama. The code automatically pulls all of the available models that are smaller than your available NVRAM on your GPU. This is to make sure the code is not spending time on swapping models in and out of NVRAM on the GPU. Once a model is loaded, the code tries to create as much data as possible but if the model is repeatedly failing to produce useful examples, the code loads another model. 

each example follows the following JSON schema

```python 
 schema = {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "code": {"type": "string"},
                        "tests": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["title", "description", "code", "tests"]
                }
```

An example of the synthetically generated python code is as below 

```json
{
    "title": "Graph Coloring Challenge (Hard)",
    "description": "You are given an undirected graph with `n` vertices and `m` edges. The task is to determine if it's possible to color the graph using exactly `k` colors such that no two adjacent vertices share the same color.\n\n#### Function Signature\n```python\ndef can_color_graph(n: int, m: int, k: int, edges: List[Tuple[int, int]]) -> str:\n```\n\n#### Input\n- `n` (int): The number of vertices in the graph. \\(1 \\leq n \\leq 1000\\).\n- `m` (int): The number of edges in the graph.\n- `k` (int): The exact number of colors to use for coloring the graph. \\(1 \\leq k \\leq n\\).\n- `edges` (List[Tuple[int, int]]): A list of tuples where each tuple contains two integers representing an edge between vertices in 0-based indexing.\n\n#### Output\n- Returns `\"YES\"` if it is possible to color the graph using exactly `k` colors under the given constraints; otherwise, returns `\"NO\"\".\n\n#### Constraints\n- The graph may contain multiple edges and self-loops.\n- You should consider all possible scenarios where `k < n`, `k = n`, and `k > n`.\n\n#### Hints\n- Consider using a backtracking approach to explore different colorings.\n- Use Depth First Search (DFS) or Breadth First Search (BFS) to traverse the graph while attempting to apply colors.\n- Pay attention to disconnected components in the graph, as they may have independent coloring constraints.",
    "code": "from typing import List, Tuple\n\ndef can_color_graph(n: int, m: int, k: int, edges: List[Tuple[int, int]]) -> str:\n    from collections import defaultdict\n    \n    def is_valid(vertex, color):\n        for neighbor in graph[vertex]:\n            if colors[neighbor] == color:\n                return False\n        return True\n    \n    def backtrack(node=0):\n        if node == n:\n            return len(set(colors)) == k\n        for color in range(1, k + 1):\n            if is_valid(node, color):\n                colors[node] = color\n                if backtrack(node + 1):\n                    return True\n                colors[node] = 0\n        return False\n    \n    graph = defaultdict(list)\n    for u, v in edges:\n        graph[u].append(v)\n        graph[v].append(u)\n    \n    colors = [0] * n\n    \n    if k < n:  # If k is less than the number of nodes, check coloring feasibility\n        return \"NO\"\n    \n    return \"YES\" if backtrack() else \"NO\"",
    "tests": [
        "assert can_color_graph(3, 2, 2, [(0, 1), (1, 2)]) == 'YES'",
        "assert can_color_graph(3, 3, 2, [(0, 1), (1, 2), (2, 0)]) == 'NO'",
        "assert can_color_graph(4, 4, 3, [(0, 1), (1, 2), (2, 3), (3, 0)]) == 'YES'",
        "assert can_color_graph(5, 0, 5, []) == 'YES'",
        "assert can_color_graph(6, 7, 4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]) == 'NO'"
    ],
    "difficulty": "super hard",
    "model": "phi4:latest",
    "style": "Facebook Hacker Cup"
}
```

## Setup
```bash
conda create --name pymetheus python=3.8
conda activate pymetheus
pip install ollama jsonschema pynvml
```
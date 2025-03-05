# Pymetheus
Synthetic Dataset of Python Code for Reinforcement Learning

## Introduction
The good examples of synthetic python codes exist in the `data` folder

each example follows the following JSON schema

```json 
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
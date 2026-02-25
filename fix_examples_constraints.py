import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

updates = [
    (1, "Input: (none)\nOutput:\nHello World", "Use print()"),
    (2, "Input: 2 3\nOutput: 5", "1 ≤ a,b ≤ 10^9"),
    (5, "Input: 2 7 5\nOutput: 7", "All numbers valid integers"),
    (6, "Input: hello\nOutput: olleh", "String length ≤ 10^5"),
    (7, "Input: [1,3,5], [2,4,6]\nOutput: [1,2,3,4,5,6]", "Arrays already sorted"),
    (8, "Input: [1,3,5,7], target=5\nOutput: index 2", "Array sorted ascending"),
    (9, "Input: Linked List: 3→2→0→4→2(loop)\nOutput: True", "List length ≤ 10^5"),
    (10, "Push: 1,2,3\nPop→3", "Use only two queues"),
    (11, "Graph with weights\nOutput: shortest path cost", "No negative weights"),
    (12, "Input: [5,3,8,4,2]\nOutput: [2,3,4,5,8]", "Use QuickSort"),
    (13, "Insert: cat, cap\nSearch: cat → True", "Only lowercase a-z"),
    (14, "Input: Graph adjacency list\nOutput: BFS/DFS order", "Graph ≤ 10^5 nodes"),
    (15, "Input: N=4\nOutput: 2 solutions", "1 ≤ N ≤ 12"),
    (16, "Input: Sudoku Grid\nOutput: Completed valid grid", "9×9 grid")
]

for pid, example, constraint in updates:
    cur.execute(
        "UPDATE problems SET examples=?, constraints=? WHERE id=?",
        (example, constraint, pid)
    )

conn.commit()
conn.close()

print("All examples and constraints updated successfully!")
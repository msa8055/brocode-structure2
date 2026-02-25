import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

problems = [
    (1, "Sum of Two Numbers", "Return the sum of two integers."),
    (1, "Check Even or Odd", "Determine if a number is even or odd."),
    
    (2, "Find Maximum", "Return the maximum of three numbers."),
    (2, "String Reverse", "Reverse a given string."),

    (3, "Merge Sorted Arrays", "Merge two sorted arrays into one sorted array."),
    (3, "Binary Search", "Implement binary search."),

    (4, "Linked List Cycle", "Detect a cycle in a linked list."),
    (4, "Stack Using Queues", "Implement stack using two queues."),

    (5, "Dijkstra Algorithm", "Find shortest path using Dijkstra’s algorithm."),
    (5, "QuickSort", "Implement QuickSort algorithm."),

    (6, "Trie Data Structure", "Implement a Trie with insert/search."),
    (6, "Graph BFS/DFS", "Implement BFS and DFS."),

    (7, "N-Queens", "Solve the N-Queens backtracking problem."),
    (7, "Sudoku Solver", "Write a Sudoku backtracking solver.")
]

for stage, title, desc in problems:
    c.execute("INSERT INTO problems (stage, title, description) VALUES (?, ?, ?)",
              (stage, title, desc))

conn.commit()
conn.close()

print("All stage problems inserted!")
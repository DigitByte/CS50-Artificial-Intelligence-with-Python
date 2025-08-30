class Node():
    """
Represents a node in the search tree.
Contains state, parent node, and action that led to this node.
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    """
Stack-based frontier for Depth-First Search (DFS).
Last-in, first-out (LIFO) structure.
    """
    def __init__(self):
        self.frontier = []

    def add(self, node):
        """Add node to the end of the frontier."""
        self.frontier.append(node)

    def contains_state(self, state):
        """Check if state exists in frontier."""
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """Check if frontier is empty."""
        return len(self.frontier) == 0

    def remove(self):
        """Remove and return last node (LIFO)."""
        if self.empty():
            raise Exception("Empty frontier")
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node

class QueueFrontier(StackFrontier):
    """
Queue-based frontier for Breadth-First Search (BFS).
First-in, first-out (FIFO) structure.
Inherits from StackFrontier but overrides remove method.
    """
    def remove(self):
        """Remove and return first node (FIFO)."""
        if self.empty():
            raise Exception("Empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node
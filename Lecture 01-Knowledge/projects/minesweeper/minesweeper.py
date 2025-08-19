import itertools
import random
import copy


class Minesweeper():
    """
Main Minesweeper game class that represents the game board and state.
Handles mine placement, game state, and basic game operations.
"""

    def __init__(self, height=8, width=8, mines=8):
        """Initialize the Minesweeper game with given dimensions and mine count."""

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()  # Stores coordinates of all mines

        # Initialize an empty field with no mines (False = no mine)
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly to the board
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True  # Mark cell as containing a mine

        # Track which mines have been correctly identified by the player
        self.mines_found = set()

    def print(self):
        """Prints a text-based representation of the board showing mine locations."""
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")  # X represents a mine
                else:
                    print("| ", end="")  # Space represents safe cell
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        """Check if a given cell contains a mine."""
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
Returns the number of mines that are within one row and column of a given cell,
not including the cell itself. This is the number shown when a cell is revealed.
        """
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column (3x3 area centered on cell)
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell is in bounds and contains a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """Check if all mines have been correctly identified (game won)."""
        return self.mines_found == self.mines


class Sentence():
    """
Logical statement about a Minesweeper game.
Represents a constraint: "These N cells contain exactly M mines."
Used for logical inference in the AI player.
"""

    def __init__(self, cells, count):
        """Initialize a sentence with a set of cells and mine count."""
        self.cells = set(cells)  # Cells involved in this constraint
        self.count = count       # Number of mines among these cells

    def __eq__(self, other):
        """Check if two sentences are equivalent."""
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """String representation for debugging."""
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
If the number of cells equals the mine count, all cells must be mines.
Returns the set of confirmed mines, or empty set if not certain.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
If the mine count is zero, all cells must be safe.
Returns the set of confirmed safe cells, or empty set if not certain.
        """
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
Update the sentence when a cell is confirmed to be a mine.
Removes the cell from consideration and decreases the mine count.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return True
        return False

    def mark_safe(self, cell):
        """
Update the sentence when a cell is confirmed to be safe.
Removes the cell from consideration (mine count remains unchanged).
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return True
        return False


class MinesweeperAI():
    """
AI player for Minesweeper that uses logical inference to play the game.
Maintains knowledge about safe cells, mines, and makes intelligent moves.
"""

    def __init__(self, height=8, width=8):
        """Initialize the AI with game dimensions and empty knowledge base."""

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()   # Known mines
        self.safes = set()   # Known safe cells

        # List of sentences about the game known to be true (knowledge base)
        self.knowledge = []

    def mark_mine(self, cell):
        """
Mark a cell as a mine and update all sentences in knowledge base.
Propagates this information through all known constraints.
        """
        if cell not in self.mines:
            self.mines.add(cell)
            for sentence in self.knowledge:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
Mark a cell as safe and update all sentences in knowledge base.
Propagates this information through all known constraints.
        """
        if cell not in self.safes:
            self.safes.add(cell)
            for sentence in self.knowledge:
                sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
Called when a cell is revealed. Updates AI's knowledge with new information.

Steps:
1. Record the move and mark cell as safe
2. Create new sentence from revealed cell's neighbors
3. Update knowledge base with new inferences
4. Make additional inferences through subset elimination
        """
        # 1) Mark that move has been made and cell is safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 2) Get all neighboring cells (3x3 area excluding center)
        neighbor_cells = []
        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2):
                neighbor_cell = (cell[0] + delta_row, cell[1] + delta_col)
                row_in_bounds = 0 <= neighbor_cell[0] < self.height
                col_in_bounds = 0 <= neighbor_cell[1] < self.width

                if neighbor_cell != cell and row_in_bounds and col_in_bounds:
                    neighbor_cells.append(neighbor_cell)

        # Adjust count by ignoring already known mines
        count_after_ignoring_mines = count
        new_cells = set()

        for neighbor in neighbor_cells:
            if neighbor in self.mines:
                count_after_ignoring_mines -= 1  # Mine already accounted for
            elif neighbor not in self.safes and neighbor not in self.mines:
                new_cells.add(neighbor)  # Unknown cell to include in sentence

        # Create new sentence and add to knowledge base if it contains cells
        new_sentence = Sentence(new_cells, count_after_ignoring_mines)
        if len(new_sentence.cells) > 0:
            self.knowledge.append(new_sentence)

        # 3) Continuously update knowledge until no more conclusions can be drawn
        changes_made = True
        while changes_made:
            changes_made = False

            # Create a copy to avoid modifying while iterating
            for sentence in copy.deepcopy(self.knowledge):
                # Check for newly identifiable mines or safe cells
                new_mines = sentence.known_mines()
                new_safes = sentence.known_safes()

                if new_mines:
                    for mine in new_mines:
                        self.mark_mine(mine)
                        changes_made = True

                if new_safes:
                    for safe in new_safes:
                        self.mark_safe(safe)
                        changes_made = True

        # 4) Make additional inferences using subset elimination
        # If one sentence is a subset of another, we can infer a new sentence
        new_inferences = []
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                sentence_1 = self.knowledge[i]
                sentence_2 = self.knowledge[j]

                if sentence_1.cells.issubset(sentence_2.cells):
                    new_cells = sentence_2.cells - sentence_1.cells
                    new_count = sentence_2.count - sentence_1.count
                    new_sentence = Sentence(new_cells, new_count)

                    # Add new inference if it's meaningful
                    if len(new_sentence.cells) > 0 and new_sentence not in self.knowledge:
                        new_inferences.append(new_sentence)

                elif sentence_2.cells.issubset(sentence_1.cells):
                    new_cells = sentence_1.cells - sentence_2.cells
                    new_count = sentence_1.count - sentence_2.count
                    new_sentence = Sentence(new_cells, new_count)

                    if len(new_sentence.cells) > 0 and new_sentence not in self.knowledge:
                        new_inferences.append(new_sentence)

        # Add all new inferences to knowledge base
        self.knowledge.extend(new_inferences)

    def make_safe_move(self):
        """
Returns a safe cell to choose (known to be safe and not yet played).
This is the AI's preferred move when safe options are available.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made and safe_cell not in self.mines:
                return safe_cell
        return None

    def make_random_move(self):
        """
Returns a random move when no safe moves are known.
Chooses from cells that haven't been played and aren't known mines.
        """
        # Check if game is complete (all non-mine cells played)
        total_cells = self.height * self.width
        if len(self.moves_made) + len(self.mines) >= total_cells:
            return None

        # Generate all possible cells and filter out invalid ones
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_moves.append(cell)

        # Return random choice from valid moves (or None if none exist)
        return random.choice(possible_moves) if possible_moves else None
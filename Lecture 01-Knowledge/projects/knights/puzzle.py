from logic import *

# Define symbols for each possible role:
# Each character (A, B, C) can either be a Knight (always tells the truth)
# or a Knave (always lies). These symbols will be used in logical formulas.
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# -------------------------------
# Puzzle 0
# A says "I am both a knight and a knave."
# -------------------------------
knowledge0 = And(
    # Basic structural rules:
    Or(AKnight, AKnave),            # A must be either knight OR knave
    Not(And(AKnight, AKnave)),      # A cannot be both

    # If A is a knight, then A’s statement must be true → (AKnight ∧ AKnave)
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave, then A’s statement must be false → NOT(AKnight ∧ AKnave)
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# -------------------------------
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
# -------------------------------
knowledge1 = And(
    # Structural rules for A and B
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a knight, then the statement is true → A and B are both knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, then the statement is false → NOT(A and B both knaves)
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# -------------------------------
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# -------------------------------
knowledge2 = And(
    # Structure: A and B cannot be both knight and knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A’s statement:
    # If A is a knight, then A and B must be both knights OR both knaves.
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If A is a knave, then that claim is false.
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # B’s statement:
    # If B is a knight, then A and B must be different kinds (one knight, one knave).
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # If B is a knave, then that claim is false.
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# -------------------------------
# Puzzle 3
# A says either "I am a knight." or "I am a knave." (unknown which).
# B says "A said 'I am a knave'." and "C is a knave."
# C says "A is a knight."
# -------------------------------
knowledge3 = And(
    # Structure rules: each person is exactly one of knight/knave
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave), Not(And(CKnight, CKnave)),

    # A’s possible statements:
    Or(
        # Case 1: A said "I am a knight."
        And(
            Implication(AKnight, AKnight),      # Knight says true
            Implication(AKnave, Not(AKnight))   # Knave lies
        ),
        # Case 2: A said "I am a knave."
        And(
            Implication(AKnight, AKnave),       # Knight would tell truth → impossible
            Implication(AKnave, Not(AKnave))    # Knave would lie → contradiction
        )
    ),

    # B’s statement about A:
    # If B is a knight → A actually said "I am a knave"
    Implication(BKnight, And(
                    Implication(AKnight, AKnave),
                    Implication(AKnave, Not(AKnave))
                )),
    # If B is a knave → can’t trust their statement (ignored)

    # B’s second statement: "C is a knave."
    Implication(BKnight, CKnave),   # If B is truthful, C is knave
    Implication(BKnave, Not(CKnave)),

    # C’s statement: "A is a knight."
    Implication(CKnight, AKnight),  # Truthful if knight
    Implication(CKnave, Not(AKnight)) # Lie if knave
)


def main():
    # All possible role symbols
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]

    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]

    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            # For each symbol, check if it must be true given the knowledge
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
    
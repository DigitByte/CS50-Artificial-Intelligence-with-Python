import itertools

class Sentence():
    """
Base class for all logical sentences in propositional logic.
Provides common interface for evaluation, formula representation, and symbol extraction.
"""

    def evaluate(self, model):
        """Evaluates the logical sentence against a given model (truth assignment)."""
        raise Exception("nothing to evaluate")

    def formula(self):
        """Returns string formula representing logical sentence in symbolic notation."""
        return ""

    def symbols(self):
        """Returns a set of all propositional symbols (variables) in the logical sentence."""
        return set()

    @classmethod
    def validate(cls, sentence):
        """Validates that the input is a proper logical sentence."""
        if not isinstance(sentence, Sentence):
            raise TypeError("must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):
        """Parenthesizes an expression if not already parenthesized to ensure proper precedence."""
        def balanced(s):
            """Checks if a string has balanced parentheses."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        # Don't parenthesize if already parenthesized or single symbol
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Symbol(Sentence):
    """Represents a propositional symbol (variable) in logical expressions."""

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        """Evaluates the symbol by looking up its truth value in the model."""
        try:
            return bool(model[self.name])
        except KeyError:
            raise Exception(f"variable {self.name} not in model")

    def formula(self):
        """Returns the symbol name as its formula representation."""
        return self.name

    def symbols(self):
        """Returns a set containing only this symbol."""
        return {self.name}


class Not(Sentence):
    """Represents logical negation (¬) operation."""

    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", hash(self.operand)))

    def __repr__(self):
        return f"Not({self.operand})"

    def evaluate(self, model):
        """Evaluates the negation: returns the opposite of the operand's truth value."""
        return not self.operand.evaluate(model)

    def formula(self):
        """Returns formula with negation symbol and proper parentheses."""
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        """Returns symbols from the operand (negation doesn't introduce new symbols)."""
        return self.operand.symbols()


class And(Sentence):
    """Represents logical conjunction (∧) operation with multiple conjuncts."""

    def __init__(self, *conjuncts):
        for conjunct in conjuncts:
            Sentence.validate(conjunct)
        self.conjuncts = list(conjuncts)

    def __eq__(self, other):
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self):
        return hash(
            ("and", tuple(hash(conjunct) for conjunct in self.conjuncts))
        )

    def __repr__(self):
        conjunctions = ", ".join(
            [str(conjunct) for conjunct in self.conjuncts]
        )
        return f"And({conjunctions})"

    def add(self, conjunct):
        """Adds another conjunct to the conjunction."""
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def evaluate(self, model):
        """Evaluates conjunction: returns True only if ALL conjuncts are True."""
        return all(conjunct.evaluate(model) for conjunct in self.conjuncts)

    def formula(self):
        """Returns formula with ∧ operator and proper parentheses."""
        if len(self.conjuncts) == 1:
            return self.conjuncts[0].formula()
        return " ∧ ".join([Sentence.parenthesize(conjunct.formula())
                           for conjunct in self.conjuncts])

    def symbols(self):
        """Returns union of all symbols from all conjuncts."""
        return set.union(*[conjunct.symbols() for conjunct in self.conjuncts])


class Or(Sentence):
    """Represents logical disjunction (∨) operation with multiple disjuncts."""

    def __init__(self, *disjuncts):
        for disjunct in disjuncts:
            Sentence.validate(disjunct)
        self.disjuncts = list(disjuncts)

    def __eq__(self, other):
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __hash__(self):
        return hash(
            ("or", tuple(hash(disjunct) for disjunct in self.disjuncts))
        )

    def __repr__(self):
        disjuncts = ", ".join([str(disjunct) for disjunct in self.disjuncts])
        return f"Or({disjuncts})"

    def evaluate(self, model):
        """Evaluates disjunction: returns True if ANY disjunct is True."""
        return any(disjunct.evaluate(model) for disjunct in self.disjuncts)

    def formula(self):
        """Returns formula with ∨ operator and proper parentheses."""
        if len(self.disjuncts) == 1:
            return self.disjuncts[0].formula()
        return " ∨  ".join([Sentence.parenthesize(disjunct.formula())
                            for disjunct in self.disjuncts])

    def symbols(self):
        """Returns union of all symbols from all disjuncts."""
        return set.union(*[disjunct.symbols() for disjunct in self.disjuncts])


class Implication(Sentence):
    """Represents logical implication (=>) operation: antecedent => consequent."""

    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __eq__(self, other):
        return (isinstance(other, Implication)
                and self.antecedent == other.antecedent
                and self.consequent == other.consequent)

    def __hash__(self):
        return hash(("implies", hash(self.antecedent), hash(self.consequent)))

    def __repr__(self):
        return f"Implication({self.antecedent}, {self.consequent})"

    def evaluate(self, model):
        """Evaluates implication: equivalent to ¬antecedent ∨ consequent."""
        return ((not self.antecedent.evaluate(model))
                or self.consequent.evaluate(model))

    def formula(self):
        """Returns formula with => operator and proper parentheses."""
        antecedent = Sentence.parenthesize(self.antecedent.formula())
        consequent = Sentence.parenthesize(self.consequent.formula())
        return f"{antecedent} => {consequent}"

    def symbols(self):
        """Returns union of symbols from both antecedent and consequent."""
        return set.union(self.antecedent.symbols(), self.consequent.symbols())


class Biconditional(Sentence):
    """Represents logical biconditional (<=>) operation: left if and only if right."""

    def __init__(self, left, right):
        Sentence.validate(left)
        Sentence.validate(right)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return (isinstance(other, Biconditional)
                and self.left == other.left
                and self.right == other.right)

    def __hash__(self):
        return hash(("biconditional", hash(self.left), hash(self.right)))

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

    def evaluate(self, model):
        """Evaluates biconditional: both sides have same truth value."""
        return ((self.left.evaluate(model)
                 and self.right.evaluate(model))
                or (not self.left.evaluate(model)
                    and not self.right.evaluate(model)))

    def formula(self):
        """Returns formula with <=> operator and proper parentheses."""
        left = Sentence.parenthesize(str(self.left))
        right = Sentence.parenthesize(str(self.right))
        return f"{left} <=> {right}"

    def symbols(self):
        """Returns union of symbols from both left and right sides."""
        return set.union(self.left.symbols(), self.right.symbols())


def model_check(knowledge, query):
    """
Performs model checking to verify if knowledge base entails query.
Uses recursive depth-first search through all possible truth assignments.

Args:
knowledge: Sentence representing the knowledge base
query: Sentence representing the query to check

Returns:
bool: True if knowledge entails query, False otherwise
"""

    def check_all(knowledge, query, symbols, model):
        """
Recursive helper function that checks all possible truth assignments.

Args:
knowledge: Knowledge base sentence
query: Query sentence
symbols: Set of remaining symbols to assign truth values
model: Current partial truth assignment

Returns:
bool: True if entailment holds for all completions of current model
"""

        # Base case: all symbols have been assigned truth values
        if not symbols:
            # If knowledge base is true in this model, query must also be true
            if knowledge.evaluate(model):
                return query.evaluate(model)
            # If KB is false, entailment holds vacuously (ex falso quodlibet)
            return True
        else:
            # Recursive case: assign truth values to remaining symbols
            remaining = symbols.copy()
            p = remaining.pop()  # Get next symbol to assign

            # Create two models: one where symbol p is True, one where False
            model_true = model.copy()
            model_true[p] = True

            model_false = model.copy()
            model_false[p] = False

            # Check entailment holds in both possible assignments
            return (check_all(knowledge, query, remaining, model_true) and
                    check_all(knowledge, query, remaining, model_false))

    # Get all propositional symbols from both knowledge base and query
    symbols = set.union(knowledge.symbols(), query.symbols())

    # Start recursive checking with empty model
    return check_all(knowledge, query, symbols, dict())
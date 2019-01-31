'''
maze_knowledge_base.py

Specifies a simple, Conjunctive Normal Form Propositional
Logic Knowledge Base for use in Grid Maze pathfinding problems
with side-information.
'''
from maze_clause import MazeClause
import unittest
import itertools

class MazeKnowledgeBase:

    def __init__ (self):
        self.clauses = set()

    def tell (self, clause):
        """
        Adds the given clause to the CNF MazeKnowledgeBase
        Note: we expect that no clause added this way will ever
        make the KB inconsistent (you need not check for this)
        """
        self.clauses.add(clause)

    def ask (self, query):
        """
        Given a MazeClause query, returns True if the KB entails
        the query, False otherwise
        """
        clauses = self.clauses.copy()
        new = set()
        negation = set()

        for i in query.props.items():
            prop, neg = i[0], i[1]
            #query.props[prop] = not neg
            negation.add(MazeClause([(prop, not neg)]))

        clauses |= negation

        while True:
            clause_combinations = itertools.combinations(clauses, 2)
            for first_clause, second_clause in clause_combinations:
                resolvents = MazeClause.resolve(first_clause, second_clause)
                if any(clause.is_empty() for clause in resolvents):
                    return True
                new |= resolvents
            if new.issubset(clauses):
                return False
            clauses |= new


class MazeKnowledgeBaseTests(unittest.TestCase):
    def test_mazekb1(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("X", (1, 1)), True)])))

    def test_mazekb2(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), False)]))
        kb.tell(MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("Y", (1, 1)), True)])))

    def test_mazekb3(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)]))
        kb.tell(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), True), (("Z", (1, 1)), False)]))
        kb.tell(MazeClause([(("X", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("W", (1, 1)), True)])))
        self.assertFalse(kb.ask(MazeClause([(("Y", (1, 1)), False)])))

    def test_mazekb4(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), False), (("Z", (1, 1)), False), (("S", (1, 1)), True)]))
        kb.tell(MazeClause([(("S", (1, 1)), False), (("T", (1, 1)), False)]))
        kb.tell(MazeClause([(("X", (1, 1)), True), (("T", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), True)]))
        kb.tell(MazeClause([(("T", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("Z", (1, 1)), False)])))

    def test_mazekb5(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), False), (("Z", (1, 1)), False), (("S", (1, 1)), True)]))
        kb.tell(MazeClause([(("S", (1, 1)), False), (("T", (1, 1)), False)]))
        kb.tell(MazeClause([(("X", (1, 1)), True), (("T", (1, 1)), True)]))
        kb.tell(MazeClause([(("W", (1, 1)), True)]))
        kb.tell(MazeClause([(("T", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("Z", (1, 1)), True), (("W", (1, 1)), True)])))

    def test_mazekb6(self):
        kb = MazeKnowledgeBase()
        kb.tell(MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("Z", (1, 1)), False)]))
        kb.tell(MazeClause([(("X", (1, 1)), True)]))
        self.assertFalse(kb.ask(MazeClause([(("Z", (1, 1)), False)])))
        kb.tell(MazeClause([(("Y", (1, 1)), True)]))
        self.assertTrue(kb.ask(MazeClause([(("Z", (1, 1)), False)])))


if __name__ == "__main__":
    unittest.main()

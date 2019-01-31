'''
maze_clause.py

Specifies a Propositional Logic Clause formatted specifically
for Grid Maze Pathfinding problems. Clauses are a disjunction of
MazePropositions (2-tuples of (symbol, location)) mapped to
their negated status in the sentence.
'''
import unittest

class MazeClause:

    def __init__(self, props):
        """
        Constructor parameterized by the propositions within this clause;
        argument props is a list of MazeClauses:
        [("P", (1, 1)), ("B", (1, 2)), ...]
        """
        self.props = {}
        self.valid = False

        for i in props:
            prop, neg = i[0], i[1]
            if prop not in self.props:
                self.props[prop] = neg
            elif self.props[prop] != neg:
                self.valid = True
                self.props = {}
                break


    def get_prop(self, prop):
        """
        Returns:
          - None if the requested prop is not in the clause
          - True if the requested prop is positive in the clause
          - False if the requested prop is negated in the clause
        """
        if prop not in self.props:
            return None
        return self.props[prop]

    def is_valid(self):
        """
        Returns:
          - True if this clause is logically equivalent with True
          - False otherwise
        """
        return self.valid

    def is_empty(self):
        """
        Returns:
          - True if this is the Empty Clause
          - False otherwise
        (NB: valid clauses are not empty)
        """
        return not self.valid and len(self.props) == 0

    def __eq__(self, other):
        """
        Defines equality comparator between MazeClauses: only if they
        have the same props (in any order) or are both valid
        """
        return self.props == other.props and self.valid == other.valid

    def __hash__(self):
        """
        Provides a hash for a MazeClause to enable set membership
        """
        # Hashes an immutable set of the stored props for ease of
        # lookup in a set
        return hash(frozenset(self.props.items()))

    # Hint: Specify a __str__ method for ease of debugging (this
    # will allow you to "print" a MazeClause directly to inspect
    # its composite literals)
    # def __str__ (self):
    #     return ""

    @staticmethod
    def resolve(c1, c2):
        """
        Returns a set of MazeClauses that are the result of resolving
        two input clauses c1, c2 (Hint: result will only ever be a set
        of 0 or 1 MazeClause, but it being a set is convenient for the
        inference engine)
        """
        results = set()
        c1_list = list(c1.props.items())
        c2_list = list(c2.props.items())
        for i in c1.props:
            #print(i)
            prop, neg = i, c1.props[i]
            #print(prop)
            #print(neg)
            if prop in c2.props and c2.props[prop] != neg:
                c3 = [item for item in c1_list if item[0] != prop]
                #print(c3)
                c4 = [item for item in c2_list if item[0] != prop]
                #print(c4)
                clauses = c3 + c4
                new_maze_clause = MazeClause(clauses)
                if not new_maze_clause.is_valid():
                    results.add(new_maze_clause)
        #print(results)
        return results


class MazeClauseTests(unittest.TestCase):
    def test_mazeprops1(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (2, 1)), True), (("Y", (1, 2)), False)])
        self.assertTrue(mc.get_prop(("X", (1, 1))))
        self.assertTrue(mc.get_prop(("X", (2, 1))))
        self.assertFalse(mc.get_prop(("Y", (1, 2))))
        self.assertTrue(mc.get_prop(("X", (2, 2))) is None)
        self.assertFalse(mc.is_empty())

    def test_mazeprops2(self):
        mc = MazeClause([(("X", (1, 1)), True), (("X", (1, 1)), True)])
        self.assertTrue(mc.get_prop(("X", (1, 1))))
        self.assertFalse(mc.is_empty())

    def test_mazeprops3(self):
        mc = MazeClause([(("X", (1, 1)), True), (("Y", (2, 1)), True), (("X", (1, 1)), False)])
        self.assertTrue(mc.is_valid())
        self.assertTrue(mc.get_prop(("X", (1, 1))) is None)
        self.assertFalse(mc.is_empty())

    def test_mazeprops4(self):
        mc = MazeClause([])
        self.assertFalse(mc.is_valid())
        self.assertTrue(mc.is_empty())

    def test_mazeprops5(self):
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops6(self):
        mc1 = MazeClause([(("X", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([]) in res)

    def test_mazeprops7(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (2, 2)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), True), (("Y", (2, 2)), True)]) in res)

    def test_mazeprops8(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops9(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), True), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 0)

    def test_mazeprops10(self):
        mc1 = MazeClause([(("X", (1, 1)), True), (("Y", (1, 1)), False), (("Z", (1, 1)), True)])
        mc2 = MazeClause([(("X", (1, 1)), False), (("Y", (1, 1)), False), (("W", (1, 1)), False)])
        res = MazeClause.resolve(mc1, mc2)
        self.assertEqual(len(res), 1)
        self.assertTrue(MazeClause([(("Y", (1, 1)), False), (("Z", (1, 1)), True), (("W", (1, 1)), False)]) in res)

if __name__ == "__main__":
    unittest.main()

from z3 import *
from functools import reduce


class Vocab:
    def __init__(self):
        self.cnt = 0

    def fresh(self, prefix='', sort=IntSort()):
        self.cnt += 1
        return Const(prefix + '$' + str(self.cnt), sort)

    def fresh_pt(self, prefix='', sort=IntSort()):
        return (self.fresh(prefix + 'x'), self.fresh(prefix + 'y'))


def eq(p1, p2): return And(p1[0] == p2[0], p1[1] == p2[1])
def neq(p1, p2): return Not(eq(p1, p2))
def lt(p1, p2): return Or(p1[0] < p2[0], And(p1[0] == p2[0], p1[1] < p2[1]))


def ptin(p, lp): return Or(eq(p, p0) for p0 in lp)

class RelationOps:
    def __init__(self, vocab):
        self.vocab = vocab
        
    def comp(self, r1, r2):
        '''Composes relations on points'''
        p = self.vocab.fresh_pt()
        return lambda p1, p2: Exists(list(p), And(r1(p1, p), r2(p, p2)))


def switch_expr(expr, choices):
    return reduce(lambda rest, ichoice: If(expr == ichoice[0], ichoice[1], rest),
                  enumerate(choices), False)

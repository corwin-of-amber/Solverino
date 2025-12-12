from z3 import Or, Solver as Z3Solver
from logic import Vocab
from constraints import Placement


class Solver:

    def __init__(self):
        self.pentas = []

    def add_pentas(self, pentas):
        self.pentas += pentas

    def constraints(self):
        vocab = Vocab()

        placements = [Placement(penta, vocab.fresh_pt(), vocab.fresh('v')) 
                      for penta in self.pentas]

        width, height = len(self.pentas), 5

        self.placements = placements
        
        return [Or(p.ptin((x, y)) for p in placements)
                for x in range(width) for y in range(height)]

    def check(self):
        s = Z3Solver()
        s.add(*self.constraints())
        self.solver = s
        return s.check()

    def solution(self):
        m = self.solver.model()
        return [p.from_model(m) for p in self.placements]
        
        
from logic import ptin, switch_expr


class Placement:
    def __init__(self, penta, at, vari):
        self.penta = penta
        self.at = at
        self.vari = vari

    def translate(self, coords, shift):
        dx, dy = shift
        return [(x + dx, y + dy) for x, y in coords]

    def ptin(self, pt):
        vs = self.penta.variations()
        return switch_expr(self.vari,
                           [ptin(pt, self.translate(v.blocks, self.at)) for v in vs])

    def instantiate(self, at, vari):
        return Placement(self.penta.variations()[vari], at, 0)

    def from_model(self, m):
        return self.instantiate(tuple(m[self.at[i]].as_long() for i in [0,1]),
                                m[self.vari].as_long())


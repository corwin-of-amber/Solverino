from presentation_forms import HTMLGrid


class Penta:
    def __init__(self, blocks):
        assert(len(blocks) == 5)
        self.blocks = blocks

    def __eq__(self, other):
        return set(self.blocks) == set(other.blocks)

    def size(self):
        return tuple([max(p[i] for p in self.blocks) + 1 for i in [0, 1]])
    
    def flipx(self):
        w, _ = self.size()
        return Penta([(w-1-x, y) for x,y in self.blocks])
    
    def flipy(self):
        _, h = self.size()
        return Penta([(x, h-1-y) for x,y in self.blocks])

    def transpose(self):
        return Penta([(y, x) for x,y in self.blocks])

    def rot90cw(self):
        return self.transpose().flipx()

    def variations(self):
        return [shape for p in [self, self.transpose()]
                for shape in [p, p.rot90cw(), p.rot90cw().rot90cw(), p.rot90cw().rot90cw().rot90cw()]]

    def like(self, other):
        return other in self.variations()
        #return any(shape == other for shape in self.variations())
        
    def _repr_html_(self):
        return HTMLGrid([(x, y, '') for x, y in self.blocks])._repr_html_()


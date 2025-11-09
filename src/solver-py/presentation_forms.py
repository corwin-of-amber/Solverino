class table_repr:
    def __init__(self, iter):
        self.rows = list(iter)
        self.td_style = "text-align: left"
        self.col_styles = {}
    def _cell_html(self, obj):
        if hasattr(obj, '_repr_html_'): return obj._repr_html_()
        if hasattr(obj, '_repr_svg_'): return obj._repr_svg_()
        else: return str(obj)  # @todo escape
    def _td(self, obj, col_index):
        style = ";".join(x for x in [self.td_style, self.col_styles.get(col_index, None)] if x)
        return f'<td style="{style}">{self._cell_html(obj)}</td>'
    def _tr(self, data):
        if not (isinstance(data, list) or isinstance(data, tuple)):
            data = (data,)
        return f'<tr>{"".join(self._td(v, i) for i, v in enumerate(data))}</tr>'
    def _repr_html_(self):
        return f'<table style="background: white">{"".join(map(self._tr, self.rows))}</table>'


def vertically(iter):
    return table_repr([x] for x in iter)


class HTMLGrid:
    def __init__(self, cells, css_class=[], styles=[]):
        self.cells = cells
        self.css_class = css_class
        self.styles = styles
        
    def _repr_html_(self):
        c = [f'<div style="grid-row: {y+1}; grid-column: {x+1};" data-txt="{txt}" class="htmlgrid-cell">{txt}</div>'
             for x,y,txt in self.cells]       
        return '''
          <style>
            .htmlgrid-root { display: grid; grid-auto-columns: 1fr; width: fit-content; text-align: center; }
            .htmlgrid-cell { line-height: 1; width: 1.25em; height: 1.25em; background: #ddd; border: 0.5px solid #aaa; }
          </style>''' + f'''<style>{''.join(self.styles)}</style>
          <div class="htmlgrid-root" style="grid-rows: 3; ">
            {'\n'.join(c)}
          </div>'''


class Legend:
    """
    Generates a table of objects by consecutive keys.
    """
    def __init__(self, by=lambda x: x, start_at=0):
        self.keys = {}  # item -> key
        self.items = [] # (key, item)
        self.by = by
        self._keygen = iter(range(start_at, 2 ** 31))

    def key(self, item):
        k = self.by(item)
        v = self.keys.get(k, None)
        if v is None:
            v = self._keygen.__next__()
            self.keys[k] = v
            self.items.append((v, item))
        return v
    
    def _repr_html_(self):
        return table_repr(self.items)._repr_html_()
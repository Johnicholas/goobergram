from linear_constraints import Number, Compound, equate

def nonself(d):
    return dict((k, v) for k, v in d.items() if k != 'self')

class Figure(Compound):
    def __init__(self):
        super(Figure, self).__init__({})
    def draw(self):
        for part in self.get_parts():
            if hasattr(part, 'draw'):
                part.draw()

class Point(Figure):
    def __init__(self):
        super(Point, self).__init__()
        x, y = Number(), Number()
        self.add_parts(nonself(locals()))

class Label(Point):
    def __init__(self, text):
        super(Label, self).__init__()
        self.text = text
    def draw(self):
        print 'label %g %g %r' % (self.x.get_value(),
                                  self.y.get_value(),
                                  self.text)

class Line(Figure):
    def __init__(self):
        super(Line, self).__init__()
        start = Point()
        end = Point()
        center = Point()
        self.add_parts(nonself(locals()))
        equate(center, (start + end) / 2)
    def draw(self):
        coords = [self.start.x, self.start.y,
                  self.end.x, self.end.y]
        print 'draw %s %s %s %s' % tuple(c.get_value() for c in coords)

class HLine(Line):
    def __init__(self):
        super(HLine, self).__init__()
        y, length = Number(), Number()
        self.add_parts(nonself(locals()))
        equate(self.start.y, y)
        equate(self.end.y, y)
        equate(self.start.x + length, self.end.x)

class VLine(Line):
    def __init__(self):
        super(VLine, self).__init__()
        x, length = Number(), Number()
        self.add_parts(nonself(locals()))
        equate(self.start.x, x)
        equate(self.end.x, x)
        equate(self.start.y + length, self.end.y)

class Box(Figure):
    def __init__(self):
        super(Box, self).__init__()
        left, right = VLine(), VLine()
        top, bottom = HLine(), HLine()
        nw, n, ne, e, se, s, sw, w, c = map(lambda i: Point(), range(9))
        ht, wd = Number(), Number()
        self.add_parts(nonself(locals()))

        equate(nw, left.start)
        equate(nw, top.start)
        equate(ne, right.start)
        equate(ne, top.end)
        equate(sw, left.end)
        equate(sw, bottom.start)
        equate(se, right.end)
        equate(se, bottom.end)

        equate(n, (nw + ne) / 2)
        equate(s, (sw + se) / 2)
        equate(w, (nw + sw) / 2)
        equate(e, (ne + se) / 2)

        equate(c, (n + s) / 2)

        equate(ht, left.length)
        equate(wd, top.length)

class LabelBox(Box):
    def __init__(self, text):
        super(LabelBox, self).__init__()
        label = Label(text)
        self.add_parts(nonself(locals()))
        equate(label, self.c) # XXX does this work?

l1 = Line()
equate(l1.end.x, 5)
equate(l1.end.y, (l1.start.y + 10))
equate(l1.start, dict(x=3, y=4))
l1.draw()

l2 = HLine()
l2.draw()                       # XXX should raise an error
equate(l2.y, 42)
equate(l2.length, 10)
equate(l2.start.x, 1)
l2.draw()

print
lb = LabelBox('Aloha')
equate(lb.top, l2)
equate(lb.ht, 100)
lb.draw()                       # XXX I think the output is wrong -- checkme

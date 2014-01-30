"""
>>> d = Domain('mydomain')
>>> stmt = d.select(Star())
>>> stmt.where(d.column('city') == 'Seattle').to_sql()
"select * from mydomain where city = 'Seattle'"

>>> city = d.column('city')
>>> stmt.where((city == 'Seattle') | (city == 'Portland')).to_sql()
"select * from mydomain where (city = 'Seattle') or (city = 'Portland')"
"""

import re

from .compiler import SimpleCompiler
from .core import *
from .node import *


class Every(Field):
    def __init__(self, field):
        self.field = field


class ItemName(Field, Literal):
    def __init__(self):
        Field.__init__(self, 'itemName()')
        Literal.__init__(self, 'itemName()')


class Star(Literal):
    def __init__(self):
        self.value = '*'


class Count(Field, Literal):
    def __init__(self):
        Field.__init__(self, 'count(*)')
        Literal.__init__(self, 'count(*)')


class BetweenOp(BinaryOp):
    pass


class PostgresField(Field):
    def between(self, lower, upper):
        return BetweenOp(self, (lower, upper))


class Compiler(SimpleCompiler):
    reserved_words = [
        'or', 'and', 'not', 'from', 'where', 'select', 'like', 'null', 'is',
        'order', 'by', 'asc', 'desc', 'in', 'between', 'limit',
        'every'
    ]

    def __init__(self):
        super(Compiler, self).__init__()
        operators = [
            (LikeOp, 'like'),
            (NotLikeOp, 'not like'),
            (IsOp, 'is'),
            (IsNotOp, 'is not'),
        ]
        for op in operators:
            self.operators[op[0]] = op[1]

    def quote_field(self, field):
        FIELD_RE = re.compile(r'^[a-z0-9_$]+$', re.I)
        if not FIELD_RE.match(field.name) or field.name in self.reserved_words:
            return "`{}`".format(field.name.replace('`', '``'))
        else:
            return super(Compiler, self).quote_field(field)

    def quote_string(self, expr):
        return expr.replace('"', '""')

    def compile_field(self, field):
        if isinstance(field, Every):
            return "every({})".format(self.compile_field(field.field))
        return super(Compiler, self).compile_field(field)

    def compile_string(self, expr):
        return "'" + self.quote_string(expr) + "'"

    def compile_binary_op(self, op, depth=0):
        if isinstance(op, BetweenOp):
            return "{} between {} and {}".format(
                self.compile_expr(op.left, depth + 1),
                self.compile_expr(op.right[0], depth + 1),
                self.compile_expr(op.right[1], depth + 1)
            )

        return super(Compiler, self).compile_binary_op(op, depth)


class Domain(SimpleTable):
    def field_promote(self, name):
        if isinstance(name, Node):
            return name
        return PostgresField(name)

    def to_sql(self):
        compiler = Compiler()
        return compiler.compile(self)

    def column(self, name):
        return self.field_promote(name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

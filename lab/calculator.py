import operator as op
from plyplus import Grammar, STransformer

calc_grammar = Grammar("""
    start: add;
    ?add: (add add_symbol)? mul;
    ?mul: (mul mul_symbol)? atom;
    @atom: neg | number | '\(' add '\)';
    neg: '-' atom;
    number: '[\d.]+';
    mul_symbol: '\*' | '/';
    add_symbol: '\+' | '-';
    WS: '[ \t]+' (%ignore);
""")

class Calc(STransformer):

    def _bin_operator(self, exp):
        arg1, operator_symbol, arg2 = exp.tail

        operator_func = { '+': op.add, '-': op.sub, '*': op.mul, '/': op.div }[operator_symbol]

        return operator_func(arg1, arg2)

    number      = lambda self, exp: float(exp.tail[0])
    neg         = lambda self, exp: -exp.tail[0]
    __default__ = lambda self, exp: exp.tail[0]

    add = _bin_operator
    mul = _bin_operator

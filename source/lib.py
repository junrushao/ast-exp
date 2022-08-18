# Taken and modified from: https://github.com/python/typeshed/blob/master/stdlib/_ast.pyi


class AST:
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None


class mod(AST):
    ...


class FunctionType(mod):
    argtypes: list[expr]
    returns: expr


class Module(mod):
    body: list[stmt]


class Interactive(mod):
    body: list[stmt]


class Expression(mod):
    body: expr


class stmt(AST):
    ...


class FunctionDef(stmt):
    name: _identifier
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None


class AsyncFunctionDef(stmt):
    name: _identifier
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None


class ClassDef(stmt):
    name: _identifier
    bases: list[expr]
    keywords: list[keyword]
    body: list[stmt]
    decorator_list: list[expr]


class Return(stmt):
    value: expr | None


class Delete(stmt):
    targets: list[expr]


class Assign(stmt):
    targets: list[expr]
    value: expr


class AugAssign(stmt):
    target: expr
    op: operator
    value: expr


class AnnAssign(stmt):
    target: expr
    annotation: expr
    value: expr | None
    simple: int


class For(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]


class AsyncFor(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]


class While(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]


class If(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]


class With(stmt):
    items: list[withitem]
    body: list[stmt]


class AsyncWith(stmt):
    items: list[withitem]
    body: list[stmt]


class Raise(stmt):
    exc: expr | None
    cause: expr | None


class Try(stmt):
    body: list[stmt]
    handlers: list[ExceptHandler]
    orelse: list[stmt]
    finalbody: list[stmt]


class Assert(stmt):
    test: expr
    msg: expr | None


class Import(stmt):
    names: list[alias]


class ImportFrom(stmt):
    module: _identifier | None
    names: list[alias]
    level: int


class Global(stmt):
    names: list[_identifier]


class Nonlocal(stmt):
    names: list[_identifier]


class Expr(stmt):
    value: expr


class Pass(stmt):
    ...


class Break(stmt):
    ...


class Continue(stmt):
    ...


class expr(AST):
    ...


class BoolOp(expr):
    op: boolop
    values: list[expr]


class BinOp(expr):
    left: expr
    op: operator
    right: expr


class UnaryOp(expr):
    op: unaryop
    operand: expr


class Lambda(expr):
    args: arguments
    body: expr


class IfExp(expr):
    test: expr
    body: expr
    orelse: expr


class Dict(expr):
    keys: list[expr | None]
    values: list[expr]


class Set(expr):
    elts: list[expr]


class ListComp(expr):
    elt: expr
    generators: list[comprehension]


class SetComp(expr):
    elt: expr
    generators: list[comprehension]


class DictComp(expr):
    key: expr
    value: expr
    generators: list[comprehension]


class GeneratorExp(expr):
    elt: expr
    generators: list[comprehension]


class Await(expr):
    value: expr


class Yield(expr):
    value: expr | None


class YieldFrom(expr):
    value: expr


class Compare(expr):
    left: expr
    ops: list[cmpop]
    comparators: list[expr]


class Call(expr):
    func: expr
    args: list[expr]
    keywords: list[keyword]


class FormattedValue(expr):
    value: expr
    conversion: int
    format_spec: expr | None


class JoinedStr(expr):
    values: list[expr]


class Constant(expr):
    value: Any  # None, str, bytes, bool, int, float, complex, Ellipsis
    kind: str | None
    # Aliases for value, for backwards compatibility
    s: Any
    n: complex


class NamedExpr(expr):
    target: expr
    value: expr


class Attribute(expr):
    value: expr
    attr: _identifier
    ctx: expr_context


class slice(AST):
    ...


class Slice(slice):
    lower: expr | None
    upper: expr | None
    step: expr | None


class ExtSlice(slice):
    dims: list[slice]


class Index(slice):
    value: expr


class Subscript(expr):
    value: expr
    slice: slice
    ctx: expr_context


class Starred(expr):
    value: expr
    ctx: expr_context


class Name(expr):
    id: _identifier
    ctx: expr_context


class List(expr):
    elts: list[expr]
    ctx: expr_context


class Tuple(expr):
    elts: list[expr]
    ctx: expr_context


class expr_context(AST):
    ...


class AugLoad(expr_context):
    ...


class AugStore(expr_context):
    ...


class Param(expr_context):
    ...


class Suite(mod):
    body: list[stmt]


class Del(expr_context):
    ...


class Load(expr_context):
    ...


class Store(expr_context):
    ...


class boolop(AST):
    ...


class And(boolop):
    ...


class Or(boolop):
    ...


class operator(AST):
    ...


class Add(operator):
    ...


class BitAnd(operator):
    ...


class BitOr(operator):
    ...


class BitXor(operator):
    ...


class Div(operator):
    ...


class FloorDiv(operator):
    ...


class LShift(operator):
    ...


class Mod(operator):
    ...


class Mult(operator):
    ...


class MatMult(operator):
    ...


class Pow(operator):
    ...


class RShift(operator):
    ...


class Sub(operator):
    ...


class unaryop(AST):
    ...


class Invert(unaryop):
    ...


class Not(unaryop):
    ...


class UAdd(unaryop):
    ...


class USub(unaryop):
    ...


class cmpop(AST):
    ...


class Eq(cmpop):
    ...


class Gt(cmpop):
    ...


class GtE(cmpop):
    ...


class In(cmpop):
    ...


class Is(cmpop):
    ...


class IsNot(cmpop):
    ...


class Lt(cmpop):
    ...


class LtE(cmpop):
    ...


class NotEq(cmpop):
    ...


class NotIn(cmpop):
    ...


class comprehension(AST):
    target: expr
    iter: expr
    ifs: list[expr]
    is_async: int


class excepthandler(AST):
    ...


class ExceptHandler(excepthandler):
    type: expr | None
    name: _identifier | None
    body: list[stmt]


class arguments(AST):
    args: list[arg]
    vararg: arg | None
    kwonlyargs: list[arg]
    kw_defaults: list[expr | None]
    kwarg: arg | None
    defaults: list[expr]
    posonlyargs: list[arg]


class arg(AST):
    arg: _identifier
    annotation: expr | None


class keyword(AST):
    arg: _identifier | None
    value: expr


class alias(AST):
    name: _identifier
    asname: _identifier | None


class withitem(AST):
    context_expr: expr
    optional_vars: expr | None

import os

from tqdm import tqdm
from tvm.script.parser import doc, doc_core

TVM_PATH = "/root/Projects/tvm-dev/python"


class LinenoChecker(doc.NodeVisitor):
    def __init__(self):
        self.no_lineno = set()
        self.no_col_offset = set()
        self.no_end_lineno = set()
        self.no_end_col_offset = set()

    def visit(self, node):
        if isinstance(node, doc.AST) and not isinstance(
            node,
            (
                doc.expr_context,
                doc.operator,
                doc.boolop,
                doc.unaryop,
                doc.cmpop,
            ),
        ):
            lineno = getattr(node, "lineno", None)
            col_offset = getattr(node, "col_offset", None)
            end_lineno = getattr(node, "end_lineno", None)
            end_col_offset = getattr(node, "end_col_offset", None)
            if lineno is None:
                self.no_lineno.add(type(node).__name__.split(".")[-1])
            if col_offset is None:
                self.no_col_offset.add(type(node).__name__.split(".")[-1])
            if end_lineno is None:
                self.no_end_lineno.add(type(node).__name__.split(".")[-1])
            if end_col_offset is None:
                self.no_end_col_offset.add(type(node).__name__.split(".")[-1])

        super().visit(node)


def main():
    all_files = []
    for root, _, files in os.walk(TVM_PATH):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    all_files.append(f.read())
    lineno_checker = LinenoChecker()
    for f in tqdm(all_files):
        program = doc.parse(f)
        lineno_checker.visit(program)
        f_back = doc.from_doc(program)
    for name in doc_core.__all__:
        a = name in lineno_checker.no_lineno
        b = name in lineno_checker.no_col_offset
        c = name in lineno_checker.no_end_lineno
        d = name in lineno_checker.no_end_col_offset
        if a or b or c or d:
            print(name, a, b, c, d)


if __name__ == "__main__":
    main()

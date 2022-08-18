"""Parser for lib.py"""
# pylint: disable=missing-docstring
import ast
from typing import Dict, List, Optional

import attrs

SRC_PATH = "./source/lib.py"
DOC_PATH = "./generated/doc.py"
VISITOR_PATH = "./generated/visitor.py"

BLOCK_LIST = [
    "AsyncFor",
    "AsyncWith",
    "AsyncFunctionDef",
    "Await",
    "type_ignore",
    "TypeIgnore",
    "FunctionType",
]


@attrs.define
class Field:  # pylint: disable=too-few-public-methods
    name: str
    type: str


@attrs.define
class ASTNode:
    name: str
    parent_cls: Optional[str]
    fields: List[Field]

    @property
    def parent(self) -> Optional["ASTNode"]:
        if self.parent_cls is None:
            return None
        return NAME2NODE[self.parent_cls]

    @property
    def _init_params(self) -> List[str]:
        result = [x.name for x in self.fields]
        if (p := self.parent) is not None:  # pylint: disable=invalid-name
            result.extend(p._init_params)  # pylint: disable=protected-access
        return result

    @property
    def _init_super_params(self) -> List[str]:
        if (p := self.parent) is not None:  # pylint: disable=invalid-name
            return p._init_params  # pylint: disable=protected-access
        return []

    @property
    def init_method(self) -> str:
        result = ""
        result += f"    def __init__(self, {', '.join(self._init_params)}):\n"
        result += f"        super().__init__({', '.join(self._init_super_params)})\n"
        for field in self.fields:
            result += f"        self.{field.name} = {field.name}\n"
        return result

    @property
    def class_header(self) -> str:
        result = ""
        result += f"class {self.name}"
        if (p := self.parent) is not None:  # pylint: disable=invalid-name
            result += f"({p.name}):\n"
        else:
            result += ":\n"
        params = [f'"{p}"' for p in self._init_params]
        result += f"    _FIELDS = [{', '.join(params)}]\n"
        return result


def _is_ellipsis_stmt(stmt: ast.stmt) -> bool:
    """Check if stmt is an ellipsis stmt"""
    return (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and stmt.value.value == ...
    )


def collect_ast_nodes(path: str) -> Dict[str, ASTNode]:
    """Collect all AST nodes"""

    results: List[ASTNode] = []
    with open(path, "r", encoding="utf-8") as i_f:
        source = i_f.read()
    program: List[ast.stmt] = ast.parse(source).body
    source_lines: List[str] = source.splitlines()
    for node in program:
        if not isinstance(node, ast.ClassDef):
            raise ValueError("Not a class definition: " + str(ast.dump(node)))
        if node.name in BLOCK_LIST:
            continue
        assert len(node.bases) <= 1
        fields: List[Field] = []
        for stmt in node.body:
            if _is_ellipsis_stmt(stmt):
                continue
            if not isinstance(stmt, ast.AnnAssign):
                raise ValueError("Not an annotation: " + str(ast.dump(stmt)))
            if not isinstance(stmt.target, ast.Name):
                raise ValueError("Not a name: " + str(ast.dump(stmt.target)))
            annotation = source_lines[stmt.lineno - 1][
                stmt.annotation.col_offset : stmt.annotation.end_col_offset
            ].strip()
            assert stmt.target.id != "type_comment"
            fields.append(Field(stmt.target.id, annotation))
        parent = None
        if node.bases:
            assert len(node.bases) == 1
            assert isinstance(node.bases[0], ast.Name)
            parent = node.bases[0].id
        results.append(
            ASTNode(
                name=node.name,
                parent_cls=parent,
                fields=fields,
            )
        )
    return {x.name: x for x in results}


NAME2NODE: Dict[str, "ASTNode"] = collect_ast_nodes(SRC_PATH)


def generate_class_defs(path: str) -> None:
    code = ""
    code += "# pylint: disable=redefined-outer-name,missing-docstring,invalid-name\n"
    code += "# pylint: disable=useless-super-delegation,redefined-builtin\n"
    code += "# pylint: disable=too-few-public-methods,too-many-arguments\n"
    all_nodes = []
    for v in NAME2NODE.values():  # pylint: disable=invalid-name
        code += v.class_header + "\n"
        code += v.init_method + "\n"
        all_nodes.append(f'"{v.name}"')
    code += "__all__ = [" + ", ".join(all_nodes) + "]\n"
    with open(path, "w", encoding="utf-8") as o_f:
        o_f.write(code)


# class NodeVisitor:
#     def visit(self, node: ast.AST) -> Any:


def main():
    """Main generator"""
    for node in NAME2NODE.values():
        print(node)
    generate_class_defs(DOC_PATH)


if __name__ == "__main__":
    main()

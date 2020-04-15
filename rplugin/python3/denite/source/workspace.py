# ============================================================================
# FILE: workspace.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import re
from denite.kind.file import Kind as FileKind
from denite.source.base import Base
from os.path import relpath

symbolKinds = [
    "File",
    "Module",
    "Namespace",
    "Package",
    "Class",
    "Method",
    "Property",
    "Field",
    "Constructor",
    "Enum",
    "Interface",
    "Function",
    "Variable",
    "Constant",
    "String",
    "Number",
    "Boolean",
    "Array",
    "Object",
    "Key",
    "Null",
    "EnumMember",
    "Struct",
    "Event",
    "Operator",
    "TypeParameter",
]
symbol_kind_map = {i + 1: v for i, v in enumerate(symbolKinds)}


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = "coc-workspace"
        self.kind = FileKind(vim)

    def define_syntax(self):
        self.vim.command("syntax case ignore")
        self.vim.command(
            r"syntax match deniteSource_WorkspaceHeader /\v^.*$/ containedin="
            + self.syntax_name
        )
        self.vim.command(
            r"syntax match deniteSource_WorkspaceName /\v^\s*\S+/ contained "
            r"containedin=deniteSource_WorkspaceHeader"
        )
        self.vim.command(
            r"syntax match deniteSource_WorkspaceKind /\[\w\+\]/ contained "
            r"containedin=deniteSource_WorkspaceHeader"
        )
        self.vim.command(
            r"syntax match deniteSource_WorkspaceFile /\f\+$/ contained "
            r"containedin=deniteSource_WorkspaceHeader"
        )

    def highlight(self):
        self.vim.command("highlight default link deniteSource_WorkspaceName Normal")
        self.vim.command("highlight default link deniteSource_WorkspaceKind Typedef")
        self.vim.command("highlight default link deniteSource_WorkspaceFile Comment")
    def on_init(self,context):
        context['is_interactive'] = True

    def gather_candidates(self, context):
        items = self.vim.call("CocAction", "getWorkspaceSymbols", context["input"],context['bufnr'])
        if not items:
            return []
        candidates = []
        for item in items:
            name = item["name"]
            kind = symbol_kind_map.get(item["kind"],"Unknown")
            file_path = item["location"]["uri"]
            lnum = item["location"]["range"]["start"]["line"]+1
            col = item["location"]["range"]["start"]["character"]
            candidates.append(
                {
                    "word": name,
                    "abbr": "%s [%s] %s" % (name, kind, file_path.replace("file://","")),
                    "action__path": file_path,
                    "action__col": col,
                    "action__line": lnum,
                }
            )
        return candidates

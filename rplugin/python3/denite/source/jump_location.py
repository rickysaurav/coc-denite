# pylint: disable=E0401,C0111
from os.path import relpath
from denite.kind.file import Kind as FileKind
from denite.source.base import Base

class Source(Base):

    def __init__(self, vim):
        super(Source, self).__init__(vim)

        self.name = 'coc-jump-locations'
        self.matchers = ['matcher_fuzzy']
        self.sorters = []
        self.kind = FileKind(vim)

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteSource_JumplocationHeader /\v^.*$/ containedin='
                         + self.syntax_name)
        self.vim.command(r'syntax match deniteSource_JumplocationFile /\v^\s*\S+/ contained '
                         r'containedin=deniteSource_JumplocationHeader')

    def highlight(self):
        self.vim.command('highlight default link deniteSource_JumplocationFile Comment')

    def gather_candidates(self, _):
        cwd = self.vim.call('getcwd')
        items = self.vim.vars.get('coc_jump_locations')
        if items is None:
            return []
        candidates = []
        for item in items:
            filepath = relpath(item['filename'], start=cwd)
            candidates.append({
                'word': filepath,
                'abbr': '%s:%s:%s %s' % (filepath, item['lnum'], item['col'], item['text']),
                'action__path': item['filename'],
                'action__col': item['col'],
                'action__line': item['lnum'],
                })

        return candidates

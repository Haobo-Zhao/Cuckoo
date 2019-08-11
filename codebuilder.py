class CodeBuilder:
    """Helper class for building source code"""

    def __init__(self, indent=0):
        self.code = []
        self.init_indent = indent
        self.indent_level = self.init_indent

    def __str__(self):
        return ''.join(str(line) for line in self.code)

    def add_line(self, line):
        self.code.extend(['' * self.indent_level, line, '\n'])

    def add_section(self):
        """Will append a new line when done"""
        s = CodeBuilder(self.indent_level)
        self.code.append(s)
        return s

    # I respect PEP-8
    INDENT_STEP = 4

    def indent(self):
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        self.indent_level -= self.INDENT_STEP

    def get_globals(self):
        assert self.indent_level == self.init_indent
        source = str(self)
        result = {}
        exec(source, result)
        return result

import re

import codebuilder


class Template(object):
    """Mimicking some of Django syntax.
    contexts are dicts
    """
    def __init__(self, template, *contexts):
        self.context = {}
        for c in contexts:
            self.context.update(c)

        # (self.all_vars - self.loop_vars) means the vars needed to get from self.context
        self.all_vars = set()
        self.loop_vars = set()

        code = codebuilder.CodeBuilder()
        code.add_line('def _render(context, dot_handler):')
        code.indent()
        # this section will be completed when all vars are known in the template
        vars = code.add_section()
        code.add_line('result = []')
        code.add_line('append_result = result.append')
        code.add_line('extend_result = result.extend')
        code.add_line('to_str = str')

        buffered = []

        def flush_output():
            """Batching lines of code"""
            if len(buffered) == 1:
                code.add_line("append_result(%s)" % buffered[0])
            elif len(buffered) > 1:
                code.add_line("extend_result([%s])" % ", ".join(buffered))
            del buffered[:]

        # split the template into literals,
        # {{ expression }}, {# comment #} and {% `if` or `for` statement %}
        tokens = re.split(r'(?s)({{.*?}}|{%.*?%}|{#.*?#})', template)

        for token in tokens:
            if token.startswith('{#'):
                # Simply move on when encountering comments
                continue
            else:
                # Non-empty literal are directly added.
                if token:
                    # Preserve single quotes and double quotes in the template
                    buffered.append(repr(token))

        flush_output()

        # Complete the variables section now that all vars are known
        for var_name in (self.all_vars - self.loop_vars):
            vars.add_line("c_{0} = context[{1}]".format(var_name, var_name))

        code.add_line("return ''.join(result)")
        code.dedent()
        self.__render__ = code.get_globals()['_render']

    def render(self, context=None):
        """Render the template with the provided context"""
        c = dict(self.context)
        if context:
            c.update(context)
        return self.__render__(c, self.dot_handler)

    def dot_handler(self, value, *dots):
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value

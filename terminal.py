from context import TerminalContext


class Terminal(object):

    def __init__(self, manager, contexts, name, index, pos, start_callback=None, restart_callback=None, stop_callback=None):
        self.manager = manager
        self.contexts = contexts
        self.name = name
        self.index = index
        self.pos = pos
        self.status = 0
        self.start_callback = start_callback
        self.restart_callback = restart_callback
        self.stop_callback = stop_callback

        self.terminal_contexts = []

        for context_name in self.contexts:
            self._setup(context_name, self.contexts[context_name])

        self.output = []

    def _setup(self, context_name, context):
        if context_name == "main":
            self.terminal_contexts.append(TerminalContext(context, self.pos, "Expand", self._expand_terminal, text=self.name))
        else:
            self.terminal_contexts.append(TerminalContext(context, None, "Shrink", self._shrink_terminal, text=self.name))

    def reconfigure(self):
        pass

    def update(self):
        pass

    def _expand_terminal(self):
        self.manager.focus_terminal(self)

    def _shrink_terminal(self):
        self.manager.focus_all()

    # TODO Update Frame
    def set_name(self, name):
        self.name = name

    def set_pos(self, pos):
        self.pos = pos

    def set_start_callback(self, start_callback):
        self.start_callback = start_callback
        for terminal_context in self.terminal_contexts:
            terminal_context.set_start_callback(start_callback)

    def set_restart_callback(self, restart_callback):
        self.restart_callback = restart_callback
        for terminal_context in self.terminal_contexts:
            terminal_context.set_restart_callback(restart_callback)

    def set_stop_callback(self, stop_callback):
        self.stop_callback = stop_callback
        for terminal_context in self.terminal_contexts:
            terminal_context.set_stop_callback(stop_callback)

    def update_status(self, status):
        self.status = status
        for terminal_context in self.terminal_contexts:
            terminal_context.update_status(status)

    def append(self, msg, end='\n'):
        self.output.append(msg)
        for terminal_context in self.terminal_contexts:
            terminal_context.append(msg, end)

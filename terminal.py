from context import TerminalContext
from util import Dict


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

        self.terminal_contexts = Dict()

        for context_name in self.contexts:
            self.add_context(context_name, self.contexts[context_name])

        self.output = []

    def add_context(self, context_name, context):
        if context_name == "main":
            self.terminal_contexts[context_name] = TerminalContext(context, self.pos, "Expand", self._expand_terminal, "Eject", self._eject_terminal, text=self.name)
        elif context_name == "popout":
            self.terminal_contexts[context_name] = TerminalContext(context, None, None, None, None, None, text=self.name)
            terminal_context = self.terminal_contexts[context_name]

            for msg in self.output:
                terminal_context.append(*msg)
        else:
            self.terminal_contexts[context_name] = TerminalContext(context, None, "Shrink", self._shrink_terminal, "Eject", self._eject_terminal, text=self.name)

    def remove_context(self, context_name):
        if context_name == "popout":
            if context_name in self.terminal_contexts:
                del self.terminal_contexts[context_name]

    def update(self):
        pass

    def _expand_terminal(self):
        self.manager.focus_terminal(self)

    def _shrink_terminal(self):
        self.manager.focus_all()

    def _eject_terminal(self):
        self.manager.eject_terminal(self)

    # TODO Update Frame
    def set_name(self, name):
        self.name = name

    def set_pos(self, pos):
        self.pos = pos

    def set_start_callback(self, start_callback):
        self.start_callback = start_callback
        for terminal_context_name in self.terminal_contexts:
            terminal_context = self.terminal_contexts[terminal_context_name]
            terminal_context.set_start_callback(start_callback)

    def set_restart_callback(self, restart_callback):
        self.restart_callback = restart_callback
        for terminal_context_name in self.terminal_contexts:
            terminal_context = self.terminal_contexts[terminal_context_name]
            terminal_context.set_restart_callback(restart_callback)

    def set_stop_callback(self, stop_callback):
        self.stop_callback = stop_callback
        for terminal_context_name in self.terminal_contexts:
            terminal_context = self.terminal_contexts[terminal_context_name]
            terminal_context.set_stop_callback(stop_callback)

    def update_status(self, status):
        self.status = status
        for terminal_context_name in self.terminal_contexts:
            terminal_context = self.terminal_contexts[terminal_context_name]
            terminal_context.update_status(status)

    def append(self, msg, end='\n'):
        self.output.append((msg, end))
        for terminal_context_name in self.terminal_contexts:
            terminal_context = self.terminal_contexts[terminal_context_name]
            terminal_context.append(msg, end)

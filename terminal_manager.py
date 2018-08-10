import math
from queue import Queue

import log
from context import PageContext
from terminal import Terminal
from util import Dict


class TerminalManager(object):

    def __init__(self, window):
        self.window = window
        self.terminals = Dict()
        self.expanded_term = None
        self.current_context = None
        self.contexts = Dict()
        self.queue = Queue()

    def setup(self):
        self.contexts["main"] = PageContext(self.window.get_root_context())
        self.current_context = self.contexts["main"]

    def show(self):
        self.current_context.show()

    def hide(self):
        self.current_context.hide()

    def update(self):
        for tm_name in self.terminals.keys():
            self.terminals[tm_name].update()

        while not self.queue.empty():
            func, data = self.queue.get()

            if func == "add_terminal":
                name = data
                index = len(self.terminals)
                self.contexts[index] = PageContext(self.window.get_root_context())
                cntxs = Dict(main=self.contexts["main"])
                cntxs[index] = self.contexts[index]
                self.terminals[index] = Terminal(self, cntxs, name, index, TerminalManager.get_rc_index(index))
                self.contexts["main"].configure_page()
            elif func == "set_terminal_attribute":
                name, attrib, value = data
                term = self.get_terminal(name)

                if attrib == "start_callback":
                    term.set_start_callback(value)
                elif attrib == "restart_callback":
                    term.set_restart_callback(value)
                elif attrib == "stop_callback":
                    term.set_stop_callback(value)
                elif attrib == "status":
                    term.update_status(value)
                else:
                    log.error("Invalid Attribute Passed: " + attrib)
            elif func == "append_to_terminal":
                name, data, end = data
                term = self.get_terminal(name)
                term.append(data, end)

    def add_terminal(self, name):
        self.queue.put(("add_terminal", name))

    def focus_terminal(self, terminal):
        self.current_context.hide()
        self.current_context = self.contexts[terminal.index]
        self.current_context.show()

    def focus_all(self):
        self.current_context.hide()
        self.current_context = self.contexts["main"]
        self.current_context.show()

    def set_terminal_attribute(self, name, attrib, value):
        self.queue.put(("set_terminal_attribute", (name, attrib, value)))

    def append_to_terminal(self, name, data, end='\n'):
        self.queue.put(("append_to_terminal", (name, data, end)))

    def get_terminal(self, name):
        for terminal_key in self.terminals.keys():
            terminal = self.terminals[terminal_key]
            if terminal.name == name:
                return terminal

    @staticmethod
    def get_rc_index(index):
        edge = int(math.sqrt(index))
        left = int(index - (edge ** 2))

        if left == edge:
            # Start new row
            row = left
            col = 0
        elif left < edge:
            # on right side
            row = left
            col = edge
        else:
            # on bottom
            row = edge
            col = left - edge

        return row, col

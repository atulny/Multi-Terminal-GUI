from rendering.tkinter.context import RootContext
from pthread import PThread
from terminal_manager import TerminalManager
import time


class Window(object):

    def __init__(self, title="title", dim=(800, 600), theme=0):
        self.title = title
        self.dim = dim
        self.theme = theme
        self.root_context = None
        self.terminal_manager = TerminalManager(self)

        self.is_running = True

        self._setup()

    def _setup(self):
        self.root_context = RootContext(self, self.title, self.dim, self.theme)
        self.root_context.setup()
        self.terminal_manager.setup()

    def start(self, run_callback, run_callback_args):
        thread = PThread(call_back=run_callback, call_back_args=run_callback_args)
        thread.start()

        self.terminal_manager.show()
        self._run()

    def stop(self):
        self.is_running = False

    def _run(self):
        while self.is_running:
            self.root_context.update()
            self.terminal_manager.update()
            time.sleep(1/60)

    def get_terminal_manger(self):
        return self.terminal_manager

    def get_root_context(self):
        return self.root_context

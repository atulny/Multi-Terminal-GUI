from display import Display
from pthread import PThread
from terminal_manager import TerminalManager


class Window(object):

    def __init__(self, title="title", dim=(800, 600), theme=0):
        self.title = title
        self.dim = dim
        self.theme = theme
        self.display = None
        self.terminal_manager = TerminalManager(self)

        self.is_running = True

        self._setup()

    def _setup(self):
        self.display = Display(self, self.title, self.dim, self.theme)
        self.display.setup()
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
            self.display.update()
            self.terminal_manager.update()

    def get_terminal_manger(self):
        return self.terminal_manager

    def get_root_context(self):
        return self.display

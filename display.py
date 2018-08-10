from ttkthemes import ThemedTk


class Display(ThemedTk):
    themes = [
        "default",
        "classic",
        "clam",
        "winnactive",
        "vista",
        "xpnative",
        "alt",
        "arc",
        "blue",
        "clearlooks",
        "elegance",
        "kroc",
        "plastik",
        "radiance",
        "winxpblue"
    ]

    def __init__(self, window, window_title, dim, theme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_title = window_title
        self.dim = dim
        self.window = window
        self.theme = theme

    def setup(self):
        self.set_theme(Display.themes[self.theme])

        self.title(self.window_title)
        self.geometry("%dx%d" % self.dim)
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        self.protocol("WM_DELETE_WINDOW", self.stop)

    def update(self):
        super().update()
        super().update_idletasks()

    def stop(self):
        self.window.stop()
        # self.destroy()

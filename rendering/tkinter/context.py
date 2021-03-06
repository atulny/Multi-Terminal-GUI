import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class RootContext(ThemedTk):
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
        self.set_theme(RootContext.themes[self.theme])

        self.title(self.window_title)
        self.geometry("%dx%d" % self.dim)
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        self.protocol("WM_DELETE_WINDOW", self.stop)
        self.center()

    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def update(self):
        super().update()
        super().update_idletasks()

    def stop(self):
        self.window.stop()
        # self.destroy()


class Context(ttk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root


class LabeledContext(ttk.LabelFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root


class PopOutContext(tk.Toplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PageContext(Context):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root

    def show(self):
        self.pack(side="top", fill="both", expand=True)

    def hide(self):
        self.pack_forget()

    def configure_page(self):
        cols, rows = self.grid_size()

        for i in range(rows):
            self.grid_rowconfigure(i, weight=1, minsize=self.winfo_height() / rows)
        for j in range(cols):
            self.grid_columnconfigure(j, weight=1, minsize=self.winfo_width() / cols)


class TerminalContext(LabeledContext):
    def __init__(self, root, pos, resize_func_name, resize_func, pop_out_func_name, pop_out_func, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.pos = pos
        self.resize_func_name = resize_func_name
        self.resize_func = resize_func
        self.pop_out_func_name = pop_out_func_name
        self.pop_out_func = pop_out_func

        self.start_callback = None
        self.restart_callback = None
        self.stop_callback = None

        self.is_started = False

        self.expand_image = tk.PhotoImage(file="res/expand_16.png")
        self.shrink_image = tk.PhotoImage(file="res/shrink_16.png")
        self.eject_image = tk.PhotoImage(file="res/eject_16.png")

        self._setup_terminal()

    def _setup_terminal(self):
        self.top_bar = Context(self, relief=tk.SUNKEN)
        self.status_indicator = tk.Message(self.top_bar, relief=tk.GROOVE, bg="red")
        self.start_button = ttk.Button(self.top_bar, text="Start")
        self.stop_button = ttk.Button(self.top_bar, text="Stop")
        self.text_box = tk.Text(self, borderwidth=3, relief=tk.SUNKEN, undo=True, wrap='word', state=tk.DISABLED)
        self.scroll_bar = ttk.Scrollbar(self, command=self.text_box.yview)
        self.text_box['yscrollcommand'] = self.scroll_bar.set

        if self.resize_func_name and self.resize_func:
            self.expand = ttk.Button(self.text_box, text=self.resize_func_name, command=self.resize_func)

        if self.pop_out_func_name and self.pop_out_func:
            self.eject = ttk.Button(self.text_box, text=self.pop_out_func_name, command=self.pop_out_func)

        self.configure_terminal()

    def configure_terminal(self):
        if self.pos:  # Put in grid
            row, col = self.pos
            self.grid(row=row, column=col, sticky="nsew")
            resize_image = self.expand_image
        else:  # Put in solo-view
            self.pack(side="top", fill="both", expand=True)
            resize_image = self.shrink_image

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Top Bar

        padx = 2
        pady = 2

        self.top_bar.grid(row=0, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=padx, pady=pady)

        self.top_bar.grid_rowconfigure(0, weight=1, minsize=32)
        self.top_bar.grid_columnconfigure(0, weight=1, minsize=32)
        self.top_bar.grid_columnconfigure(1, weight=5)
        self.top_bar.grid_columnconfigure(2, weight=5)

        self.status_indicator.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=padx, pady=pady)
        self.start_button.grid(row=0, column=1, columnspan=1, sticky="nsew", padx=padx, pady=pady)
        self.stop_button.grid(row=0, column=2, columnspan=1, sticky="nsew", padx=padx, pady=pady)

        # Text Box

        self.text_box.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew")

        # Scroll Bar

        self.scroll_bar.grid(row=1, rowspan=1, column=2, sticky="nsew")

        # Expand Button

        if self.resize_func_name and self.resize_func:
            self.expand.config(image=resize_image)
            self.expand.place(relx=1.0, rely=1.0, x=-padx, y=-pady, anchor="se")
            self.expand.update()
            width = self.expand.winfo_width() + padx
        else:
            width = padx

        # Eject Button
        if self.pop_out_func_name and self.pop_out_func:
            self.eject.config(image=self.eject_image)
            self.eject.place(relx=1.0, rely=1.0, x=-(width + padx), y=-pady, anchor="se")

    def set_start_callback(self, start_callback):
        self.start_callback = start_callback
        if not self.is_started:
            self.start_button.config(command=start_callback)

    def set_restart_callback(self, restart_callback):
        self.restart_callback = restart_callback
        if self.is_started:
            self.start_button.config(command=restart_callback)

    def set_stop_callback(self, stop_callback):
        self.stop_callback = stop_callback
        self.stop_button.config(command=stop_callback)

    def update_status(self, status):
        if status == 0:  # Inactive
            self.status_indicator.config(bg="red")
            self.start_button.config(text="Start")
            self.start_button.config(command=self.start_callback)
            self.is_started = False
        elif status == 1:  # Active
            self.status_indicator.config(bg="green")
            self.start_button.config(text="Restart")
            self.start_button.config(command=self.restart_callback)
            self.is_started = True
        elif status == 2:  # Standby
            self.status_indicator.config(bg="yellow")
            self.start_button.config(text="Restart")
            self.start_button.config(command=self.restart_callback)
            self.is_started = True
        else:  # Unknown
            self.status_indicator.config(bg="gray")
            self.start_button.config(text="Restart")
            self.start_button.config(command=self.restart_callback)
            self.is_started = True

    def append(self, msg, end='\n'):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, msg + end)
        self.text_box.config(state=tk.DISABLED)

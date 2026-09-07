"""
ui.py
-----
Everything tkinter-related lives here. This file doesn't know *how*
passwords are generated or analyzed — it just calls generator.py and
analyzer.py and displays the results. That separation means you could
swap this whole file for a web interface later without touching the
actual password logic.
"""

import tkinter as tk
from tkinter import ttk

from generator import generate_password
from analyzer import analyze_password

COLORS = {
    "bg": "#1c1c1e",
    "surface": "#262628",
    "border": "#3a3a3c",
    "text": "#e8e8ea",
    "text_muted": "#9a9a9d",
    "accent": "#5b8def",
}

RATING_COLORS = {
    "Weak": "#e0645f",
    "Fair": "#d9a441",
    "Good": "#6fae6f",
    "Strong": "#5b8def",
}

FONT_FAMILY = "Helvetica"


class LockboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lockbox")
        self.root.configure(bg=COLORS["bg"])
        self.root.geometry("460x620")
        self.root.minsize(420, 560)

        self._configure_ttk_style()
        self._build_header()
        self._build_tabs()

    # -- Setup ------------------------------------------------------

    def _configure_ttk_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=COLORS["surface"],
            foreground=COLORS["text_muted"],
            padding=(16, 8),
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["bg"])],
            foreground=[("selected", COLORS["text"])],
        )

        style.configure("TFrame", background=COLORS["bg"])
        style.configure(
            "Horizontal.TScale",
            background=COLORS["bg"],
            troughcolor=COLORS["surface"],
        )
        style.configure(
            "TCheckbutton",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            focuscolor=COLORS["bg"],
        )
        style.map("TCheckbutton", background=[("active", COLORS["bg"])])

    def _build_header(self):
        header = tk.Frame(self.root, bg=COLORS["bg"])
        header.pack(fill="x", padx=24, pady=(24, 8))

        tk.Label(
            header,
            text="LOCKBOX",
            font=(FONT_FAMILY, 20, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Create stronger passwords. Understand your security.",
            font=(FONT_FAMILY, 10),
            bg=COLORS["bg"],
            fg=COLORS["text_muted"],
        ).pack(anchor="w", pady=(2, 0))

    def _build_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=16, pady=16)

        generator_tab = tk.Frame(notebook, bg=COLORS["bg"])
        analyzer_tab = tk.Frame(notebook, bg=COLORS["bg"])

        notebook.add(generator_tab, text="Generator")
        notebook.add(analyzer_tab, text="Analyzer")

        self._build_generator_tab(generator_tab)
        self._build_analyzer_tab(analyzer_tab)

    # -- Generator tab ------------------------------------------------

    def _build_generator_tab(self, parent):

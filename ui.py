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

# --- Color palette -----------------------------------------------------
# One dark background, one accent color, done. Resist the urge to add
# more colors — a security tool should feel calm, not busy.
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
        """ttk widgets (Notebook, Scale, Checkbutton) don't take plain
        tkinter color options — they need a 'Style' configured instead.
        The 'clam' theme is the one that actually respects custom colors
        on most platforms."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TNotebook", background=COLORS["bg"], borderwidth=0
        )
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

        style.configure(
            "TFrame", background=COLORS["bg"]
        )
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
        style.map(
            "TCheckbutton",
            background=[("active", COLORS["bg"])],
        )

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
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.password_var = tk.StringVar()
        self.gen_status_var = tk.StringVar()

        content = tk.Frame(parent, bg=COLORS["bg"])
        content.pack(fill="both", expand=True, padx=8, pady=8)

        # Length slider
        length_row = tk.Frame(content, bg=COLORS["bg"])
        length_row.pack(fill="x", pady=(0, 4))

        tk.Label(
            length_row, text="Length", font=(FONT_FAMILY, 11),
            bg=COLORS["bg"], fg=COLORS["text"],
        ).pack(side="left")

        self.length_display = tk.Label(
            length_row, textvariable=self.length_var, font=(FONT_FAMILY, 11, "bold"),
            bg=COLORS["bg"], fg=COLORS["accent"],
        )
        self.length_display.pack(side="right")

        ttk.Scale(
            content, from_=4, to=64, orient="horizontal",
            variable=self.length_var,
            command=lambda _: self.length_var.set(int(float(self.length_var.get()))),
        ).pack(fill="x", pady=(0, 16))

        # Character type checkboxes
        options_frame = tk.Frame(content, bg=COLORS["bg"])
        options_frame.pack(fill="x", pady=(0, 16))

        options = [
            ("Uppercase (A-Z)", self.upper_var),
            ("Lowercase (a-z)", self.lower_var),
            ("Numbers (0-9)", self.digits_var),
            ("Symbols (!@#$...)", self.symbols_var),
        ]
        for label, var in options:
            ttk.Checkbutton(options_frame, text=label, variable=var).pack(
                anchor="w", pady=2
            )

        # Generate button
        tk.Button(
            content,
            text="Generate Password",
            command=self.on_generate,
            bg=COLORS["accent"],
            fg="#ffffff",
            activebackground="#4a7bd4",
            activeforeground="#ffffff",
            relief="flat",
            font=(FONT_FAMILY, 11, "bold"),
            padx=12, pady=10,
            cursor="hand2",
        ).pack(fill="x", pady=(0, 16))

        # Result display
        result_box = tk.Frame(
            content, bg=COLORS["surface"], highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        result_box.pack(fill="x", pady=(0, 8))

        self.password_entry = tk.Entry(
            result_box,
            textvariable=self.password_var,
            font=(FONT_FAMILY, 13),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            state="readonly",
            readonlybackground=COLORS["surface"],
            justify="center",
        )
        self.password_entry.pack(fill="x", padx=12, pady=14)

        # Copy button + status message
        action_row = tk.Frame(content, bg=COLORS["bg"])
        action_row.pack(fill="x")

        tk.Button(
            action_row,
            text="Copy to Clipboard",
            command=self.on_copy,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            activebackground=COLORS["border"],
            activeforeground=COLORS["text"],
            relief="flat",
            font=(FONT_FAMILY, 10),
            padx=10, pady=6,
            cursor="hand2",
        ).pack(side="left")

        tk.Label(
            action_row,
            textvariable=self.gen_status_var,
            font=(FONT_FAMILY, 10),
            bg=COLORS["bg"],
            fg=COLORS["accent"],
        ).pack(side="left", padx=(12, 0))

    def on_generate(self):
        try:
            password = generate_password(
                self.length_var.get(),
                self.upper_var.get(),
                self.lower_var.get(),
                self.digits_var.get(),
                self.symbols_var.get(),
            )
            self.password_entry.config(state="normal")
            self.password_var.set(password)
            self.password_entry.config(state="readonly")
            self.gen_status_var.set("")
        except ValueError as error:
            self.password_entry.config(state="normal")
            self.password_var.set("")
            self.password_entry.config(state="readonly")
            self.gen_status_var.set(str(error))

    def on_copy(self):
        password = self.password_var.get()
        if not password:
            self.gen_status_var.set("Generate a password first.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()  # required on some platforms for clipboard to update immediately

        self.gen_status_var.set("Copied!")
        # Clear the "Copied!" message after 2 seconds so it doesn't
        # sit there forever.
        self.root.after(2000, lambda: self.gen_status_var.set(""))

    # -- Analyzer tab ---------------------------------------------------

    def _build_analyzer_tab(self, parent):
        self.analyze_input_var = tk.StringVar()
        self.rating_var = tk.StringVar(value="")
        self.analyze_status_var = tk.StringVar()
        self.show_password = False

        content = tk.Frame(parent, bg=COLORS["bg"])
        content.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(
            content, text="Enter a password to check",
            font=(FONT_FAMILY, 11), bg=COLORS["bg"], fg=COLORS["text"],
        ).pack(anchor="w", pady=(0, 6))

        input_row = tk.Frame(
            content, bg=COLORS["surface"], highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        input_row.pack(fill="x", pady=(0, 12))

        self.password_input_entry = tk.Entry(
            input_row,
            textvariable=self.analyze_input_var,
            font=(FONT_FAMILY, 12),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            show="*",
        )
        self.password_input_entry.pack(side="left", fill="x", expand=True, padx=(12, 4), pady=10)

        self.toggle_btn = tk.Button(
            input_row,
            text="Show",
            command=self.on_toggle_visibility,
            bg=COLORS["surface"],
            fg=COLORS["accent"],
            activebackground=COLORS["surface"],
            relief="flat",
            font=(FONT_FAMILY, 9),
            cursor="hand2",
        )
        self.toggle_btn.pack(side="right", padx=(0, 8))

        tk.Button(
            content,
            text="Analyze Password",
            command=self.on_analyze,
            bg=COLORS["accent"],
            fg="#ffffff",
            activebackground="#4a7bd4",
            activeforeground="#ffffff",
            relief="flat",
            font=(FONT_FAMILY, 11, "bold"),
            padx=12, pady=10,
            cursor="hand2",
        ).pack(fill="x", pady=(0, 16))

        # Rating
        self.rating_label = tk.Label(
            content,
            textvariable=self.rating_var,
            font=(FONT_FAMILY, 16, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["text_muted"],
        )
        self.rating_label.pack(anchor="w")

        # Feedback list
        feedback_box = tk.Frame(
            content, bg=COLORS["surface"], highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        feedback_box.pack(fill="both", expand=True, pady=(8, 4))

        self.feedback_text = tk.Text(
            feedback_box,
            font=(FONT_FAMILY, 10),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            relief="flat",
            wrap="word",
            state="disabled",
            padx=12, pady=10,
            height=8,
        )
        self.feedback_text.pack(fill="both", expand=True)

        tk.Label(
            content,
            textvariable=self.analyze_status_var,
            font=(FONT_FAMILY, 9),
            bg=COLORS["bg"],
            fg=COLORS["text_muted"],
        ).pack(anchor="w", pady=(4, 0))

    def on_toggle_visibility(self):
        self.show_password = not self.show_password
        self.password_input_entry.config(show="" if self.show_password else "*")
        self.toggle_btn.config(text="Hide" if self.show_password else "Show")

    def on_analyze(self):
        password = self.analyze_input_var.get()
        try:
            rating, feedback = analyze_password(password)
        except ValueError as error:
            self.analyze_status_var.set(str(error))
            self.rating_var.set("")
            self._set_feedback_text([])
            return

        self.analyze_status_var.set("")
        self.rating_var.set(rating)
        self.rating_label.config(fg=RATING_COLORS.get(rating, COLORS["text"]))
        self._set_feedback_text(feedback)

    def _set_feedback_text(self, feedback_lines):
        self.feedback_text.config(state="normal")
        self.feedback_text.delete("1.0", tk.END)
        for line in feedback_lines:
            self.feedback_text.insert(tk.END, f"•  {line}\n")
        self.feedback_text.config(state="disabled")

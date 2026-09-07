"""
main.py
-------
The entry point. Run this file to launch Lockbox.

This file deliberately does almost nothing — it creates a tkinter
window and hands control to LockboxApp (in ui.py). Keeping main.py
tiny makes it obvious where the program actually starts.
"""

import tkinter as tk
from ui import LockboxApp


def main():
    root = tk.Tk()
    app = LockboxApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

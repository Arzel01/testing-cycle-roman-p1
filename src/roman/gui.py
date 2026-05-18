import tkinter as tk
from tkinter import ttk

from .converter import to_roman, from_roman, RomanError


class RomanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roman Numeral Converter")
        self.root.geometry("420x260")
        self._building = False

        container = ttk.Frame(root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Integer (1-3999)").grid(row=0, column=0, sticky="w")
        self.int_var = tk.StringVar()
        self.int_entry = ttk.Entry(container, textvariable=self.int_var, width=24)
        self.int_entry.grid(row=1, column=0, sticky="we", pady=(0, 12))

        ttk.Label(container, text="Roman").grid(row=2, column=0, sticky="w")
        self.roman_var = tk.StringVar()
        self.roman_entry = ttk.Entry(container, textvariable=self.roman_var, width=24)
        self.roman_entry.grid(row=3, column=0, sticky="we", pady=(0, 12))

        self.status_var = tk.StringVar(value="Type a number or a roman numeral.")
        self.status = ttk.Label(container, textvariable=self.status_var, foreground="#555")
        self.status.grid(row=4, column=0, sticky="w")

        container.columnconfigure(0, weight=1)

        self.int_var.trace_add("write", self._on_int_change)
        self.roman_var.trace_add("write", self._on_roman_change)

    def _on_int_change(self, *_args):
        if self._building:
            return
        raw = self.int_var.get().strip()
        if raw == "":
            self._set_roman("")
            self._info("Type a number or a roman numeral.")
            return
        try:
            value = int(raw)
        except ValueError:
            self._set_roman("")
            self._error("Not an integer.")
            return
        try:
            self._set_roman(to_roman(value))
            self._info("Converted " + str(value) + " to roman.")
        except RomanError as exc:
            self._set_roman("")
            self._error(str(exc))

    def _on_roman_change(self, *_args):
        if self._building:
            return
        raw = self.roman_var.get().strip()
        if raw == "":
            self._set_int("")
            self._info("Type a number or a roman numeral.")
            return
        try:
            value = from_roman(raw)
            self._set_int(str(value))
            self._info("Parsed " + raw.upper() + " as integer.")
        except RomanError as exc:
            self._set_int("")
            self._error(str(exc))

    def _set_roman(self, text):
        self._building = True
        self.roman_var.set(text)
        self._building = False

    def _set_int(self, text):
        self._building = True
        self.int_var.set(text)
        self._building = False

    def _info(self, message):
        self.status.configure(foreground="#555")
        self.status_var.set(message)

    def _error(self, message):
        self.status.configure(foreground="#b00020")
        self.status_var.set(message)


def main():
    root = tk.Tk()
    RomanApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

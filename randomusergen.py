import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

phonemes = {
    "en": {
        "starts": ["bl", "br", "cr", "d", "dr", "f", "fl", "g", "gr", "h", "k", "l", "m", "n", "pr", "r", "s", "sh", "st", "t", "tr", "w"],
        "vowels": ["a", "e", "i", "o", "u", "oo", "ee", "ai", "ou"],
        "ends": ["", "n", "r", "t", "s", "ck", "nd"]
    },
    "nl": {
        "starts": ["b", "bl", "br", "d", "dr", "g", "gr", "k", "kl", "kn", "kr", "m", "n", "p", "pr", "r", "s", "sl", "sn", "sp", "st", "v", "z"],
        "vowels": ["a", "e", "i", "o", "u", "ie", "oe", "eu", "ui", "ij", "ou"],
        "ends": ["", "r", "l", "n", "t", "s", "m", "ng", "st"]
    },
    "de": {
        "starts": ["b", "bl", "br", "d", "dr", "f", "fl", "g", "gl", "gr", "h", "k", "kl", "kr", "m", "n", "p", "pr", "r", "s", "sch", "sp", "st", "t", "tr", "w", "z"],
        "vowels": ["a", "e", "i", "o", "u", "ä", "ö", "ü", "ei", "au", "ie"],
        "ends": ["", "n", "r", "l", "t", "s", "ch", "ng", "st"]
    },
    "sv": {
        "starts": ["b", "br", "d", "dr", "f", "fl", "g", "gl", "gr", "h", "k", "kl", "kr", "m", "n", "p", "pr", "r", "s", "sk", "sl", "sm", "sn", "sp", "st", "tr", "v"],
        "vowels": ["a", "e", "i", "o", "u", "y", "å", "ä", "ö", "ei", "au", "ue"],
        "ends": ["", "n", "r", "t", "s", "m", "ng", "st", "sk"]
    },
    "no": {
        "starts": ["b", "bl", "br", "d", "dr", "f", "fl", "g", "gr", "h", "k", "kl", "kr", "l", "m", "n", "p", "pr", "r", "s", "sk", "sl", "sn", "sp", "st", "tr", "v"],
        "vowels": ["a", "e", "i", "o", "u", "y", "æ", "ø", "å", "ei", "au", "ue"],
        "ends": ["", "n", "r", "t", "s", "m", "ng", "st", "sk"]
    }
}

style_modifiers = {
    "Medieval": {
        "starts_add": ["th", "wh", "gh", "kn", "wr", "st", "sc"],
        "ends_add": ["th", "ld", "rd", "st", "sh"],
        "vowels_add": ["ae", "ea", "eo", "io"],
    },
    "Modern": {
        "starts_remove": ["kn", "wr", "gh", "sc"],
        "ends_remove": ["th", "ld", "rd", "sh"],
        "vowels_add": ["oo", "ee", "ai", "ou"],
    },
    "Fantasy": {
        "starts_add": ["x", "z", "q", "zh", "kh", "gh", "th"],
        "ends_add": ["x", "z", "q", "th", "sh", "kh"],
        "vowels_add": ["ae", "io", "ua", "eu", "yy"],
    }
}

def apply_capitalization(name, style):
    if style == "lowercase":
        return name.lower()
    elif style == "capitalize":
        return name.capitalize()
    elif style == "camelCase":
        parts = name.split('_')
        return ''.join(p.capitalize() for p in parts)
    else:
        return name

def generate_syllable(lang, style, complexity):
    base = phonemes[lang].copy()
    mod = style_modifiers.get(style, {})
    starts = base["starts"][:]
    vowels = base["vowels"][:]
    ends = base["ends"][:]
    if "starts_add" in mod:
        starts += mod["starts_add"]
    if "ends_add" in mod:
        ends += mod["ends_add"]
    if "vowels_add" in mod:
        vowels += mod["vowels_add"]
    if "starts_remove" in mod:
        starts = [s for s in starts if s not in mod["starts_remove"]]
    if "ends_remove" in mod:
        ends = [e for e in ends if e not in mod["ends_remove"]]

    if complexity == 1:
        return random.choice(starts) + random.choice(vowels)
    elif complexity == 2:
        return random.choice(starts) + random.choice(vowels) + random.choice(ends)
    else:
        # complexity 3: starts + vowel + end + optional extra vowel
        extra_vowel = random.choice(vowels) if random.random() < 0.5 else ""
        return random.choice(starts) + random.choice(vowels) + random.choice(ends) + extra_vowel

def generate_username(lang, style, min_syll, max_syll, capitalize, add_numbers, add_symbols, complexity):
    syllable_count = random.randint(min_syll, max_syll)
    username = ''.join(generate_syllable(lang, style, complexity) for _ in range(syllable_count))
    if add_numbers:
        username += str(random.randint(0, 99))
    if add_symbols:
        username += random.choice(['_', '-', '.'])
    return apply_capitalization(username, capitalize)

class UsernameGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Username Generator")
        self.geometry("600x450")
        self.language_map = {
            "English": "en",
            "Dutch": "nl",
            "German": "de",
            "Swedish": "sv",
            "Norwegian": "no"
        }
        self.lang_var = tk.StringVar(value="English")
        self.style_var = tk.StringVar(value="Modern")
        self.min_syll_var = tk.IntVar(value=2)
        self.max_syll_var = tk.IntVar(value=3)
        self.complexity_var = tk.IntVar(value=2)
        self.capital_var = tk.StringVar(value="lowercase")
        self.numbers_var = tk.BooleanVar(value=False)
        self.symbols_var = tk.BooleanVar(value=False)
        self.amount_var = tk.IntVar(value=10)
        self.create_widgets()

    def create_widgets(self):
        padding_opts = {'padx': 10, 'pady': 5}
        ttk.Label(self, text="Language:").grid(row=0, column=0, sticky="w", **padding_opts)
        ttk.OptionMenu(self, self.lang_var, self.lang_var.get(), *self.language_map.keys()).grid(row=0, column=1, sticky="ew", **padding_opts)
        ttk.Label(self, text="Style:").grid(row=1, column=0, sticky="w", **padding_opts)
        ttk.OptionMenu(self, self.style_var, self.style_var.get(), "Medieval", "Modern", "Fantasy").grid(row=1, column=1, sticky="ew", **padding_opts)
        ttk.Label(self, text="Min syllables:").grid(row=2, column=0, sticky="w", **padding_opts)
        ttk.Spinbox(self, from_=1, to=6, textvariable=self.min_syll_var, width=5).grid(row=2, column=1, sticky="w", **padding_opts)
        ttk.Label(self, text="Max syllables:").grid(row=3, column=0, sticky="w", **padding_opts)
        ttk.Spinbox(self, from_=1, to=8, textvariable=self.max_syll_var, width=5).grid(row=3, column=1, sticky="w", **padding_opts)
        ttk.Label(self, text="Syllable Complexity (1-3):").grid(row=4, column=0, sticky="w", **padding_opts)
        ttk.Spinbox(self, from_=1, to=3, textvariable=self.complexity_var, width=5).grid(row=4, column=1, sticky="w", **padding_opts)
        ttk.Label(self, text="Capitalization:").grid(row=5, column=0, sticky="w", **padding_opts)
        ttk.OptionMenu(self, self.capital_var, self.capital_var.get(), "lowercase", "capitalize", "camelCase").grid(row=5, column=1, sticky="ew", **padding_opts)
        ttk.Checkbutton(self, text="Add numbers (0-99)", variable=self.numbers_var).grid(row=6, column=0, columnspan=2, sticky="w", **padding_opts)
        ttk.Checkbutton(self, text="Add symbol (_ - .)", variable=self.symbols_var).grid(row=7, column=0, columnspan=2, sticky="w", **padding_opts)
        ttk.Label(self, text="Amount to generate:").grid(row=8, column=0, sticky="w", **padding_opts)
        ttk.Spinbox(self, from_=1, to=50, textvariable=self.amount_var, width=5).grid(row=8, column=1, sticky="w", **padding_opts)
        ttk.Button(self, text="Generate", command=self.generate_usernames).grid(row=9, column=0, columnspan=2, pady=15, sticky="ew", padx=10)
        self.output = tk.Text(self, height=12)
        self.output.grid(row=10, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(1, weight=1)
        ttk.Button(self, text="Save to File", command=self.save_to_file).grid(row=11, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def generate_usernames(self):
        min_syl = self.min_syll_var.get()
        max_syl = self.max_syll_var.get()
        if min_syl > max_syl:
            messagebox.showerror("Error", "Min syllables cannot be greater than max syllables.")
            return
        lang_full = self.lang_var.get()
        lang = self.language_map[lang_full]
        style = self.style_var.get()
        complexity = self.complexity_var.get()
        capitalize = self.capital_var.get()
        add_numbers = self.numbers_var.get()
        add_symbols = self.symbols_var.get()
        amount = self.amount_var.get()
        self.output.delete('1.0', tk.END)
        for _ in range(amount):
            username = generate_username(lang, style, min_syl, max_syl, capitalize, add_numbers, add_symbols, complexity)
            self.output.insert(tk.END, username + "\n")

    def save_to_file(self):
        names = self.output.get('1.0', tk.END).strip()
        if not names:
            messagebox.showinfo("Info", "No usernames to save.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(names)
            messagebox.showinfo("Saved", f"Usernames saved to {filepath}")

if __name__ == "__main__":
    app = UsernameGeneratorApp()
    app.mainloop()
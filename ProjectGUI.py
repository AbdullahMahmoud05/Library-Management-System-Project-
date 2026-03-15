import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ══════════════════════════════════════════════
#  YOUR ORIGINAL CODE  (unchanged)
# ══════════════════════════════════════════════

class Book:
    def __init__(self, book_name, author, year, book_type):
        self.book_name = book_name
        self.author = author
        self.year = year
        self.book_type = book_type
        self._ratings = []

    def get_average_rate(self):
        if not self._ratings:
            return "No Rates Yet"
        return round(sum(self._ratings) / len(self._ratings), 2)

    def add_rating(self, rating):
        if 0 <= rating <= 5:
            self._ratings.append(rating)
            return True
        return False

    def show_info(self):
        print("\n--- Book Info ---")
        print("Book Name :", self.book_name)
        print("Author :", self.author)
        print("Year :", self.year)
        print("Type :", self.book_type)
        print("Average Rate :", self.get_average_rate())
        print("-----------------")


class Library:
    def __init__(self):
        self._books = []

    def _find_book(self, book_name):
        for book in self._books:
            if book.book_name.lower() == book_name.lower():
                return book
        return None


class Books(Library):

    def add_book(self):
        print("\nAdd New Book")
        book_name = input("Enter book name : ")
        author = input("Enter author : ")
        year = input("Enter year : ")
        book_type = input("Enter type : ")

        if self._find_book(book_name):
            print(f"\n '{book_name}'Book is already exists.\nTry another name.")

        book = Book(book_name, author, year, book_type)
        self._books.append(book)
        print(f"\nBook '{book_name}' added successfully!")

    def show_all_books(self):
        if not self._books:
            print("\nNo books found.")
            return

        print("\n=== All Books ===")
        for book in self._books:
            book.show_info()

    def search_book(self):
        book_name = input("\nEnter book name to search: ")
        book = self._find_book(book_name)

        if book:
            book._find_book(book_name).show_info()
        else:
            print(f"\n[✗]'{book_name}' not found.")

    def delete_book(self):
        book_name = input("\nEnter book name to delete: ")
        book = self._find_book(book_name)

        if book:
            self._books.remove(book)
            print(f"\n  '{book_name}' deleted successfully!")
        else:
            print(f"\n '{book_name}' not found.")

    def rate_book(self):
        book_name = input("\nEnter book name to rate: ")
        book = self._find_book(book_name)

        if not book:
            print(f"\n  '{book_name}' not found.")

        raiting = input("Enter rating (0-5): ")
        if book.add_rating(raiting):
            print(f"\nRating added. \nNew Average: {book.get_average_rate()}")
        else:
            print("\nRating must be between 0 and 5.")


# ══════════════════════════════════════════════
#  GUI  LAYER
# ══════════════════════════════════════════════

# ── palette ───────────────────────────────────
BG      = "#0f1117"
PANEL   = "#1a1d27"
CARD    = "#21253a"
ACCENT  = "#4f8ef7"
SUCCESS = "#3ecf8e"
DANGER  = "#f76f6f"
WARNING = "#f7c948"
TEXT    = "#e8eaf6"
SUBTEXT = "#8b90a0"
BORDER  = "#2e3250"

FH1  = ("Helvetica", 20, "bold")
FH2  = ("Helvetica", 13, "bold")
FBODY= ("Helvetica", 11)
FSM  = ("Helvetica", 9)


class LibraryApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.library = Books()          # ← same object your main() uses
        self.title("Library Management System")
        self.geometry("980x640")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build()
        self._refresh()

    # ── master layout ─────────────────────────
    def _build(self):
        # SIDEBAR
        side = tk.Frame(self, bg=PANEL, width=210)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(side, text="📚", font=("Helvetica", 30),
                 bg=PANEL, fg=ACCENT).pack(pady=(22, 0))
        tk.Label(side, text="Library", font=FH1,
                 bg=PANEL, fg=TEXT).pack()
        tk.Label(side, text="Management System", font=FSM,
                 bg=PANEL, fg=SUBTEXT).pack(pady=(0, 12))
        tk.Frame(side, bg=BORDER, height=1).pack(fill="x", padx=14, pady=4)

        # nav
        nav = [
            ("➕  Add Book",        self._gui_add),
            ("📋  Show All Books",  self._gui_show_all),
            ("🔍  Search Book",     self._gui_search),
            ("🗑   Delete Book",    self._gui_delete),
            ("⭐  Rate a Book",     self._gui_rate),
        ]
        for label, cmd in nav:
            b = tk.Button(side, text=label, font=FBODY,
                          bg=PANEL, fg=TEXT, bd=0, pady=10,
                          activebackground=CARD, activeforeground=ACCENT,
                          anchor="w", padx=18, cursor="hand2", command=cmd)
            b.pack(fill="x")
            b.bind("<Enter>", lambda e, w=b: w.config(bg=CARD, fg=ACCENT))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=PANEL, fg=TEXT))

        self._count_lbl = tk.Label(side, text="", font=FSM,
                                   bg=PANEL, fg=SUBTEXT)
        self._count_lbl.pack(side="bottom", pady=14)

        # MAIN
        main = tk.Frame(self, bg=BG)
        main.pack(side="right", fill="both", expand=True)

        hdr = tk.Frame(main, bg=BG, pady=18, padx=22)
        hdr.pack(fill="x")
        self._title_lbl = tk.Label(hdr, text="All Books",
                                   font=FH1, bg=BG, fg=TEXT)
        self._title_lbl.pack(side="left")
        self._msg_lbl = tk.Label(hdr, text="", font=FSM, bg=BG, fg=SUCCESS)
        self._msg_lbl.pack(side="right")

        # search bar
        sf = tk.Frame(main, bg=BG, padx=22)
        sf.pack(fill="x")
        self._q = tk.StringVar()
        self._q.trace_add("write", lambda *_: self._refresh())
        se = tk.Entry(sf, textvariable=self._q, bg=CARD, fg=TEXT,
                      insertbackground=TEXT, relief="flat", font=FBODY,
                      bd=0, highlightthickness=2,
                      highlightcolor=ACCENT, highlightbackground=BORDER)
        se.pack(fill="x", ipady=8, pady=(0, 10))
        se.insert(0, "🔍  Search by name or author…")
        se.bind("<FocusIn>",  lambda e: se.delete(0, "end")
                if se.get().startswith("🔍") else None)
        se.bind("<FocusOut>", lambda e: se.insert(0, "🔍  Search by name or author…")
                if not se.get() else None)

        # table
        tf = tk.Frame(main, bg=BG, padx=22)
        tf.pack(fill="both", expand=True)

        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("T.Treeview",
                     background=CARD, foreground=TEXT, rowheight=34,
                     fieldbackground=CARD, borderwidth=0, font=FBODY)
        st.configure("T.Treeview.Heading",
                     background=PANEL, foreground=ACCENT,
                     font=FH2, relief="flat")
        st.map("T.Treeview", background=[("selected", "#4f5fa8")])

        cols = ("BookName", "Author", "Year", "Type", "AvRate")
        self._tree = ttk.Treeview(tf, columns=cols,
                                  show="headings", style="T.Treeview")
        for col, w in zip(cols, (210, 170, 65, 115, 110)):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center")

        sb = ttk.Scrollbar(tf, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # bottom bar
        bot = tk.Frame(main, bg=PANEL, pady=10, padx=22)
        bot.pack(fill="x", side="bottom")
        for txt, col, cmd in [
            ("⭐ Rate Selected", WARNING, self._rate_selected),
            ("🗑  Delete Selected", DANGER, self._delete_selected),
        ]:
            b = tk.Button(bot, text=txt, font=FBODY, bg=col,
                          fg="#0f1117", bd=0, padx=14, pady=6,
                          cursor="hand2", relief="flat", command=cmd)
            b.pack(side="left", padx=5)

    # ── table refresh ─────────────────────────
    def _refresh(self):
        q = self._q.get().strip().lower()
        if q.startswith("🔍"):
            q = ""
        for r in self._tree.get_children():
            self._tree.delete(r)
        for book in self.library._books:
            if q and q not in book.book_name.lower() \
                 and q not in book.author.lower():
                continue
            av = book.get_average_rate()
            self._tree.insert("", "end", values=(
                book.book_name, book.author, book.year,
                book.book_type,
                f"⭐ {av}" if av != "No Rates Yet" else "— No Rates Yet"
            ))
        n = len(self.library._books)
        self._count_lbl.config(text=f"{n} book{'s' if n != 1 else ''} total")

    def _msg(self, text, color=SUCCESS):
        self._msg_lbl.config(text=text, fg=color)
        self.after(3000, lambda: self._msg_lbl.config(text=""))

    def _selected_name(self):
        sel = self._tree.selection()
        if not sel:
            self._msg("Select a book from the table first.", WARNING)
            return None
        return self._tree.item(sel[0])["values"][0]

    # ── reusable popup ────────────────────────
    def _popup(self, title, fields):
        """Open a form dialog. fields = list of label strings.
           Returns dict {label: value} or None if cancelled."""
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=PANEL)
        win.resizable(False, False)
        win.grab_set()
        win.update_idletasks()
        px, py = self.winfo_x(), self.winfo_y()
        pw, ph = self.winfo_width(), self.winfo_height()
        w = 360
        win.geometry(f"{w}x{len(fields)*72+120}+{px+(pw-w)//2}+{py+(ph-300)//2}")

        tk.Label(win, text=title, font=FH2, bg=PANEL,
                 fg=ACCENT, pady=14).pack()
        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=14)

        body = tk.Frame(win, bg=PANEL, padx=22, pady=10)
        body.pack(fill="both", expand=True)

        entries = {}
        for label in fields:
            tk.Label(body, text=label, font=FBODY,
                     bg=PANEL, fg=SUBTEXT).pack(anchor="w", pady=(8, 2))
            e = tk.Entry(body, bg=CARD, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=FBODY, bd=0,
                         highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
            e.pack(fill="x", ipady=7)
            entries[label] = e

        result = {}

        def submit():
            for lbl, ent in entries.items():
                v = ent.get().strip()
                if not v:
                    self._msg(f"'{lbl}' cannot be empty.", DANGER)
                    return
                result[lbl] = v
            win.destroy()

        def cancel():
            win.destroy()

        bf = tk.Frame(body, bg=PANEL)
        bf.pack(fill="x", pady=(14, 0))
        tk.Button(bf, text="✓  Confirm", font=FBODY, bg=SUCCESS,
                  fg="#0f1117", bd=0, padx=12, pady=6,
                  cursor="hand2", relief="flat",
                  command=submit).pack(side="left", padx=(0, 8))
        tk.Button(bf, text="Cancel", font=FBODY, bg=CARD,
                  fg=TEXT, bd=0, padx=12, pady=6,
                  cursor="hand2", relief="flat",
                  command=cancel).pack(side="left")

        list(entries.values())[0].focus_set()
        win.wait_window()
        return result if result else None

    # ══════════════════════════════════════════
    #  GUI WRAPPERS FOR YOUR 5 METHODS
    # ══════════════════════════════════════════

    # 1. Add Book
    def _gui_add(self):
        self._title_lbl.config(text="Add Book")
        data = self._popup("Add New Book",
                           ["Book Name", "Author", "Year", "Type"])
        if not data:
            return
        # check duplicate (your logic)
        if self.library._find_book(data["Book Name"]):
            self._msg(f"'{data['Book Name']}' already exists!", DANGER)
            return
        book = Book(data["Book Name"], data["Author"],
                    data["Year"], data["Type"])
        self.library._books.append(book)
        self._msg(f"Book '{data['Book Name']}' added successfully!", SUCCESS)
        self._refresh()

    # 2. Show All Books
    def _gui_show_all(self):
        self._title_lbl.config(text="All Books")
        self._q.set("")
        self._refresh()
        if not self.library._books:
            self._msg("No books found.", WARNING)

    # 3. Search Book
    def _gui_search(self):
        self._title_lbl.config(text="Search Book")
        data = self._popup("Search Book", ["Book Name"])
        if not data:
            return
        book = self.library._find_book(data["Book Name"])
        if book:
            # highlight in table
            self._q.set("")
            self._refresh()
            for item in self._tree.get_children():
                if self._tree.item(item)["values"][0].lower() \
                        == book.book_name.lower():
                    self._tree.selection_set(item)
                    self._tree.see(item)
                    break
            self._msg(f"Found: '{book.book_name}'", SUCCESS)
        else:
            self._msg(f"'{data['Book Name']}' not found.", DANGER)

    # 4. Delete Book
    def _gui_delete(self):
        self._title_lbl.config(text="Delete Book")
        data = self._popup("Delete Book", ["Book Name"])
        if not data:
            return
        book = self.library._find_book(data["Book Name"])
        if book:
            if messagebox.askyesno("Confirm",
                                   f"Delete '{book.book_name}'?", parent=self):
                self.library._books.remove(book)
                self._msg(f"'{book.book_name}' deleted.", SUCCESS)
                self._refresh()
        else:
            self._msg(f"'{data['Book Name']}' not found.", DANGER)

    # 5. Rate a Book
    def _gui_rate(self):
        self._title_lbl.config(text="Rate a Book")
        data = self._popup("Rate a Book", ["Book Name", "Rating (0 - 5)"])
        if not data:
            return
        book = self.library._find_book(data["Book Name"])
        if not book:
            self._msg(f"'{data['Book Name']}' not found.", DANGER)
            return
        try:
            rating = float(data["Rating (0 - 5)"])
        except ValueError:
            self._msg("Rating must be a number.", DANGER)
            return
        if book.add_rating(rating):
            self._msg(f"Rating added! Average: {book.get_average_rate()}", SUCCESS)
            self._refresh()
        else:
            self._msg("Rating must be between 0 and 5.", DANGER)

    # ── quick actions from bottom bar ─────────
    def _rate_selected(self):
        name = self._selected_name()
        if not name:
            return
        rating = simpledialog.askfloat(
            "Rate Book", f"Rating for '{name}' (0 – 5):",
            minvalue=0, maxvalue=5, parent=self)
        if rating is None:
            return
        book = self.library._find_book(name)
        if book.add_rating(rating):
            self._msg(f"Average: {book.get_average_rate()}", SUCCESS)
            self._refresh()
        else:
            self._msg("Rating must be 0 – 5.", DANGER)

    def _delete_selected(self):
        name = self._selected_name()
        if not name:
            return
        if messagebox.askyesno("Confirm", f"Delete '{name}'?", parent=self):
            book = self.library._find_book(name)
            if book:
                self.library._books.remove(book)
                self._msg(f"'{name}' deleted.", SUCCESS)
                self._refresh()


# ── run ───────────────────────────────────────
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
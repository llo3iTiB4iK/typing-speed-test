import tkinter as tk
from tkinter.messagebox import showinfo, askyesno
from art import logo
from game import Game

GAME_WINDOW_TITLE = "Typing Speed Test by llo3iTiB4iK"
TIMER_LABEL_DEFAULT = "Start typing to launch timer!"
WORDS_AREA_DEFAULT = "Here will be displayed text to type!"
ENTRY_AREA_DEFAULT = "Write words here!"


def fill_text(event):
    if not event.widget.get().strip():
        clear_text(event)
        event.widget.insert(0, ENTRY_AREA_DEFAULT)


def clear_text(event):
    event.widget.delete(0, tk.END)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game = Game()
        # window config
        self.title(GAME_WINDOW_TITLE)
        self.config(padx=50, pady=50)
        self.resizable(False, False)
        # program header
        self.header = tk.Label(self, text=logo, font="Courier 8")
        self.header.grid(row=0, column=0, columnspan=2)
        # timer label
        self.timer_label = tk.Label(self, font="Helvetica 24")
        self.timer_label.grid(row=1, column=0, pady=40)
        self.timer = ""
        # stop timer button
        self.stop_button = tk.Button(self, text="STOP", borderwidth=5, background="black", foreground="red", font=("Arial", 16, "bold"), command=self.reset_all)
        self.stop_button.grid(row=1, column=1)
        # field showing text to write
        self.words_text = tk.StringVar(self)
        self.words_area = tk.Label(textvariable=self.words_text, borderwidth=2, relief="groove", font=("Courier", 22, "underline"), background="white", padx=10, pady=10, width=len(WORDS_AREA_DEFAULT))
        self.words_area.grid(row=2, column=0, columnspan=2, pady=30)
        # field to enter text
        self.entry_area = tk.Entry(self, justify="center", font="Arial 22")
        self.entry_area.grid(row=3, column=0, columnspan=2)
        self.entry_area.bind("<FocusIn>", self.entry_field_focused)
        self.entry_area.bind("<FocusOut>", fill_text)
        self.entry_area.bind("<space>", self.space_pressed)
        # add confirmation before closing the window
        self.bind("<Escape>", lambda _: self.window_exit())
        self.protocol("WM_DELETE_WINDOW", self.window_exit)
        # restore default widgets values
        self.reset_all()

    def reset_all(self):
        if self.timer:
            self.after_cancel(self.timer)
            self.timer = ""
        self.game.reset()
        self.timer_label.configure(text=TIMER_LABEL_DEFAULT)
        self.stop_button.configure(state="disabled")
        self.words_text.set(WORDS_AREA_DEFAULT)
        self.entry_area.delete(0, tk.END)
        self.entry_area.insert(0, ENTRY_AREA_DEFAULT)
        self.entry_area.bind("<Key>", self.start_timer)
        self.header.focus()

    def fill_words_area(self):
        self.words_text.set(" ".join(self.game.words)[:len(WORDS_AREA_DEFAULT)])

    def entry_field_focused(self, event):
        if self.words_text.get() == WORDS_AREA_DEFAULT:
            self.game.shuffle_words()
            self.fill_words_area()
        if event.widget.get() == ENTRY_AREA_DEFAULT:
            clear_text(event)

    def space_pressed(self, event):
        word_entered = event.widget.get().strip()
        if word_entered:
            self.game.enter_word(word_entered)
            self.fill_words_area()
        clear_text(event)

    def start_timer(self, event):
        if event.char.strip() and event.keysym not in ['Escape', 'BackSpace']:
            event.widget.unbind("<Key>")
            self.stop_button.configure(state="normal")
            self.countdown(60)

    def countdown(self, secs):
        self.timer_label.configure(text=f"{secs} seconds left!")
        if secs > 0:
            self.timer = self.after(1000, self.countdown, secs - 1)
        else:
            self.game.enter_word(self.entry_area.get().strip())
            cpm, wpm, acc = self.game.get_stats()
            showinfo(title="Test finished!", message=f"Your result is {cpm} CPM ({wpm} WPM)\nAccuracy: {acc}%")
            self.reset_all()

    def window_exit(self):
        if askyesno("Exit?", "Are you sure you want to exit?"):
            self.destroy()

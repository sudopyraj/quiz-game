import tkinter as tk
from tkinter import ttk
import requests
import random
import html

# ---------------------- CONFIG ----------------------

API_BASE = "https://opentdb.com/api.php?amount=1&type=multiple"

CATEGORIES = {
    "General Knowledge": 9,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Mathematics": 19,
    "History": 23,
    "Geography": 22,
}

DIFFICULTIES = ["easy", "medium", "hard"]

THEME = {
    "bg": "#121212",
    "panel": "#1e1e1e",
    "accent": "#4CAF50",
    "text": "#ffffff",
    "muted": "#bbbbbb",
    "button": "#2a2a2a",
    "hover": "#333333"
}

# ---------------------- APP ----------------------

class QuizApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("QuizMaster Pro")
        self.geometry("1000x650")
        self.configure(bg=THEME["bg"])
        self.resizable(False, False)

        self.score = 0
        self.total = 0
        self.correct_answer = ""

        self._build_layout()

    # ---------- Layout ----------

    def _build_layout(self):
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = MainArea(self)
        self.main_area.pack(side="right", expand=True, fill="both")

        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

    # ---------- Quiz Logic ----------

    def fetch_question(self, category, difficulty):
        url = f"{API_BASE}&category={category}&difficulty={difficulty}"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()["results"][0]

            question = html.unescape(data["question"])
            self.correct_answer = html.unescape(data["correct_answer"])
            answers = [html.unescape(a) for a in data["incorrect_answers"]]
            answers.append(self.correct_answer)
            random.shuffle(answers)

            self.main_area.display_question(question, answers)

        except:
            self.status_bar.set_status("Failed to fetch question")

    def check_answer(self, selected):
        self.total += 1

        if selected == self.correct_answer:
            self.score += 1
            self.status_bar.set_status("Correct!")
        else:
            self.status_bar.set_status(f"Wrong! Answer: {self.correct_answer}")

        self.main_area.update_score(self.score, self.total)


# ---------------------- SIDEBAR ----------------------

class Sidebar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=THEME["panel"], width=250)
        self.parent = parent

        self.pack_propagate(False)

        self._build()

    def _build(self):
        title = tk.Label(self, text="Quiz Controls",
                         bg=THEME["panel"], fg=THEME["text"],
                         font=("Arial", 16, "bold"))
        title.pack(pady=20)

        self.category_var = tk.StringVar()
        self.category_box = ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=list(CATEGORIES.keys()),
            state="readonly"
        )
        self.category_box.set("Select Category")
        self.category_box.pack(pady=10, padx=20)

        self.difficulty_var = tk.StringVar()
        self.difficulty_box = ttk.Combobox(
            self,
            textvariable=self.difficulty_var,
            values=DIFFICULTIES,
            state="readonly"
        )
        self.difficulty_box.set("Select Difficulty")
        self.difficulty_box.pack(pady=10, padx=20)

        start_btn = StyledButton(
            self,
            text="Start Quiz",
            command=self.start_quiz
        )
        start_btn.pack(pady=30, padx=20, fill="x")

    def start_quiz(self):
        cat = self.category_var.get()
        diff = self.difficulty_var.get()

        if cat in CATEGORIES and diff in DIFFICULTIES:
            self.parent.fetch_question(CATEGORIES[cat], diff)


# ---------------------- MAIN AREA ----------------------

class MainArea(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=THEME["bg"])
        self.parent = parent

        self.answer_var = tk.StringVar()

        self._build()

    def _build(self):
        self.question_label = tk.Label(
            self,
            text="Welcome to QuizMaster",
            wraplength=600,
            bg=THEME["bg"],
            fg=THEME["text"],
            font=("Arial", 18)
        )
        self.question_label.pack(pady=40)

        self.answer_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(
                self,
                text="",
                variable=self.answer_var,
                value="",
                bg=THEME["button"],
                fg=THEME["text"],
                selectcolor=THEME["accent"],
                font=("Arial", 14),
                anchor="w",
                padx=10,
                pady=10,
                wraplength=600
            )
            btn.pack(fill="x", padx=100, pady=5)
            self.answer_buttons.append(btn)

        submit_btn = StyledButton(
            self,
            text="Submit",
            command=self.submit_answer
        )
        submit_btn.pack(pady=30)

        self.score_label = tk.Label(
            self,
            text="Score: 0/0",
            bg=THEME["bg"],
            fg=THEME["muted"],
            font=("Arial", 12)
        )
        self.score_label.pack()

    def display_question(self, question, answers):
        self.question_label.config(text=question)
        self.answer_var.set(None)

        for i, btn in enumerate(self.answer_buttons):
            btn.config(text=answers[i], value=answers[i])

    def submit_answer(self):
        selected = self.answer_var.get()
        if selected:
            self.parent.check_answer(selected)

    def update_score(self, score, total):
        self.score_label.config(text=f"Score: {score}/{total}")


# ---------------------- STATUS BAR ----------------------

class StatusBar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=THEME["panel"], height=30)
        self.pack_propagate(False)

        self.label = tk.Label(
            self,
            text="Ready",
            bg=THEME["panel"],
            fg=THEME["muted"]
        )
        self.label.pack(side="left", padx=10)

    def set_status(self, text):
        self.label.config(text=text)


# ---------------------- STYLED BUTTON ----------------------

class StyledButton(tk.Button):

    def __init__(self, parent, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=THEME["accent"],
            fg="white",
            activebackground=THEME["hover"],
            relief="flat",
            font=("Arial", 12),
            pady=8
        )


# ---------------------- RUN ----------------------

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
import requests
import random
import html
import tkinter as tk
from tkinter import ttk, messagebox

# ----------- CONFIG -----------
CATEGORIES = {
    "General Knowledge": 9,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Mathematics": 19,
    "History": 23,
    "Geography": 22
}

DIFFICULTY = ["easy", "medium", "hard"]

API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"

# ----------- APP CLASS -----------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuizBuddy Pro")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        self.score = 0
        self.total = 0
        self.correct_answer = ""

        self.build_ui()

    def build_ui(self):
        title = tk.Label(self.root, text="QuizBuddy", 
                         font=("Helvetica", 24, "bold"),
                         fg="white", bg="#1e1e2f")
        title.pack(pady=10)

        # Category Dropdown
        self.category_var = tk.StringVar()
        self.category_box = ttk.Combobox(
            self.root, textvariable=self.category_var,
            values=list(CATEGORIES.keys()), state="readonly"
        )
        self.category_box.set("Select Category")
        self.category_box.pack(pady=5)

        # Difficulty Dropdown
        self.difficulty_var = tk.StringVar()
        self.difficulty_box = ttk.Combobox(
            self.root, textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"], state="readonly"
        )
        self.difficulty_box.set("Select Difficulty")
        self.difficulty_box.pack(pady=5)

        # Question Label
        self.question_label = tk.Label(
            self.root, text="Click Start to begin",
            wraplength=600, justify="center",
            font=("Arial", 14),
            fg="white", bg="#1e1e2f"
        )
        self.question_label.pack(pady=20)

        # Answer Buttons
        self.answer_var = tk.StringVar()
        self.answer_buttons = []

        for _ in range(4):
            rb = tk.Radiobutton(
                self.root, text="", variable=self.answer_var,
                font=("Arial", 12),
                fg="white", bg="#2a2a40",
                selectcolor="#444466",
                wraplength=500, anchor="w", justify="left"
            )
            rb.pack(fill="x", padx=50, pady=5)
            self.answer_buttons.append(rb)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame, text="Start Quiz",
            command=self.fetch_question,
            bg="#4CAF50", fg="white",
            font=("Arial", 12), width=15
        )
        self.start_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(
            btn_frame, text="Submit Answer",
            command=self.check_answer,
            bg="#2196F3", fg="white",
            font=("Arial", 12), width=15
        )
        self.next_btn.grid(row=0, column=1, padx=10)

        # Score Label
        self.score_label = tk.Label(
            self.root, text="Score: 0/0",
            font=("Arial", 12),
            fg="white", bg="#1e1e2f"
        )
        self.score_label.pack(pady=10)

    def fetch_question(self):
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()

        if category not in CATEGORIES or difficulty not in DIFFICULTY:
            messagebox.showwarning("Warning", "Select category and difficulty")
            return

        url = f"{API_URL}&category={CATEGORIES[category]}&difficulty={difficulty}"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            q = data["results"][0]

            question = html.unescape(q["question"])
            self.correct_answer = html.unescape(q["correct_answer"])
            answers = [html.unescape(ans) for ans in q["incorrect_answers"]]
            answers.append(self.correct_answer)
            random.shuffle(answers)

            self.question_label.config(text=question)
            self.answer_var.set(None)

            for i in range(4):
                self.answer_buttons[i].config(text=answers[i], value=answers[i])

        except:
            messagebox.showerror("Error", "Failed to fetch question")

    def check_answer(self):
        selected = self.answer_var.get()

        if not selected:
            messagebox.showwarning("Warning", "Select an answer")
            return

        self.total += 1

        if selected == self.correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Nice, you got it right.")
        else:
            messagebox.showinfo("Wrong", f"Correct answer was:\n{self.correct_answer}")

        self.score_label.config(text=f"Score: {self.score}/{self.total}")
        self.fetch_question()

# ----------- RUN APP -----------
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
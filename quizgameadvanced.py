import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os

# ------------------ CONFIG ------------------

LEADERBOARD_FILE = "leaderboard.json"
QUESTION_TIME = 15

CATEGORIES = [
    "General Knowledge", "Science", "Mathematics", "History",
    "Geography", "Computers", "Physics", "Chemistry",
    "Biology", "Sports", "Movies", "Music",
    "Literature", "Politics", "Space", "Inventions",
    "Programming", "AI", "Cybersecurity", "Economics",
    "Philosophy", "Art", "World Capitals", "Mythology",
    "Internet"
]

DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]


# ------------------ MAIN APP ------------------

class QuizApp:

    def __init__(self, root):
        self.root = root
        self.root.title("QuizMaster Pro")
        self.root.geometry("1100x700")
        self.dark_mode = True

        self.score = 0
        self.current_index = 0
        self.time_left = QUESTION_TIME
        self.selected_category = None
        self.selected_difficulty = "Easy"
        self.questions = []

        self.load_leaderboard()
        self.create_layout()
        self.apply_theme()

    # ------------------ UI LAYOUT ------------------

    def create_layout(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.create_category_panel()
        self.create_quiz_panel()
        self.create_status_bar()

        self.root.bind("<Return>", lambda e: self.next_question())
        self.root.bind("<Escape>", lambda e: self.quit_quiz())

    def create_category_panel(self):
        self.left_frame = tk.Frame(self.main_frame, width=250)
        self.left_frame.pack(side="left", fill="y")

        tk.Label(self.left_frame, text="Categories").pack(pady=10)

        canvas = tk.Canvas(self.left_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for cat in CATEGORIES:
            btn = tk.Button(
                self.scroll_frame,
                text=cat,
                command=lambda c=cat: self.select_category(c)
            )
            btn.pack(fill="x", padx=5, pady=3)

        # Difficulty
        tk.Label(self.left_frame, text="Difficulty").pack(pady=10)
        self.diff_combo = ttk.Combobox(
            self.left_frame,
            values=DIFFICULTY_LEVELS,
            state="readonly"
        )
        self.diff_combo.set("Easy")
        self.diff_combo.pack()

        tk.Button(self.left_frame, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.left_frame, text="Toggle Theme", command=self.toggle_theme).pack(pady=5)
        tk.Button(self.left_frame, text="Leaderboard", command=self.show_leaderboard).pack(pady=5)
        tk.Button(self.left_frame, text="Quit", command=self.quit_quiz).pack(pady=20)

    def create_quiz_panel(self):
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.question_label = tk.Label(
            self.right_frame,
            text="Select a category and start the quiz.",
            wraplength=700,
            font=("Arial", 18)
        )
        self.question_label.pack(pady=20)

        self.selected_option = tk.StringVar()
        self.option_buttons = []

        for _ in range(4):
            rb = tk.Radiobutton(
                self.right_frame,
                variable=self.selected_option,
                value="",
                font=("Arial", 14),
                indicatoron=0,
                width=30
            )
            rb.pack(pady=5)
            self.option_buttons.append(rb)

        self.timer_label = tk.Label(self.right_frame, text="")
        self.timer_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.right_frame, length=400)
        self.progress.pack(pady=10)

        tk.Button(self.right_frame, text="Next Question", command=self.next_question).pack(pady=10)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Score: 0", anchor="w")
        self.status_bar.pack(fill="x", side="bottom")

    # ------------------ QUIZ LOGIC ------------------

    def select_category(self, category):
        self.selected_category = category

    def generate_questions(self):
        questions = []
        for i in range(10):
            correct = random.randint(1, 4)
            options = [f"Option {j}" for j in range(1, 5)]
            questions.append({
                "question": f"{self.selected_category} Question {i+1}?",
                "options": options,
                "answer": options[correct - 1]
            })
        return questions

    def start_quiz(self):
        if not self.selected_category:
            messagebox.showwarning("Warning", "Select a category first.")
            return

        self.selected_difficulty = self.diff_combo.get()
        self.questions = self.generate_questions()
        self.score = 0
        self.current_index = 0
        self.display_question()

    def display_question(self):
        if self.current_index >= len(self.questions):
            self.finish_quiz()
            return

        q = self.questions[self.current_index]
        self.question_label.config(text=q["question"])
        self.selected_option.set("")

        for i, option in enumerate(q["options"]):
            self.option_buttons[i].config(text=option, value=option)

        self.progress["value"] = (self.current_index / len(self.questions)) * 100
        self.start_timer()

    def next_question(self):
        if self.current_index >= len(self.questions):
            return

        selected = self.selected_option.get()
        correct = self.questions[self.current_index]["answer"]

        if selected == correct:
            self.score += 1

        self.current_index += 1
        self.status_bar.config(text=f"Score: {self.score}")
        self.display_question()

    def finish_quiz(self):
        self.progress["value"] = 100
        name = simpledialog.askstring("Quiz Finished", f"Score: {self.score}\nEnter your name:")
        if name:
            self.save_score(name, self.score)
        messagebox.showinfo("Done", "Quiz completed!")

    def quit_quiz(self):
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            self.root.destroy()

    # ------------------ TIMER ------------------

    def start_timer(self):
        self.time_left = QUESTION_TIME
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.next_question()

    # ------------------ LEADERBOARD ------------------

    def load_leaderboard(self):
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, "r") as f:
                self.leaderboard = json.load(f)
        else:
            self.leaderboard = []

    def save_score(self, name, score):
        self.leaderboard.append({"name": name, "score": score})
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(self.leaderboard, f, indent=4)

    def show_leaderboard(self):
        text = "\n".join([f"{x['name']} - {x['score']}" for x in self.leaderboard])
        messagebox.showinfo("Leaderboard", text if text else "No scores yet.")

    # ------------------ THEME ------------------

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        bg = "#121212" if self.dark_mode else "#f5f5f5"
        fg = "white" if self.dark_mode else "black"

        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        self.left_frame.configure(bg=bg)
        self.right_frame.configure(bg=bg)

        self.question_label.configure(bg=bg, fg=fg)
        self.timer_label.configure(bg=bg, fg=fg)
        self.status_bar.configure(bg=bg, fg=fg)


# ------------------ RUN ------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
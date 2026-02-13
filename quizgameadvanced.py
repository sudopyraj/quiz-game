# Import required libraries
import requests       # To fetch quiz data from Open Trivia API
import json           # To parse JSON response
import pprint         # (Optional) Pretty print for debugging
import random         # To shuffle answers and randomize messages
import html           # To decode HTML entities from API response

# Counters to track score
no_of_correct_answer = 0
no_of_incorrect_answer = 0

# Ask user name and greet
username = input("Type your Name here: ")
print(f"Hey {username}, welcome to quizbuddy")

# List of difficulty levels for display
difficulty_list0 = ["Easy", "Medium", "Hard"]

# List of available quiz categories (OpenTDB category IDs)
categories = [
    {"id": 9,  "name": "General Knowledge"},
    {"id": 10, "name": "Entertainment: Books"},
    {"id": 11, "name": "Entertainment: Film"},
    {"id": 12, "name": "Entertainment: Music"},
    {"id": 13, "name": "Entertainment: Musicals & Theatres"},
    {"id": 14, "name": "Entertainment: Television"},
    {"id": 15, "name": "Entertainment: Video Games"},
    {"id": 16, "name": "Entertainment: Board Games"},
    {"id": 17, "name": "Science & Nature"},
    {"id": 18, "name": "Science: Computers"},
    {"id": 19, "name": "Science: Mathematics"},
    {"id": 20, "name": "Mythology"},
    {"id": 21, "name": "Sports"},
    {"id": 22, "name": "Geography"},
    {"id": 23, "name": "History"},
    {"id": 24, "name": "Politics"},
    {"id": 25, "name": "Art"},
    {"id": 26, "name": "Celebrities"},
    {"id": 27, "name": "Animals"},
    {"id": 28, "name": "Vehicles"},
    {"id": 29, "name": "Entertainment: Comics"},
    {"id": 30, "name": "Science: Gadgets"},
    {"id": 31, "name": "Entertainment: Japanese Anime & Manga"},
    {"id": 32, "name": "Entertainment: Cartoon & Animations"}
]

# API difficulty values (must be lowercase for API)
difficulty_list = ["easy", "medium", "hard"]

# Random positive feedback messages
correct_messages = [
    "Nice, you actually got it right.",
    "Correct. Miracles do happen.",
    "Yep, that’s the one.",
    "You nailed it.",
    "Right answer. Don’t let it get to your head.",
    "Solid pick, that’s correct.",
    "Correct. Maybe your brain is awake today.",
    "Good job, you hit the target.",
    "Right. Even I’m shocked.",
    "Correct. Keep this streak before it disappears.",
    "Yep, that's the right one.",
    "Correct answer, no complaints from me.",
    "You got it right. Wild.",
    "Correct. I’ll pretend I expected that.",
    "You’re right. Relax, I’m surprised too.",
    "Correct. Look at you… functioning.",
    "Yeah, that’s correct. Don’t get used to it."
]

# Random negative feedback messages (with correct answer inserted)
incorrect_messages = [
    "Nope, the correct answer is {correct_answer}.",
    "Wrong. It’s actually {correct_answer}.",
    "Not even close. Correct is {correct_answer}.",
    "Incorrect. The right one is {correct_answer}.",
    "Nah, that’s not it. It’s {correct_answer}.",
    "Nope. Try again, correct is {correct_answer}.",
    "Wrong guess. Correct answer: {correct_answer}.",
    "You missed it. It's {correct_answer}.",
    "Incorrect. The real answer is {correct_answer}.",
    "Nope. Should’ve gone with {correct_answer}.",
    "Not right. The correct one was {correct_answer}.",
    "Missed it. Correct answer: {correct_answer}.",
    "That’s wrong. Real answer is {correct_answer}.",
    "Nope. The answer is {correct_answer}, not whatever you guessed.",
    "Wrong again. Correct is {correct_answer}.",
    "Incorrect. It was {correct_answer}.",
    "That’s not correct. Try {correct_answer} next time."
]

# Display categories
x = 1
input("\nType Enter to see Categories: ")
for cat in categories:
    print(str(x) + ":", cat["name"])
    x += 1

# Function to safely take numeric input from user
def userinput(cdnum, name):
    while True:
        try:
            user_input = int(input(f"\nType the {name} Number Here: "))
        except ValueError:
            # If user enters non-integer value
            print("type a valid integer here: ")
            continue
        
        # Check if input is within valid range
        if user_input > cdnum or user_input <= 0:
            print(f"Type the valid {name} number here:")
            continue
        
        return user_input

# Get category and difficulty from user
category_choosen = userinput(24, "category")

x = 1
for dif in difficulty_list0:
    print(str(x) + ":", dif)
    x += 1

difficulty_choosen = userinput(3, "Difficulty")

# Get API-compatible values
cate_api = categories[category_choosen - 1]["id"]
diff_api = difficulty_list[difficulty_choosen - 1]

# Build API URL
url = f"https://opentdb.com/api.php?amount=1&category={cate_api}&difficulty={diff_api}&type=multiple"

# Main quiz loop
while True:
    try:
        # Fetch question from API
        r = requests.get(url, timeout=10)
    except:
        # Handle timeout error
        print("Request Timedout Check your internet connection")

    # If request failed
    if r.status_code != 200:
        end_game = input("Failed to fetch question. Press Enter to retry or type 'quit' to exit: ")
        if end_game == "quit":
            break
            
    else:
        # Parse JSON response
        data = json.loads(r.text)

        # Extract question data
        question_data = data['results'][0]

        # Decode HTML characters
        question = html.unescape(question_data['question'])
        difficulty = question_data['difficulty']
        category = html.unescape(question_data['category'])
        correct_answer = html.unescape(question_data['correct_answer'])
        answers = html.unescape(question_data['incorrect_answers'])

        # Add correct answer and shuffle options
        answers.append(correct_answer)
        random.shuffle(answers)

        # Display question info
        print("Category Chosen: ", category)
        print(f"Difficulty  {difficulty}")
        print("\n")
        print(f"Question \n {question}")
        answerno = 1

    # Display answer options
    for i in answers:
        print(str(answerno) +  ":" + "",  i)
        answerno += 1

    # Get user answer
    userans = userinput(4, "Answer number")
    check_ans = answers[userans - 1]

    # Random feedback message
    message_for_correctans = random.choice(correct_messages)
    message_for_incorrectans = random.choice(incorrect_messages).format(correct_answer=correct_answer)

    # Check answer and update score
    if check_ans == correct_answer:
        print(message_for_correctans)
        no_of_correct_answer += 1
    else:
        print(message_for_incorrectans)
        no_of_incorrect_answer += 1

    # Ask to play again
    play_again = input("wanna play again if yes then enter else type 'quit': ").lower()
    if play_again == "quit":
        break

# Final score display
print("\nThank you for Playing 👇")
print("########################")
print("Your Score:")
print("Correct answer:", no_of_correct_answer)
print("incorrect answer:", no_of_incorrect_answer)
print("########################")






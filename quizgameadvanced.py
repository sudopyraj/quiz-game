
import requests
import json
import pprint
import random
import html

no_of_correct_answer = 0
no_of_incorrect_answer = 0

username = input("Type your Name here: ")
print(f"Hey {username}, welcome to quizbuddy")

#Lists

difficulty_list0 = ["Easy", "Medium", "Hard"]

categories = [    {"id": 9,  "name": "General Knowledge"},    {"id": 10, "name": "Entertainment: Books"},    {"id": 11, "name": "Entertainment: Film"},    {"id": 12, "name": "Entertainment: Music"},    {"id": 13, "name": "Entertainment: Musicals & Theatres"},    {"id": 14, "name": "Entertainment: Television"},    {"id": 15, "name": "Entertainment: Video Games"},    {"id": 16, "name": "Entertainment: Board Games"},    {"id": 17, "name": "Science & Nature"},    {"id": 18, "name": "Science: Computers"},    {"id": 19, "name": "Science: Mathematics"},    {"id": 20, "name": "Mythology"},    {"id": 21, "name": "Sports"},    {"id": 22, "name": "Geography"},    {"id": 23, "name": "History"},    {"id": 24, "name": "Politics"},    {"id": 25, "name": "Art"},    {"id": 26, "name": "Celebrities"},    {"id": 27, "name": "Animals"},    {"id": 28, "name": "Vehicles"},    {"id": 29, "name": "Entertainment: Comics"},    {"id": 30, "name": "Science: Gadgets"},    {"id": 31, "name": "Entertainment: Japanese Anime & Manga"},    {"id": 32, "name": "Entertainment: Cartoon & Animations"}]

difficulty_list = ["easy", "medium", "hard"]

correct_messages = [    "Nice, you actually got it right.",    "Correct. Miracles do happen.",    "Yep, that’s the one.",    "You nailed it.",    "Right answer. Don’t let it get to your head.",    "Solid pick, that’s correct.",    "Correct. Maybe your brain is awake today.",    "Good job, you hit the target.",    "Right. Even I’m shocked.",    "Correct. Keep this streak before it disappears.",    "Yep, that's the right one.",    "Correct answer, no complaints from me.",    "You got it right. Wild.",    "Correct. I’ll pretend I expected that.",    "You’re right. Relax, I’m surprised too.",    "Correct. Look at you… functioning.",    "Yeah, that’s correct. Don’t get used to it."]

incorrect_messages = ["Nope, the correct answer is {correct_answer}.",    "Wrong. It’s actually {correct_answer}.",    "Not even close. Correct is {correct_answer}.",    "Incorrect. The right one is {correct_answer}.",    "Nah, that’s not it. It’s {correct_answer}.",    "Nope. Try again, correct is {correct_answer}.",    "Wrong guess. Correct answer: {correct_answer}.",    "You missed it. It's {correct_answer}.",    "Incorrect. The real answer is {correct_answer}.",    "Nope. Should’ve gone with {correct_answer}.",    "Not right. The correct one was {correct_answer}.",    "Missed it. Correct answer: {correct_answer}.",    "That’s wrong. Real answer is {correct_answer}.",    "Nope. The answer is {correct_answer}, not whatever you guessed.",    "Wrong again. Correct is {correct_answer}.",    "Incorrect. It was {correct_answer}.",    "That’s not correct. Try {correct_answer} next time."]


x = 1
input("\nType Enter to see Categories: ")
for cat in categories:   
    print(str(x) + ":", cat["name"])
    x += 1
#input function
def userinput(cdnum,name):
    while True:
        try:
            user_input = int(input(f"\nType the {name} Number Here: "))
        except ValueError:
            print("type a valid integer here: ")
            continue
        if user_input > cdnum or user_input <= 0:
            print(f"Type the valid {name} number here:")
            continue
        
        return user_input
category_choosen = userinput(24,"category")

x = 1

for dif in difficulty_list0:
    print(str(x) + ":", dif)
    x += 1
difficulty_choosen = userinput(3,"Difficulty")

cate_api = categories[category_choosen - 1]["id"]
diff_api = difficulty_list[difficulty_choosen - 1]

url = f"https://opentdb.com/api.php?amount=1&category={cate_api}&difficulty={diff_api}&type=multiple"

#bulding quiz game logic

while True:
    try:

    
        r = requests.get(url, timeout=10)
    except:
        print("Request Timedout Check your internet connection")
    if r.status_code != 200:
        end_game = input("Failed to fetch question. Press Enter to retry or type 'quit' to exit: ")
        if end_game == "quit":
            break
            
    else:
        data = json.loads(r.text)
        # pprint.pprint(data)

        question_data = data['results'][0]

        question = html.unescape(question_data['question'])
        difficulty = question_data['difficulty']
        category = html.unescape(question_data['category'])
        correct_answer = html.unescape(question_data['correct_answer'])
        answers = html.unescape(question_data['incorrect_answers'])


        answers.append(correct_answer)
        random.shuffle(answers)

        print("Category Chosen: ", category)
        print(f"Difficulty  {difficulty}")
        print("\n")
        print(f"Question \n {question}")
        answerno = 1


    
    for i in answers:
        print(str(answerno) +  ":" + "",  i)
        answerno += 1
    userans = userinput(4,"Answer number")
    
    check_ans = answers[userans - 1]

    message_for_correctans = random.choice(correct_messages)
    message_for_incorrectans = random.choice(incorrect_messages).format(correct_answer=correct_answer)

    if check_ans == correct_answer:
        print(message_for_correctans)
        no_of_correct_answer += 1
    else:
        print(message_for_incorrectans)
        no_of_incorrect_answer += 1
    play_again = input("wanna play again if yes then enter else type 'quit': ").lower()
    if play_again == "quit":
            break
print("\nThank you for Playing 👇")
print("########################")
print("Your Score:")
print("Correct answer:", no_of_correct_answer)
print("incorrect answer:", no_of_incorrect_answer)
print("########################")

        





    






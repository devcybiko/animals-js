#!/usr/bin/env python3
import time
import json

birdQuestion = {
    "value": "robin",
    "yes": None,
    "no": None
}
fishQuestion = {
    "value": "salmon",
    "yes": None,
    "no": None
}
root = {
    "value": "does it fly",
    "yes": birdQuestion,
    "no": fishQuestion
};

def addQuestion(currentQuestion, yesOrNo, question, animalName):
    oldAnimal = currentQuestion.get(yesOrNo)
    newAnimal = {
        "value": animalName,
        "yes": None,
        "no": None
    }
    newQuestion = {
        "value": question,
        "yes": newAnimal,
        "no": oldAnimal
    }
    currentQuestion[yesOrNo] = newQuestion
    # if yesOrNo == 'yes':
    #     oldAnimal = currentQuestion.get("yes")
    #     currentQuestion["yes"] = newQuestion
    #     newQuestion["no"] = oldAnimal
    # else:
    #     oldAnimal = currentQuestion.get("no")
    #     currentQuestion["no"] = newQuestion
    #     newQuestion["no"] = oldAnimal

def _dump(msg, node, currentNode, cnt=0):
    if not node: return
    checked = ""
    if node == currentNode: checked = " <==="
    out = " | "*cnt + msg + node.get("value") + checked
    print(out)
    _dump("yes: ", node["yes"], currentNode, cnt+1)
    _dump(" no: ", node["no"], currentNode, cnt+1)

def dump_decision_tree(node):
    print("")
    _dump("", root, node)
    print("")

def inquire(prompt):
    s = input(prompt + "? ")
    s = s.lower().strip()
    return s

def yes_or_no(prompt):
    while True:
        s = inquire(prompt)
        if s == "y" or s=="yes": return "yes"
        if s == "n" or s=="no": return "no"
        if s == "q" or s=="quit": return "quit"
        print("Please enter 'yes', 'no' or 'quit'")

def ask_question(currentQuestion):
    answer = yes_or_no(currentQuestion.get("value"))
    if answer == "yes":
        nextQuestion = currentQuestion.get("yes")
    elif answer == "no":
        nextQuestion = currentQuestion.get("no")
    return [nextQuestion, answer]

def new_animal(currentQuestion, lastQuestion, lastAnswer, cnt):
    animal = currentQuestion.get("value")
    answer = yes_or_no("is it a " + animal)
    if answer == "yes":
        print("")
        print("I knew it! I got it in " + str(cnt) + " tries")
        print("Thanks for the game!\n")
    elif answer == "no":
        newAnimal = inquire("What animal were you thinking of")
        question = inquire("Please enter a question to differentiate a "+newAnimal+" from a " + animal)
        addQuestion(lastQuestion, lastAnswer, question, newAnimal)
    return answer

def read_decision_tree():
    global root
    try:
        with open('tree.json') as f:
            root = json.load(f)
    except:
        write_decision_tree() ### initialize the missing file

def write_decision_tree():
    with open('tree.json', 'w') as f:
        json.dump(root, f, indent=2)

def play_game():
    currentQuestion = root
    lastQuestion = currentQuestion
    lastAnswer = "no"
    cnt=0
    while lastAnswer != "quit":
        cnt = cnt + 1
        dump_decision_tree(currentQuestion)
        if currentQuestion["yes"] != None: ### it's an question, not a animal
            [nextQuestion, lastAnswer] = ask_question(currentQuestion)
            lastQuestion = currentQuestion
            currentQuestion = nextQuestion
        else:
            lastAnswer = new_animal(currentQuestion, lastQuestion, lastAnswer, cnt)
            break
    return lastAnswer

def main():
    read_decision_tree()
    again = "yes"
    while again == "yes":
        lastAnswer = play_game()
        write_decision_tree()
        if lastAnswer == "quit": again = "no"
        else: again = yes_or_no("Would you like to play again, or 'quit'")

main()
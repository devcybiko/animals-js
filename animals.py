#!/usr/bin/env python3
import time
import json

birdNode = {
    "value": "robin",
    "yes": None,
    "no": None
}
fishNode = {
    "value": "salmon",
    "yes": None,
    "no": None
}
root = {
    "value": "does it fly",
    "yes": birdNode,
    "no": fishNode
};

def addQuestion(node, yesOrNo, question, animalName):
    oldAnimal = node.get(yesOrNo)
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
    node[yesOrNo] = newQuestion
    # if yesOrNo == 'yes':
    #     oldAnimal = node.get("yes")
    #     node["yes"] = newNode
    #     newNode["no"] = oldAnimal
    # else:
    #     oldAnimal = node.get("no")
    #     node["no"] = newNode
    #     newNode["no"] = oldAnimal

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

def ask_question(node):
    answer = yes_or_no(node.get("value"))
    if answer == "yes":
        node = node.get("yes")
    elif answer == "no":
        lastNode = node
        lastAnswer = answer
        node = node.get("no")
    return [node, answer]

def ask_animal(node, lastNode, lastAnswer, cnt):
    answer = yes_or_no("is it a " + node.get("value"))
    if answer == "yes":
        print("")
        print("I knew it! I got it in " + str(cnt) + " tries")
        print("Thanks for the game!\n")
    elif answer == "no":
        animal = inquire("What animal were you thinking of")
        question = inquire("Please enter a question to differentiate a "+animal+" from a " + node.get("value"))
        addQuestion(lastNode, lastAnswer, question, animal)
    again = yes_or_no("Would you like to play again, or 'quit'")
    return [node, again]

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

def main():
    read_decision_tree()
    node = root
    lastNode = node
    lastAnswer = "no"
    cnt=0
    while True:
        cnt = cnt + 1
        dump_decision_tree(node)
        if node.get("yes") != None:
            lastNode = node
            [node, lastAnswer] = ask_question(node)
            if lastAnswer == "quit": break
        else:
            [node, again] = ask_animal(node, lastNode, lastAnswer, cnt)
            write_decision_tree()
            if again == "quit" or again == "no": break
            cnt = 0
            node = root

main()
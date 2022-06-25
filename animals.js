#!/usr/bin/env node

const glstools = require('glstools');
const gprocs = glstools.procs;
const gstrings = glstools.strings;
const gfiles = glstools.files;
const fs = require("fs");
const path = require("path");
const { Input, AutoComplete } = require('enquirer');

let birdNode = {
    type: "animal",
    value: "bird",
    yes: null,
    no: null
}
let fishNode = {
    type: "animal",
    value: "fish",
    yes: null,
    no: null
}
let root = {
    type: "question",
    value: "does it fly?",
    yes: birdNode,
    no: fishNode
};

function addQuestion(node, yesOrNo, question, animalName) {
    let animal = {
        type: "animal",
        value: animalName,
        yes: null,
        no: null
    };
    let newNode = {
        type: "question",
        value: question,
        yes: animal,
        no: null
    };
    if (yesOrNo === 'yes') {
        let oldAnimal = node.yes;
        node.yes = newNode;
        newNode.no = oldAnimal
    } else {
        let oldAnimal = node.no;
        node.no = newNode;
        newNode.no = oldAnimal;
    }
}

async function readline(prompt) {
    const input = new Input({
        name: 'name',
        message: prompt
    });
    let line = await input.run();
    return line;
}

function dump(msg, node, currentNode, cnt=0) {
    if (!node) return;
    let checked = "";
    if (node === currentNode) checked = " <===";
    let out = " | ".repeat(cnt) + msg + node.value + checked;
    console.log(out);
    dump("yes: ", node.yes, currentNode, cnt+1);
    dump(" no: ", node.no, currentNode, cnt+1);
}
async function main$(_opts) {
    let opts = _opts || gprocs.args("", "");
    let node = root;
    let lastNode = root;
    let lastAnswer = "n";
    while (true) {
        dump("", root, node);
        if (node.type === "question") {
            let answer = (await readline(node.value)).toLowerCase();
            if (answer === "y" || answer === "yes") {
                lastNode = node;
                lastAnswer = answer;
                node = node.yes;
            } else if (answer === "n" || answer === "no") {
                lastNode = node;
                lastAnswer = answer;
                node = node.no;
            }
            else console.log("(please answer 'y' or 'n'");
        } else {
            let answer = (await readline("is it a " + node.value)).toLowerCase();
            if (answer === "y" || answer === "yes") {
                console.log("I knew it! Let's play again!");
                node = root;
            } else if (answer === "n" || answer === "no") {
                let animal = await readline("What animal were you thinking of?");
                let question = await readline(`Please enter a question to differentiate a ${node.value} from a ${animal}?`);
                addQuestion(lastNode, lastAnswer, question, animal);
                node = root;
                console.log("Let's play again!");
            }
            else console.log("(please answer 'y' or 'n'");
        }
    }
}

module.exports = { main$ }

if (module.id === ".") {
    return main$();
}

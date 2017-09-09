from random import *
from operator import *
from threading import *
from subprocess import *
from pymongo import *
from pprint import *

student_users = {}


class MathsQuiz(object):
    def __init__(self, studentName):
        self.studentName = studentName
        self.randomNumber1 = 0
        self.randomNumber2 = 0
        self.randomSign = 0
        self.studentScore = 0

    def start_quiz(self):
        questionNumber = 0
        while True:

            # noinspection PyBroadException
            try:
                maxQuestions = int(input(
                    "Enter the number of questions in integer form. "
                )
                )
                break
            except:
                print(
                    "That is an invalid input. "
                )
                continue
        for questionNumber in range(1, maxQuestions + 1):
            self.ask_question()
            print(
                "\nYou are currently on {} / {}"
                .format(self.studentScore,
                        questionNumber
                        )
            )
        print(
            "{} , your final score was {} / {}"
            .format(self.studentName,
                    self.studentScore,
                    questionNumber
                    )
        )

    def random_generator(self):
        self.randomNumber1 = randint(0, 10)
        self.randomNumber2 = randint(0, 10)
        self.randomSign = choice(["+",
                                  "-",
                                  "*"])

    def ask_question(self):
        self.random_generator()
        operator = {"+": add,
                    "-": sub,
                    "*": mul}
        while True:
            # noinspection PyBroadException
            try:
                studentGuess = int(input(
                    "Enter the answer to {} {} {}\n"
                    .format(self.randomNumber1,
                            self.randomSign,
                            self.randomNumber2
                            )
                )
                )
                break
            except:
                print(
                    "That is an invalid answer, try again."
                )
                continue
        # noinspection PyTypeChecker
        if studentGuess == operator[self.randomSign](self.randomNumber1,
                                                     self.randomNumber2
                                                     ):
            print(
                "Correct."
            )
            self.studentScore += 1
        else:
            print(
                "Incorrect."
            )


def mongod_startup():
    call("mongodb-startup.bat")


class Mongo(object):
    def __init__(self, studentName):
        self.studentName = studentName
        self.client = MongoClient()
        self.db = self.client.maths_quiz
        self.collection = self.db.studentScores

    def store_to_database(self):
        postToDatabase = {"name": self.studentName,
                          "score": student_users[self.studentName].studentScore}
        self.db.posts.insert_one(postToDatabase)

    def read_from_database(self):
        pprint(self.db.posts.find_one({"name": self.studentName}))

    def delete_from_database(self):
        self.db.posts.delete_one({"name": self.studentName})

    def overwrite_score_from_database(self):
        self.db.posts.update({"name": self.studentName},
                             {"$set": {"score": student_users[self.studentName].studentScore}})

    def delete_entire_database(self):
        self.client.db.command("dropDatabase")


def startup():
    print(
        "This is a basic Maths quiz,"
        "answer each question,"
        "at the end you will get a score.\n\n"
    )
    while True:
        quizOrQuit = input(
            "Do you wish to participate? (Y/N)"
        ).lower()
        if quizOrQuit not in "yesno":
            print(
                "Not a valid input."
            )
        else:
            break
    if quizOrQuit in "yes":
        studentName = str(input(
            "What is your name? "
        )
        )
        student_users[studentName] = MathsQuiz(studentName)
        student_users[studentName].start_quiz()
    else:
        quit()


mongodStartup = Thread(target=mongod_startup)
mongodStartup.start()
startup()

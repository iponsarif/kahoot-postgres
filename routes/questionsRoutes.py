from flask import request, json, jsonify, abort
import os

from . import router, getQuiz, questionsFileLocation
from src.utils.file import readFile, writeFile
from src.utils.authorization import verifyLogin

# bikin soal untuk kuis yang udah ada
@router.route('/quizzes/<int:quizId>/questions', methods=['POST'])
@verifyLogin
def createQuestion(quizId):
    body = request.json
    body["quiz-id"] = quizId

    response = {
        "error": False
    }

    questionData = {
        "questions": []
    }

    questionData = readFile(questionsFileLocation)

    questionData["questions"].append(body)
    
    response["data"] = body
    response["message"] = "berhasil membuat question"

    writeFile(questionsFileLocation, questionData)

    return jsonify(response)

# minta data sebuah soal untuk kuis tertentu
@router.route('/quizzes/<int:quizId>/questions/<int:questionNumber>') # methods=["GET", "PUT", "DELETE"] PUT = update
def getThatQuestion(quizId, questionNumber):
    
    quizData = getQuiz(quizId).json

    response = {
        "error": False
    }

    try:
        for question in quizData["data"]["question-list"]:
            if question["question-number"] == questionNumber:
                return jsonify(question)
        raise Exception("Soal Gaketemu")
    except Exception:
        response["error"] = True
        response["message"] = "Soal Gaketemuuuuuuuu"
    return jsonify(response)


@router.route('/quizzes/<int:quizId>/questions/<int:questionNumber>', methods=["PUT", "DELETE"])
def updateDeleteQuestion(quizId, questionNumber):
    if request.method == "DELETE":
        return deleteQuestion(quizId, questionNumber)
    elif request.method == "PUT":
        return updateQuestion(quizId, questionNumber)

def deleteQuestion(quizId, questionNumber):
    questionData = readFile(questionsFileLocation)
    
    response = {
        "error": False
    }

    questionToBeDeleted = getThatQuestion(quizId, questionNumber).json # ambil dari fungsi getThatQuestion

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i]["question-number"] == questionToBeDeleted["question-number"]:
            del questionData["questions"][i]
            
            response["message"] = "Berhasil menghapus question Number " + str(questionNumber) + " dari quiz id " + str(quizId)
            break
        else:
            response["error"] = True
            response["message"] = "Gagal menghapus. Tidak ada quiz-id " + str(quizId) + " atau question Number " + str(questionNumber)

    writeFile(questionsFileLocation, questionData)

    return jsonify(response)

def updateQuestion(quizId, questionNumber):
    body = request.json
    isQuestionFound = False

    response = {
        "error": False
    }

    try:
        questionData = readFile(questionsFileLocation)
    except:
        response["error"] = True
        response["message"] = "questions-file tidak ada"
        return jsonify(response)
    else:
        try:
            questionToBeUpdated = getThatQuestion(quizId, questionNumber).json # ambil dari fungsi getThatQuestion
        except:
            return getThatQuestion(quizId, questionNumber)
        else:
            for i in range(len(questionData["questions"])):
                if "question-number" not in questionToBeUpdated:
                    return getThatQuestion(quizId, questionNumber)
                elif questionData["questions"][i]["question-number"] == questionToBeUpdated["question-number"]:                
                    isQuestionFound = True
                    break

    if isQuestionFound:
        # questionData["questions"][i]["quiz-id"] = body["quiz-id"] # ga bisa update quiz-id-nya kayanya
        questionData["questions"][i]["question-number"] = body["question-number"]
        questionData["questions"][i]["question"] = body["question"]
        questionData["questions"][i]["answer"] = body["answer"]
        questionData["questions"][i]["options"]["A"] = body["options"]["A"]
        questionData["questions"][i]["options"]["B"] = body["options"]["B"]
        questionData["questions"][i]["options"]["C"] = body["options"]["C"]
        questionData["questions"][i]["options"]["D"] = body["options"]["D"]

        response["data"] = questionData["questions"][i]
        response["message"] = "Berhasil mengubah question Number " + str(questionNumber)
        writeFile(questionsFileLocation, questionData)
    else:
        response["error"] = True
        response["message"] = "Gagal mengubah. tidak ada question number " + str(questionNumber)

    return jsonify(response)
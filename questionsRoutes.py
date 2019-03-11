from flask import request, json, jsonify

from models import Questions, Quizzess, Options
from app import app
from models import db

# from . import router, getQuiz, questionsFileLocation
# from src.utils.file import readFile, writeFile
# from src.utils.authorization import verifyLogin

@app.route('/getAllQuestions', methods=['GET'])
def get_all_questions():
    try:
        questions = Questions.query.all()
        return jsonify([quest.serialize() for quest in questions])
    except Exception as e:
        return(str(e))

# get question by id
@app.route('/getQuestion/<id_>', methods=['GET'])
def get_question_by_id(id_):
    try:
        question = Questions.query.filter_by(id=id_).first()
        return jsonify(question.serialize())
    except Exception as e:
        return(str(e))

# create question
@app.route('/quiz/<quiz_id_>/createQuestion', methods=['POST'])
def create_question(quiz_id_):
    quiz_id = quiz_id_
    question = request.args.get('question')
    number = request.args.get('number')
    answer = request.args.get('answer')

    try:
        question = Questions(
            quiz_id = quiz_id,
            question = question,
            number = number,
            answer = answer
            )
        db.session.add(question)
        db.session.commit()
        return 'Question added, question id ={}'.format(question.id)
    except Exception as e:
        return(str(e))

@app.route('/quiz/updateQuestion/<id_>', methods=['POST'])
def update_question(id_):
    # ngambil dulu data quiz yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    _question = get_question_by_id(id_).json 
    
    question = request.args.get('question')
    number = request.args.get('number')
    answer = request.args.get('answer')

    # kalau yg diupdate tidak semua kolom
    if question is None:
        question = _question['question']

    if number is None:
        number = _question['number']

    if answer is None:
        answer = _question['answer']
        
    try:
        question_ = {
            'question': question,
            'number': number,
            'answer': answer
        }
        
        db.session.query(Questions).filter_by(id=id_).update(question_)
        db.session.commit()
        return 'Question updated, question id ={}'.format(id_)
    except Exception as e:
        return(str(e))

# hard delete question by id
@app.route('/quiz/deleteQuestion/<id_>', methods=['DELETE'])
def delete_question(id_):
    try:
        question = Questions.query.filter_by(id=id_).first()
        db.session.delete(question)
        db.session.commit()
        return 'Question deleted, question id={}'.format(id_)
    except Exception as e:
        return(str(e))

# =====================================================
# # bikin soal untuk kuis yang udah ada
# @router.route('/quizzes/<int:quizId>/questions', methods=['POST'])
# @verifyLogin
# def createQuestion(quizId):
#     body = request.json
#     body["quiz-id"] = quizId

#     response = {
#         "error": False
#     }

#     questionData = {
#         "questions": []
#     }

#     questionData = readFile(questionsFileLocation)

#     questionData["questions"].append(body)
    
#     response["data"] = body
#     response["message"] = "berhasil membuat question"

#     writeFile(questionsFileLocation, questionData)

#     return jsonify(response)

# # minta data sebuah soal untuk kuis tertentu
# @router.route('/quizzes/<int:quizId>/questions/<int:questionNumber>') # methods=["GET", "PUT", "DELETE"] PUT = update
# def getThatQuestion(quizId, questionNumber):
    
#     quizData = getQuiz(quizId).json

#     response = {
#         "error": False
#     }

#     try:
#         for question in quizData["data"]["question-list"]:
#             if question["question-number"] == questionNumber:
#                 return jsonify(question)
#         raise Exception("Soal Gaketemu")
#     except Exception:
#         response["error"] = True
#         response["message"] = "Soal Gaketemuuuuuuuu"
#     return jsonify(response)


# @router.route('/quizzes/<int:quizId>/questions/<int:questionNumber>', methods=["PUT", "DELETE"])
# def updateDeleteQuestion(quizId, questionNumber):
#     if request.method == "DELETE":
#         return deleteQuestion(quizId, questionNumber)
#     elif request.method == "PUT":
#         return updateQuestion(quizId, questionNumber)

# def deleteQuestion(quizId, questionNumber):
#     questionData = readFile(questionsFileLocation)
    
#     response = {
#         "error": False
#     }

#     questionToBeDeleted = getThatQuestion(quizId, questionNumber).json # ambil dari fungsi getThatQuestion

#     for i in range(len(questionData["questions"])):
#         if questionData["questions"][i]["question-number"] == questionToBeDeleted["question-number"]:
#             del questionData["questions"][i]
            
#             response["message"] = "Berhasil menghapus question Number " + str(questionNumber) + " dari quiz id " + str(quizId)
#             break
#         else:
#             response["error"] = True
#             response["message"] = "Gagal menghapus. Tidak ada quiz-id " + str(quizId) + " atau question Number " + str(questionNumber)

#     writeFile(questionsFileLocation, questionData)

#     return jsonify(response)

# def updateQuestion(quizId, questionNumber):
#     body = request.json
#     isQuestionFound = False

#     response = {
#         "error": False
#     }

#     try:
#         questionData = readFile(questionsFileLocation)
#     except:
#         response["error"] = True
#         response["message"] = "questions-file tidak ada"
#         return jsonify(response)
#     else:
#         try:
#             questionToBeUpdated = getThatQuestion(quizId, questionNumber).json # ambil dari fungsi getThatQuestion
#         except:
#             return getThatQuestion(quizId, questionNumber)
#         else:
#             for i in range(len(questionData["questions"])):
#                 if "question-number" not in questionToBeUpdated:
#                     return getThatQuestion(quizId, questionNumber)
#                 elif questionData["questions"][i]["question-number"] == questionToBeUpdated["question-number"]:                
#                     isQuestionFound = True
#                     break

#     if isQuestionFound:
#         # questionData["questions"][i]["quiz-id"] = body["quiz-id"] # ga bisa update quiz-id-nya kayanya
#         questionData["questions"][i]["question-number"] = body["question-number"]
#         questionData["questions"][i]["question"] = body["question"]
#         questionData["questions"][i]["answer"] = body["answer"]
#         questionData["questions"][i]["options"]["A"] = body["options"]["A"]
#         questionData["questions"][i]["options"]["B"] = body["options"]["B"]
#         questionData["questions"][i]["options"]["C"] = body["options"]["C"]
#         questionData["questions"][i]["options"]["D"] = body["options"]["D"]

#         response["data"] = questionData["questions"][i]
#         response["message"] = "Berhasil mengubah question Number " + str(questionNumber)
#         writeFile(questionsFileLocation, questionData)
#     else:
#         response["error"] = True
#         response["message"] = "Gagal mengubah. tidak ada question number " + str(questionNumber)

#     return jsonify(response)
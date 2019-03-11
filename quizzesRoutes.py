from flask import request, json, jsonify

from models import Quizzess, Questions
from app import app
from models import db

# from src.utils.file import readFile, writeFile
# from src.utils.authorization import verifyLogin

# get all quizzess
@app.route('/quiz/getAllQuizzess', methods=['GET'])
def get_all_quizzess():
    try:
        quizzess = Quizzess.query.order_by(Quizzess.id).all()
        return jsonify([quiz.serialize() for quiz in quizzess])
    except Exception as e:
        return(str(e))

# get quiz by id
@app.route('/quiz/getQuiz/<id_>', methods=['GET'])
def get_quiz_by_id(id_):
    response = {}

    # ambil quiz
    try:
        quiz = Quizzess.query.filter_by(id=id_).first()
        response["quiz"] = quiz.serialize()
    except Exception as e:
        return(str(e))

    # ambil questions dari quiz tersebut
    try:
        questions = Questions.query.filter_by(quiz_id=id_).all()
        serializedQuestions = [quest.serialize() for quest in questions]
        response["quiz"]["question-list"] = serializedQuestion
    except Exception as e:
        return(str(e))

    return jsonify(response)

# create quiz
@app.route('/quiz/createQuiz', methods=['POST'])
def create_quiz():
    creator_id = request.args.get('creator_id')
    title = request.args.get('title')
    category = request.args.get('category')

    try:
        quiz = Quizzess(
            creator_id = creator_id,
            title = title,
            category = category,
            )
        db.session.add(quiz)
        db.session.commit()
        return 'Quiz added, quiz id ={}'.format(quiz.id)
    except Exception as e:
        return(str(e))

# update quiz by quiz.id
@app.route('/quiz/updateQuiz/<id_>', methods=['POST'])
def update_quiz(id_):
    # ngambil dulu data quiz yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    quiz = get_quiz_by_id(id_).json 
    
    creator_id = request.args.get('creator_id')
    title = request.args.get('title')
    category = request.args.get('category')

    # kalau yg diupdate tidak semua kolom
    if creator_id is None:
        creator_id = quiz['username']

    if title is None:
        title = quiz['password']

    if category is None:
        category = quiz['fullname']
        
    try:
        quiz_ = {
            'creator_id': creator_id,
            'title': title,
            'category': category
        }
        
        db.session.query(Quizzess).filter_by(id=id_).update(quiz_)
        db.session.commit()
        return 'Quiz updated, quiz id ={}'.format(id_)
    except Exception as e:
        return(str(e))

# hard delete quiz by id
@app.route('/quiz/deleteQuiz/<id_>', methods=['DELETE'])
def delete_quiz(id_):
    try:
        quiz = Quizzess.query.filter_by(id=id_).first()
        db.session.delete(quiz)
        db.session.commit()
        return 'Quiz deleted, quiz id={}'.format(id_)
    except Exception as e:
        return(str(e))


# ==================================================
# # bikin kuis baru
# @app.route('/quizzes', methods=['POST'])
# # @verifyLogin
# def createQuiz():
#     body = request.json

#     response = {
#         "error": False
#     }
    
#     quizData = {
#         "total-quiz-available": 0,
#         "quizzes": []
#     }    

#     # ga perlu try except disini karena mau ada atau ngga filenya, mode open nya 'w
#     quizData = readFile(quizzesFileLocation)
        
#     quizData["total-quiz-available"] += 1
#     quizData["quizzes"].append(body)

#     response["data"] = body
#     response["message"] = "berhasil menambah data"
    
#     writeFile(quizzesFileLocation, quizData)
    
#     return jsonify(response)

# # meminta data kuis dan soalnya
# @app.route('/quizzes/<int:quizId>')
# def getQuiz(quizId):
#     # nyari quiznya
#     isQuizFound = False
#     response = {
#         "error": False
#     }

#     try:
#         quizzesData = readFile(quizzesFileLocation)
#     except:
#         response["message"] = "error load quiz data"
#         return jsonify(response)
#     else:
#         for quiz in quizzesData["quizzes"]:
#             if quiz["quiz-id"] == quizId:
#                 quizData = quiz
#                 isQuizFound = True

#                 response["data"] = quizData
#                 break
            
#     if isQuizFound:
#         # nyari soalnya
#         try:
#             questionData = readFile(questionsFileLocation)
#         except:
#             print("File questions gada")
#         else:
#             for question in questionData["questions"]:
#                 if question["quiz-id"] == quizId:
#                     quizData["question-list"].append(question)
#     else:
#         response["error"] = True
#         response["message"] = "no quiz found"

#     return jsonify(response)

# # delete quis sama ubah informasi tentang kuisnya
# @app.route('/quizzes/<int:quizId>', methods=["PUT", "DELETE"])
# # @verifyLogin
# def updateDeleteQuiz(quizId):
#     if request.method == "DELETE":
#         return deleteQuiz(quizId)
#     elif request.method == "PUT":
#         return updateQuiz(quizId)

# # fungsi hapus quiz berdasarkan quiz-id
# def deleteQuiz(quizId):
#     response = {
#         "error": False
#     }

#     try:
#         quizData = readFile(quizzesFileLocation)
#     except:
#         response["error"] = True
#         response["message"] = "quizzes-file tidak ada"
#         return jsonify(response)
#     else:
#         for i in range(len(quizData["quizzes"])):
#             quiz = quizData["quizzes"][i]

#             if quiz["quiz-id"] == quizId: # nyari indeks quiz yg akan dihapus
#                 del quizData["quizzes"][i] # hapus quiz
#                 quizData["total-quiz-available"] -= 1 # kurangi total quiz
#                 response["message"] = "Berhasil menghapus quiz id " + str(quizId)
                
#                 writeFile(quizzesFileLocation, quizData)
#                 break
#             else:
#                 response["error"] = True
#                 response["message"] = "Gagal menghapus. Tidak ada quiz-id " + str(quizId)

#     # nyari question sesuai quiz-id lalu hapus 
#     questionData = readFile(questionsFileLocation)

#     # looping ini sisa 1 question dg quiz-id sama, belum bisa semua hapus dalam 1 for(karena out of range)
#     for i in range(len(questionData["questions"])):
#         if i < len(questionData["questions"]):
#             question = questionData["questions"][i]

#             if question["quiz-id"] == quizId:
#                 del questionData["questions"][i]

#     # looping untuk hapus 1 question sisa
#     for j in range(i,len(questionData["questions"])):
#         question = questionData["questions"][j]

#         if question["quiz-id"] == quizId:
#             del questionData["questions"][j]
#             response["message"] += " dan semua questionnya"
#             break

#     writeFile(questionsFileLocation, questionData)

#     return jsonify(response)

# # fungsi ubah quiz berdasarkan quiz-id
# def updateQuiz(quizId):
#     body = request.json
    
#     response = {
#         "error": False
#     }

#     try:
#         quizData = readFile(quizzesFileLocation)
#     except:
#         response["error"] = True
#         response["message"] = "quizzes-file tidak ada"
#         return jsonify(response)
#     else:
#         for i in range(len(quizData["quizzes"])):
#             quiz = quizData["quizzes"][i]

#             if quiz["quiz-id"] == quizId: # nyari indeks quiz yg akan didelete
#                 quiz["quiz-id"] = body["quiz-id"] # hapus line ini kalau quiz-id ga bisa diubah
#                 quiz["quiz-name"] = body["quiz-name"]
#                 quiz["quiz-category"] = body["quiz-category"]
                
#                 quizData["quizzes"][i] = quiz
#                 response["data"] = quiz
#                 response["message"] = "Berhasil mengubah quiz id " + str(quizId)
#                 writeFile(quizzesFileLocation, quizData)
#                 break
#             else:
#                 response["error"] = True
#                 response ["message"] = "Gagal mengubah. Tidak ada quiz-id " + str(quizId)

#     return jsonify(response)
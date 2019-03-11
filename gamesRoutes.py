from flask import request, json, jsonify
import os
from random import randint

from . import router, quizzesFileLocation, gamesFileLocation, questionsFileLocation
from src.utils.file import readFile, writeFile

@router.route('/games', methods=['POST'])
def createGame():
    body = request.json

    quizzesData = readFile(quizzesFileLocation)

    for quiz in quizzesData["quizzes"]:
        if quiz["quiz-id"] == int(body["quiz-id"]):
            gameInfo = quiz
    
    gameInfo["game-pin"] = randint(100000,999999)
    gameInfo["user-list"] = []
    gameInfo["leaderboard"] = []

    gamesData ={
        "game-list":[]
    }    

    # simpen data game nya
    if os.path.exists(gamesFileLocation):
        gamesData = readFile(gamesFileLocation)

    gamesData["game-list"].append(gameInfo)        

    writeFile(gamesFileLocation, gamesData)

    return jsonify(gameInfo)

@router.route('/games/join', methods=['POST'])
def joinGame():
    body = request.json

    # open game data information
    gamesData = readFile(gamesFileLocation)

    position = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if body["username"] not in game["user-list"]: # kalau usernamenya udah ada, jangan di append
                game["user-list"].append(body["username"])
                game["leaderboard"].append({
                    "username": body["username"],
                    "score": 0
                })

                gameInfo = game
                position = i
                break
            # todo : error kalau usernya udah dipake

    gamesData["game-list"][position] = gameInfo
    
    writeFile(gamesFileLocation, gamesData)

    return jsonify(gameInfo)

@router.route('/games/answer', methods=['POST'])
def submitAnswer():    
    isTrue = False
    body = request.json

    #buka file question
    questionData = readFile(questionsFileLocation)

    for question in questionData["questions"]:
        if question["quiz-id"] == int(body["quiz-id"]) and question["question-number"] == int(body["question-number"]):
            if question["answer"] == body["answer"]:
                isTrue = True

    # todo: update skor/leaderboard
    gamesData = readFile(gamesFileLocation)

    gamePosition = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if isTrue:                
                userPosition = 0
                for j in range(len(game["leaderboard"])):
                    userData = game["leaderboard"][j]
                    
                    if userData["username"] == body["username"]:                        
                        userData["score"] += 100
                        
                        userInfo = userData
                        userPosition = j
                        break
                
                game["leaderboard"][userPosition] = userInfo
                gameInfo = game
                gamePosition = i
                break

    gamesData["game-list"][gamePosition] = gameInfo
    
    writeFile(gamesFileLocation, gamesData)
                
    return jsonify(request.json)


@router.route('/games/<gamePin>/leaderboard')
def getLeaderboard(gamePin):
    isGamePinFound = False
    response = {
        "error" : True
    }

    try:
        gamesData = readFile(gamesFileLocation)
    except:
        response["message"] = "error load games data"
        return jsonify(response)
    else:        
        for game in gamesData["game-list"]:
            if game["game-pin"] == int(gamePin): #body["game-pin"]
                leaderboard = game["leaderboard"]
                isGamePinFound = True
                break
    
    if isGamePinFound:
        # Descending using selection sort
        for i in range(len(leaderboard)):
            largest = leaderboard[i]["score"]
            largestPosition = leaderboard[i]
            for j in range(i,len(leaderboard)):
                if leaderboard[j]["score"] >= largest:
                    largest = leaderboard[j]["score"]
                    largestPosition = leaderboard[j]
                    positionCounter = j

            leaderboard[i], leaderboard[positionCounter] = largestPosition, leaderboard[i] # swap posisi pertama setiap looping dengan posisi largest
        
        response["data"] = leaderboard
    else:
        response["message"] = "Game pin not found"

    return jsonify(response)

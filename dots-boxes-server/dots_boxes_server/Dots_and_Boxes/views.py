import json
import math

from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.
peoniCovek = 0
peoniAI = 0


@api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
def apiOverview(request):
     body_unicode = request.body.decode('UTF-8')
     requestBody = json.loads(body_unicode)

     matrix = requestBody['matrix']
     mod = requestBody['mod']

     move = AIMove(matrix, mod)

     return Response(move)


def AIMove(matrix, mod):
     global peoniAI

     bestMove = ""
     score = -math.inf
     bestScore = -math.inf
     rowNumber = len(matrix)
     colNumber = len(matrix[0])  

     for i in range(rowNumber):
          for j in range(colNumber):

               provera = False
               m = makeMove(matrix, i, j)
               if(len(m) > 0): 
                    print(str(m[0]) + " " + str(m[1]))
                    matrix[m[0]][m[1]][m[2]] = True                        #making a move
                    if  matrix[m[0]][m[1]]['clickedSides'] == 4:
                         provera = True
                         peoniAI += 1
                    if(len(m) > 3): 
                         print(str(m[3]) + " " + str(m[4]))
                         matrix[m[3]][m[4]][m[5]] = True
                         if  matrix[m[3]][m[4]]['clickedSides'] == 4:
                              provera = True
                              peoniAI += 1
                    if provera: score = miniMax(matrix, m, mod, 2, True, True)                           #setting score
                    else: score = miniMax(matrix, m, mod, 2, False, True)

                    matrix[m[0]][m[1]]['clickedSides'] -= 1
                    matrix[m[0]][m[1]][m[2]] = False
                    if(len(m) > 3): 
                         matrix[m[3]][m[4]][m[5]] = False       #undo on a move
                         matrix[m[3]][m[4]]['clickedSides'] -= 1

                    if score > bestScore:                                  #set the best score
                         bestMove = setBestMove(m, rowNumber, colNumber)
                         bestScore = score
                         
     return bestMove


def miniMax(matrix, m, mod, depth, isMaximizing, isHardMaxHeur):
     rows = len(matrix)
     cols = len(matrix[0])

     global peoniAI
     global peoniCovek

     if mod == "Hard":
          if depth == 0: 
               if isHardMaxHeur: return hardMaxHeur(matrix, m)
               return hardMinHeur(matrix, m)
     elif mod == "Medium":
          return mediumHeur(matrix, m)
     else:
          return easyHeur(matrix, m)

     if isMaximizing:
          maxScore = -math.inf
          for i in range(rows):
               for j in range(cols):
                    m = makeMove(matrix, i, j)
                    if(len(m) > 0):
                         matrix[m[0]][m[1]][m[2]] = True                        #making a move
                         if(len(m) > 3): matrix[m[3]][m[4]][m[5]] = True

                         if matrix[m[0]][m[1]]['clickedSides'] == 4: 
                              peoniAI += 1
                              score = miniMax(matrix, m, mod, depth-1, True, True)
                         else: score = miniMax(matrix, m, mod, depth-1, False, True)                            #setting score

                         if score > maxScore: maxScore = score

                         matrix[m[0]][m[1]]['clickedSides'] -= 1
                         matrix[m[0]][m[1]][m[2]] = False
                         if(len(m) > 3): 
                              matrix[m[3]][m[4]][m[5]] = False                       #undo on a move
                              matrix[m[3]][m[4]]['clickedSides'] -= 1
                         peoniAI -= 1

          return maxScore

     else:
          minScore = math.inf
          for i in range(rows):
               for j in range(cols):
                    m = makeMove(matrix, i, j)
                    if(len(m) > 0):
                         matrix[m[0]][m[1]][m[2]] = True                             #making a move
                         if(len(m) > 3): matrix[m[3]][m[4]][m[5]] = True
                         
                         if matrix[m[0]][m[1]]['clickedSides'] == 4: 
                              peoniCovek += 1
                              score = miniMax(matrix, m, mod, depth-1, False, False)
                         else: score = miniMax(matrix, m, mod, depth-1, True, False)              #setting score

                         if score < minScore: minScore = score

                         matrix[m[0]][m[1]]['clickedSides'] -= 1
                         matrix[m[0]][m[1]][m[2]] = False
                         if(len(m) > 3): 
                              matrix[m[3]][m[4]][m[5]] = False                       #undo on a move
                              matrix[m[3]][m[4]]['clickedSides'] -= 1
                         peoniCovek -= 1
          return minScore


def hardMaxHeur(matrix, m):
     global peoniAI
                  
     if matrix[m[0]][m[1]]['clickedSides'] == 4: score = 30           
     elif matrix[m[0]][m[1]]['clickedSides'] == 3: score = -10            
     elif matrix[m[0]][m[1]]['clickedSides'] == 2: score = 5
     else: score = 1
     if len(m) > 3:
          if matrix[m[3]][m[4]]['clickedSides'] == 4: score += 30
          if matrix[m[3]][m[4]]['clickedSides'] == 3: score -= 10
          elif matrix[m[3]][m[4]]['clickedSides'] == 2: score += 5
          else: score += 1
     for p in range(peoniAI):
          score += 10
     return score


def hardMinHeur(matrix, m):
     global peoniCovek
                  
     if matrix[m[0]][m[1]]['clickedSides'] == 4: score = -30           
     elif matrix[m[0]][m[1]]['clickedSides'] == 3: score = 10            
     elif matrix[m[0]][m[1]]['clickedSides'] == 2: score = -5
     else: score = -1
     if len(m) > 3:
          if matrix[m[3]][m[4]]['clickedSides'] == 4: score -= 30
          if matrix[m[3]][m[4]]['clickedSides'] == 3: score += 10
          elif matrix[m[3]][m[4]]['clickedSides'] == 2: score -= 5
          else: score -= 1
     for p in range(peoniCovek):
          score -= 10
     return score


def mediumHeur(matrix, m):                                       
     score = 0                                                           
     if matrix[m[0]][m[1]]['clickedSides'] == 4: score = 10               
     elif matrix[m[0]][m[1]]['clickedSides'] == 3: score = -2             
     else: score = 1
     if len(m) > 3: 
          if matrix[m[3]][m[4]]['clickedSides'] == 4: score += 10
          if matrix[m[3]][m[4]]['clickedSides'] == 3: score -= 2
          else: score += 1

     return score


def easyHeur(matrix, m):
     if len(m) > 3:
          print("clickedSides " + str(matrix[m[3]][m[4]]['clickedSides']))
          if matrix[m[3]][m[4]]['clickedSides'] == 4: 
               score = 10
               print("clickedSides " + str(matrix[m[0]][m[1]]['clickedSides']))
               if matrix[m[0]][m[1]]['clickedSides'] == 4: score += 10
               print(str(score))
               return score

     print("clickedSides " + str(matrix[m[0]][m[1]]['clickedSides']))
     if matrix[m[0]][m[1]]['clickedSides'] == 4: 
          print("10")
          return 10
     print("1")
     return 1



def makeMove(matrix, i, j):
     move = []
     
     if matrix[i][j]['clickedSides'] < 4:
          if i < (len(matrix)-1): # horizontal clicks
               if matrix[i][j]['top'] == False:
                    move.append(i)
                    move.append(j)
                    move.append("top")
                    matrix[i][j]['clickedSides'] += 1
                    if i > 0: 
                         move.append(i-1)
                         move.append(j)
                         move.append("bottom")
                         matrix[i-1][j]['clickedSides'] += 1
          else:
               if matrix[i][j]['top'] == False:
                    move.append(i)
                    move.append(j)
                    move.append("top")
                    move.append(i-1)
                    move.append(j)
                    move.append("bottom")
                    matrix[i][j]['clickedSides'] += 1
                    matrix[i-1][j]['clickedSides'] += 1
               else:
                    if matrix[i][j]['bottom'] == False: 
                         move.append(i)
                         move.append(j)
                         move.append("bottom")
                         matrix[i][j]['clickedSides'] += 1
          print("Vertical move: " + str(len(move)))
          if len(move) == 0 or matrix[i][j-1]['clickedSides'] == 3:
               move = []
               if j < (len(matrix[0])-1): # vertical clicks
                    if matrix[i][j]['left'] == False:
                         move.append(i)
                         move.append(j)
                         move.append("left")
                         matrix[i][j]['clickedSides'] += 1
                         if j > 0: 
                              move.append(i)
                              move.append(j-1)
                              move.append("right")
                              matrix[i][j-1]['clickedSides'] += 1
               else:
                    if matrix[i][j]['left'] == False:
                         move.append(i)
                         move.append(j)
                         move.append("left")
                         move.append(i)
                         move.append(j-1)
                         move.append("right")
                         matrix[i][j]['clickedSides'] += 1
                         matrix[i][j-1]['clickedSides'] += 1
                    else: 
                         if matrix[i][j]['right'] == False: 
                              move.append(i)
                              move.append(j)
                              move.append("right")
                              matrix[i][j]['clickedSides'] += 1
     return move
                              
def setBestMove(m, rowNumber, colNumber):
     if m[2] == "top" : bestMove = str(m[0]) + str(m[1]) + "h"
     if m[0] == rowNumber - 1 and m[2] == "bottom" : bestMove = str(m[0]+1) + str(m[1]) + "h"
     if m[2] == "left" : bestMove = str(m[0]) + str(m[1]) + "v"
     if m[1] == colNumber - 1 and m[2] == "right" : bestMove = str(m[0]) + str(m[1]+1) + "v"
     return bestMove     
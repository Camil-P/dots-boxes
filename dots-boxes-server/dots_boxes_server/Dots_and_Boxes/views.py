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

     for i in range(rowNumber+1):
          for j in range(colNumber+1):
               for leftRight in range(2):
                    provera = False
                    m = makeMove(matrix, i, j, leftRight)
                    if(len(m) > 0):
                         if  matrix[m[0]][m[1]]['clickedSides'] == 4:
                              provera = True
                              peoniAI += 1
                         if(len(m) > 3):
                              if  matrix[m[3]][m[4]]['clickedSides'] == 4:
                                   provera = True
                                   peoniAI += 1

                         if provera: score = miniMax(matrix, m, mod, 2, True, -math.inf, math.inf, True)                           #setting score
                         else: score = miniMax(matrix, m, mod, 2, False, -math.inf, math.inf, True)
                         
                         matrix[m[0]][m[1]][m[2]] = False
                         matrix[m[0]][m[1]]['clickedSides'] -= 1
                         if matrix[m[0]][m[1]]['clickedSides'] == 3: peoniAI -= 1
                         if(len(m) > 3): 
                              matrix[m[3]][m[4]][m[5]] = False                  #undo
                              matrix[m[3]][m[4]]['clickedSides'] -= 1
                              if matrix[m[3]][m[4]]['clickedSides'] == 3: peoniAI -= 1

                         print("Score: " + str(score))
                         if score > bestScore:                                  #set the best score
                              bestMove = setBestMove(m, rowNumber, colNumber)
                              bestScore = score
                              print("i: " + str(m[0]) + " j: " + str(m[1]) + " str: " + str(m[2]))
                              print("Najbolji score: " + str(bestScore))
                         
     return bestMove


def miniMax(matrix, m, mod, depth, isMaximizing, alpha, beta, isHardMaxHeur):
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
          for i in range(rows+1):
               for j in range(cols+1):
                    for leftRight in range(2):
                         provera = False
                         m = makeMove(matrix, i, j, leftRight)
                         if(len(m) > 0):
                              if  matrix[m[0]][m[1]]['clickedSides'] == 4:
                                   provera = True
                                   peoniAI += 1
                              if(len(m) > 3):
                                   if  matrix[m[3]][m[4]]['clickedSides'] == 4:
                                        provera = True
                                        peoniAI += 1

                              if provera: score = miniMax(matrix, m, mod, depth-1, True, alpha, beta, True)                           #setting score
                              else: score = miniMax(matrix, m, mod, depth-1, False, alpha, beta, True)

                              if score > maxScore: maxScore = score

                              matrix[m[0]][m[1]][m[2]] = False
                              matrix[m[0]][m[1]]['clickedSides'] -= 1
                              if matrix[m[0]][m[1]]['clickedSides'] == 3: peoniAI -= 1
                              if(len(m) > 3): 
                                   matrix[m[3]][m[4]][m[5]] = False                       #undo on a move
                                   matrix[m[3]][m[4]]['clickedSides'] -= 1
                                   if matrix[m[3]][m[4]]['clickedSides'] == 3: peoniAI -= 1

                              if alpha > score: alpha = score
                              if beta <= alpha:
                                   return maxScore
          if maxScore == -math.inf: return 1
          return maxScore

     else:
          minScore = math.inf
          for i in range(rows+1):
               for j in range(cols+1):
                    for leftRight in range(2):
                         provera = False
                         m = makeMove(matrix, i, j, leftRight)
                         if(len(m) > 0):
                              if  matrix[m[0]][m[1]]['clickedSides'] == 4:
                                   provera = True
                                   peoniCovek += 1
                              if(len(m) > 3):
                                   if  matrix[m[3]][m[4]]['clickedSides'] == 4:
                                        provera = True
                                        peoniCovek += 1

                              if provera: score = miniMax(matrix, m, mod, depth-1, False,  alpha, beta, False)                           #setting score
                              else: score = miniMax(matrix, m, mod, depth-1, True, alpha, beta, False)

                              if score < minScore: minScore = score
                              
                              matrix[m[0]][m[1]][m[2]] = False
                              matrix[m[0]][m[1]]['clickedSides'] -= 1
                              if matrix[m[0]][m[1]]['clickedSides'] == 3: peoniCovek -= 1
                              if(len(m) > 3): 
                                   matrix[m[3]][m[4]][m[5]] = False                       #undo on a move
                                   matrix[m[3]][m[4]]['clickedSides'] -= 1
                                   if matrix[m[3]][m[4]]['clickedSides'] == 3: peoniCovek -= 1

                              if beta < score: beta = score
                              if beta <= alpha:
                                   return minScore
          if minScore == math.inf: return -1
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
     # print("i: " + str(m[0]) + " j: " + str(m[1]) + " str: " + str(m[2]))
     # print(str(score))
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
     # print("i: " + str(m[0]) + " j: " + str(m[1]) + " str: " + str(m[2]))
     # print(str(score))
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
          if matrix[m[3]][m[4]]['clickedSides'] == 4: 
               score = 10
               if matrix[m[0]][m[1]]['clickedSides'] == 4: score += 10
               return score

     if matrix[m[0]][m[1]]['clickedSides'] == 4: 
          return 10
     return 1



def makeMove(matrix, i, j, leftRight):
     move = []
     rows = len(matrix)
     cols = len(matrix[0])

     if i < rows and j < cols:
          if matrix[i][j]['clickedSides'] < 4:
               if not leftRight: 
                    if matrix[i][j]['left'] == False:
                         if j > 0:
                              move.append(i)
                              move.append(j)
                              move.append("left")
                              move.append(i)
                              move.append(j-1)
                              move.append("right")

                              matrix[i][j]['clickedSides'] += 1
                              matrix[i][j-1]['clickedSides'] += 1
                              matrix[i][j]['left'] = True
                              matrix[i][j-1]['right'] = True
                         else:
                              move.append(i)
                              move.append(j)
                              move.append("left")
                              matrix[i][j]['left'] = True
                              matrix[i][j]['clickedSides'] += 1   # isto ovo samo za bottom
               else:
                    if matrix[i][j]['top'] == False:
                         if i > 0:
                              move.append(i)
                              move.append(j)
                              move.append("top")
                              move.append(i-1)
                              move.append(j)
                              move.append("bottom")                   # dodavanje u niz move (potez)

                              matrix[i][j]['top'] = True
                              matrix[i-1][j]['bottom'] = True         
                              matrix[i][j]['clickedSides'] += 1
                              matrix[i-1][j]['clickedSides'] += 1
                         else:
                              move.append(i)
                              move.append(j)
                              move.append("top")
                              matrix[i][j]['top'] = True
                              matrix[i][j]['clickedSides'] += 1

     else:
          if j == cols and i < rows:
               if matrix[i][j-1]['right'] == False:
                    move.append(i)
                    move.append(j-1)
                    move.append("right")
                    matrix[i][j-1]['right'] = True
                    matrix[i][j-1]['clickedSides'] += 1
          if i == rows and j < cols:
               if matrix[i-1][j]['bottom'] == False:
                    move.append(i-1)
                    move.append(j)
                    move.append("bottom")
                    matrix[i-1][j]['bottom'] = True
                    matrix[i-1][j]['clickedSides'] += 1 

     return move


                              
def setBestMove(m, rowNumber, colNumber):
     if m[2] == "top" : bestMove = str(m[0]) + str(m[1]) + "h"
     if m[0] == rowNumber - 1 and m[2] == "bottom" : bestMove = str(m[0]+1) + str(m[1]) + "h"
     if m[2] == "left" : bestMove = str(m[0]) + str(m[1]) + "v"
     if m[1] == colNumber - 1 and m[2] == "right" : bestMove = str(m[0]) + str(m[1]+1) + "v"
     return bestMove     
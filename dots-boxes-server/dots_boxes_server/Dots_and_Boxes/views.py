import json
import math

from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.

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
     bestMove = ""
     score = -math.inf
     bestScore = -math.inf
     rowNumber = len(matrix)
     colNumber = len(matrix[0])  

     for i in range(rowNumber):
          for j in range(colNumber):

               m = makeMove(matrix, i, j)
               if(len(m) > 0):
                    matrix[m[0]][m[1]][m[2]] = True                        #making a move
                    if(len(m) > 3): matrix[m[3]][m[4]][m[5]] = True

                    score = miniMax(matrix, m, mod)                           #setting score

                    matrix[m[0]][m[1]]['clickedSides'] -= 1
                    matrix[m[0]][m[1]][m[2]] = False
                    if(len(m) > 3): 
                         matrix[m[3]][m[4]][m[5]] = False       #undo on a move
                         matrix[m[3]][m[4]]['clickedSides'] -= 1

                    if score > bestScore:                                  #set the best score
                         bestMove = setBestMove(m, rowNumber, colNumber)
                         bestScore = score
                         
     return bestMove


def miniMax(matrix, m, mod, depth):
     if mod == "Hard":
          points = hardHeur(matrix, m)
          if depth == 6 or points >= 10: 
               return points
     if mod == "Medium":
          return mediumHeur(matrix, m)
     if mod == "Easy":
          return easyHeur(matrix, m)


def mediumHeur(matrix, m):                                                # Nacin poentiranja: 
     score = 0                                                            # za 4. stranu 1 kocke = 10 pena, 2 kocke jos 10
     matrix[m[0]][m[1]]['clickedSides'] += 1                              # za 3. stranu 1 kocke = -10 pena, 2 kocke jos -10
     if matrix[m[0]][m[1]]['clickedSides'] == 4: score = 10               # za 2. stranu 1 kocke = 5 pena, 2 kocke jos 5
     elif matrix[m[0]][m[1]]['clickedSides'] == 2: score = 5              # za 1. stranu 1 kocke = 1 pena, 2 kocke jos 1
     elif matrix[m[0]][m[1]]['clickedSides'] == 1: score = 1
     else: score = -10
     if len(m) > 3: 
          matrix[m[3]][m[4]]['clickedSides'] += 1
          if matrix[m[3]][m[4]]['clickedSides'] == 4: score += 10
          elif matrix[m[3]][m[4]]['clickedSides'] == 2: score += 5
          elif matrix[m[3]][m[4]]['clickedSides'] == 1: score += 1
          else: score -= 10 

     return score


def easyHeur(matrix, m):
     matrix[m[0]][m[1]]['clickedSides'] += 1
     if len(m) > 3: 
          matrix[m[3]][m[4]]['clickedSides'] += 1
          if matrix[m[3]][m[4]]['clickedSides'] == 4: 
               score = 10
               if matrix[m[0]][m[1]]['clickedSides'] == 4: score += 10
               return score

     if matrix[m[0]][m[1]]['clickedSides'] == 4: return 10
     return 1



def makeMove(matrix, i, j):
     move = []
     
     if(matrix[i][j]['allSides'] == 0):
          if i < (len(matrix)-1): # horizontal clicks
               if matrix[i][j]['top'] == False:
                    move.append(i)
                    move.append(j)
                    move.append("top")
                    if i > 0: 
                         move.append(i-1)
                         move.append(j)
                         move.append("bottom")
          else:
               if matrix[i][j]['top'] == False:
                    move.append(i)
                    move.append(j)
                    move.append("top")
                    move.append(i-1)
                    move.append(j)
                    move.append("bottom")
               else:
                    if matrix[i][j]['bottom'] == False: 
                         move.append(i)
                         move.append(j)
                         move.append("bottom")

          if len(move) == 0:
               if j < (len(matrix[0])-1): # vertical clicks
                    if matrix[i][j]['left'] == False:
                         move.append(i)
                         move.append(j)
                         move.append("left")
                         if j > 0: 
                              move.append(i)
                              move.append(j-1)
                              move.append("right")
               else:
                    if matrix[i][j]['left'] == False:
                         move.append(i)
                         move.append(j)
                         move.append("left")
                         move.append(i)
                         move.append(j-1)
                         move.append("right")
                    else: 
                         if matrix[i][j]['right'] == False: 
                              move.append(i)
                              move.append(j)
                              move.append("right")
     return move
                              
def setBestMove(m, rowNumber, colNumber):
     if m[2] == "top" : bestMove = str(m[0]) + str(m[1]) + "h"
     if m[0] == rowNumber - 1 and m[2] == "bottom" : bestMove = str(m[0]+1) + str(m[1]) + "h"
     if m[2] == "left" : bestMove = str(m[0]) + str(m[1]) + "v"
     if m[1] == colNumber - 1 and m[2] == "right" : bestMove = str(m[0]) + str(m[1]+1) + "v"
     return bestMove     
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
     
     # for i in range(len(matrix)):
     #      for j in range(len(matrix[0])):
     #           print(matrix[i][j])

     move = ""

     if mod == "Easy":
          move = AIMove(matrix, mod)
     # elif mod == "Medium":
          
     # else: 

     return Response(move)

def miniMax(matrix, mod):
     return 1

def AIMove(matrix, mod):
     bestMove = ""
     score = -math.inf
     bestScore = -math.inf
     rowNumber = len(matrix)
     colNumber = len(matrix[0])

     for i in range(rowNumber):
          for j in range(colNumber):
               if(matrix[i][j]['allSides'] == 0):
                    if i < rowNumber-1: # horizontal clicks
                         if matrix[i][j]['top'] == False: 
                              print(str(j))
                              matrix[i][j]['top'] = True 
                              if i > 0: matrix[i-1][j]['bottom'] = True 
                              score = miniMax(matrix, mod)
                              if score > bestScore: # set score
                                   bestScore = score
                                   bestMove = str(i) + str(j) + 'h'
                                   print(str(i) + str(j))
                              matrix[i][j]['top'] = False
                              if i > 0: matrix[i-1][j]['bottom'] = False        
                    else:
                         if matrix[i][j]['top'] == False:
                              matrix[i][j]['top'] = True
                              score = miniMax(matrix, mod)
                              matrix[i][j]['top'] = False
                         else:
                              if matrix[i][j]['bottom'] == False: 
                                   matrix[i][j]['bottom'] = True 
                                   score = miniMax(matrix, mod)
                                   matrix[i][j]['bottom'] = False
                         if score > bestScore: # set score
                              bestScore = score
                              if matrix[i][j]['top'] != False: bestMove = str(i+1) 
                              else: bestMove = str(i)
                              bestMove += str(j) + 'h'

                    if j < colNumber-1: # vertical clicks
                         if matrix[i][j]['left'] == False: # 1 3
                              matrix[i][j]['left'] = True 
                              if j > 0: 
                                   matrix[i][j-1]['right'] = True 
                              score = miniMax(matrix, mod)
                              matrix[i][j]['left'] = False 
                              if j > 0: matrix[i][j-1]['right'] = False 
                              if score > bestScore: # set score
                                   bestScore = score
                                   bestMove = str(i) + str(j) + 'v'
                    else:
                         if matrix[i][j]['left'] == False:
                              matrix[i][j]['left'] = True
                              matrix[i][j-1]['right'] = True 
                              score = miniMax(matrix, mod)
                              matrix[i][j]['left'] = False
                              matrix[i][j-1]['right'] = False 
                         else: 
                              if matrix[i][j]['right'] == False: 
                                   matrix[i][j]['right'] = True 
                                   score = miniMax(matrix, mod)
                                   matrix[i][j]['right'] = False 
                         if score > bestScore: # set score
                              bestScore = score
                              if matrix[i][j]['left'] != False: bestMove = str(i) + str(j+1) 
                              else: bestMove = str(i) + str(j)
                              bestMove += 'v'
     return bestMove
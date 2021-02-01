from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.

@api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
def apiOverview(request):
     parsedRequest = JSONParser().parse(request)
     i = 1
     j = 1
     side = 'v'
     print(str(request.mod))
     return Response(str(i) + str(j) + side)




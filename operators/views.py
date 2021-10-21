from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from operators.serialization import Empserialize, Sesserialize
from operators.models import Operatormodel, Operatsessionmodel
import random
import base64
import hashlib
import requests

@api_view(['POST'])
def login(request):
    userna=request.POST['id']
    passso=request.POST['hashed_password']
    access_token=str(Operatsessionmodel.objects.filter(customer_id=userna).values_list('access_token', flat=True))
    emailo=str(Operatormodel.objects.filter(pk=userna).values_list('email', flat=True))
    emailo=emailo[12:-3]
    access_token=access_token[12:-3]
    sam=emailo+'-'+passso
    message_bytes = sam.encode('ascii')
    base64_bytes = str(base64.b64encode(message_bytes))
    if(access_token and access_token==base64_bytes):
        return Response(data='Successfully logged in',status=status.HTTP_200_OK)
    return Response(data='Cannot be Authenticated',status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def logout(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def details(request):
    id=request.POST['id']
    if request.method=='POST':
        results=Operatormodel.objects.get(pk=id)
        serialize=Empserialize(results)
        return Response(serialize.data)


@api_view(['POST'])
def register(request):
    operat=Operatormodel()
    if request.method=='POST':
        serialize=Empserialize(operat,request.data)
        emailo=str(request.POST['email'])
        custo=int(request.POST['id'])
        passo=str(request.POST['hashed_password'])
        sam=emailo+'-'+passo
        message_bytes = sam.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        operator_session=Operatsessionmodel.objects.create(customer_id=custo,access_token=base64_bytes)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)



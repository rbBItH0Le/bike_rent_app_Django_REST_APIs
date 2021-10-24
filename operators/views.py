from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from operators.serialization import Empserialize, Sesserialize, Stationalize
from operators.models import Operatormodel,Operatsessionmodel,Stationmodel
from django.core import serializers
from django.http import HttpResponse
import random
import base64
import hashlib
import requests
import json


@api_view(['POST'])
def login(request):
    if request.method=='POST':
        if Operatormodel.objects.filter(email=request.POST['email']).exists()==False:
            data={}
            data['Message']='User is not registered'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        if Operatormodel.objects.get(email=request.POST['email']).session_id!=None:
            data={}
            data['Message']='Already logged in'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        passo=request.POST['hashed_password']
        passcheck=Operatormodel.objects.get(email=request.POST['email']).hashed_password
        ido=Operatormodel.objects.get(email=request.POST['email'])
        ido=ido.id
        passo_bytes = passo.encode('ascii')
        passo_bytes = base64.b64encode(passo_bytes)
        passo_bytes=str(passo_bytes)
        if(passcheck==passo_bytes):
            sam=str(request.POST['email']+request.POST['hashed_password'])
            message_bytes = sam.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            operate_session=Operatsessionmodel.objects.create(operator_id=ido,access_token=base64_bytes)
            Operatormodel.objects.filter(email=request.POST['email']).update(session_id=operate_session.id)
            data={}
            data['Message']='Logged in'
            return Response(data,status=status.HTTP_200_OK)
        data={}
        data['Message']='Wrong Password'
        return Response(data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request): 
    if request.method=='POST':
        if Operatormodel.objects.filter(email=request.POST['email']).exists()==False:
            data={}
            data['Message']="User doesn't exist"
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        if Operatsessionmodel.objects.filter(access_token=request.POST['access_token']).exists()==False:
            data={}
            data['Message']="Already Logged out"
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        access=Operatsessionmodel.objects.get(access_token=request.POST['access_token']).access_token
        print(access)
        ido=Operatormodel.objects.get(id=Operatsessionmodel.objects.get(access_token=access).operator_id).id
        print(ido)
        Operatsessionmodel.objects.get(access_token=access).delete()
        Operatormodel.objects.filter(id=ido).update(session_id=None)
        data={}
        data['Message']="Logged out"
        return Response(data,status=status.HTTP_200_OK)

@api_view(['POST'])
def details(request):
    id=request.POST['id']
    if request.method=='POST':
        results=Operatormodel.objects.get(pk=id)
        serialize=Empserialize(results)
        return Response(serialize.data)

@api_view(['POST'])
def addstation(request):
    access=request.POST['access_token']
    if request.method=='POST':
        if Operatsessionmodel.objects.filter(access_token=access).exists()==False:
            data={}
            data['Message']='Not Authorized'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        oper=Operatsessionmodel.objects.get(access_token=access).operator_id
        station=Stationmodel()
        station.operator_id=oper
        serialize=Stationalize(station,request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def showstation(request):
    if request.method=='POST':
        stations=Stationmodel.objects.all()
        serialize=Stationalize(stations,many=True)
        return Response(serialize.data,status=status.HTTP_200_OK)

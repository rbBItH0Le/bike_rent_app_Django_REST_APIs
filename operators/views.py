from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from operators.models import Cyclemodel, Errormodel
from operators.serialization import AddCycleSerializers, AddstatSerializers, Cyclenalize, Empserialize, Erroralize, LoginSerializers, Sesserialize, ShowCycleSerializers, ShowstatSerializers, Stationalize,FiltersSerializers
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
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Operatormodel.objects.get(email=request.POST['email']).session_id!=None:
            error=Errormodel.objects.get(error_code=5)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)     
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
            filters={}
            filters['response']=operate_session
            filters['status']=Errormodel.objects.get(error_code=0)
            serialize=LoginSerializers(filters)
            return Response(serialize.data,status=status.HTTP_200_OK)
        error=Errormodel.objects.get(error_code=1)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request): 
    if request.method=='POST':
        if Operatormodel.objects.filter(email=request.POST['email']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Operatsessionmodel.objects.filter(access_token=request.POST['access_token']).exists()==False:
            error=Errormodel.objects.get(error_code=6)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        access=Operatsessionmodel.objects.get(access_token=request.POST['access_token']).access_token
        print(access)
        ido=Operatormodel.objects.get(id=Operatsessionmodel.objects.get(access_token=access).operator_id).id
        print(ido)
        Operatsessionmodel.objects.get(access_token=access).delete()
        Operatormodel.objects.filter(id=ido).update(session_id=None)
        error=Errormodel.objects.get(error_code=0)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def details(request):
    id=request.POST['id']
    if request.method=='POST':
        filters={}
        results=Operatormodel.objects.get(pk=id)
        errors=Errormodel.objects.get(error_code=0)
        filters['response']=results
        filters['status']=errors
        serialize=FiltersSerializers(filters)
        return Response(serialize.data)

@api_view(['POST'])
def addstation(request):
    if request.method=='POST':
        station=Stationmodel.objects.create(capacity=request.POST['capacity'],availability=request.POST['availability'],address=request.POST['address'],post_code=request.POST['post_code'],location_lat=request.POST['location_lat'],location_long=request.POST['location_long'],serialised_plan=request.POST['serialised_plan'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=station
        filters['status']=error
        serialize=AddstatSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def showstation(request):
    if request.method=='GET':
        stations=Stationmodel.objects.all()
        filters={}
        filters['response']=stations
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=ShowstatSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def showcycle(request):
    if request.method=='GET':
        cycles=Cyclemodel.objects.all()
        filters={}
        filters['response']=cycles
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=ShowCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def addcycles(request):
    if request.method=='POST':
        cycles=Cyclemodel.objects.create(station_id=request.POST['station_id'],category=request.POST['category'],is_charging=request.POST['is_charging'],battery_percentage=request.POST['battery_percentage'],model_number=request.POST['model_number'],status_id=request.POST['status_id'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=cycles
        filters['status']=error
        serialize=AddCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deletecycle(request):
    if request.method=='DELETE':
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).delete()
        error=Errormodel.objects.get(error_code=0)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
def movecycle(request):
    if request.method=='PUT':
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(station_id=request.POST['station_id'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(category=request.POST['category'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(is_charging=request.POST['is_charging'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(battery_percentage=request.POST['battery_percentage'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(model_number=request.POST['model_number'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(status_id=request.POST['status_id'])
        results=Cyclemodel.objects.get(pk=request.POST['cycle_id'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=results
        filters['status']=error
        serialize=AddCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from cycles.models import Cyclemodel
from cycles.serialization import Cyclenalize,AddCycleSerializers,ShowCycleSerializers
from operators.serialization import Erroralize
from operators.models import Statusmodel,Stationmodel,Errormodel
from datetime import datetime
import random


@api_view(['POST'])
def details(request):
    if request.method=='POST':
        pk=request.POST['pk']
        results=Cyclemodel.objects.get(pk=pk)
        serialize=Cyclenalize(results)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def track(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['PUT'])
def repair(request):
    try:
        Cyclemodel.objects.filter(status='Damaged').update(status='Available')
    except Cyclemodel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data={}
        data["MESSAGE"]="ALL BIKES HAVE BEEN REPAIRED"
        return Response(data)
    

@api_view(['PUT'])
def move(request):
    if request.method=='PUT':
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)   
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(category=request.POST['category'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(is_charging=request.POST['is_charging'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(battery_percentage=request.POST['battery_percentage'])
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(status_id=request.POST['status_id'])
        capacity=Stationmodel.objects.get(station_id=request.POST['station_id']).capacity
        if(capacity<1):
            error=Errormodel.objects.get(error_code=9)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        Stationmodel.objects.filter(station_id=request.POST['station_id']).update(capacity=capacity-1)
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(station_id=request.POST['station_id'])
        results=Cyclemodel.objects.get(pk=request.POST['cycle_id'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=results
        filters['status']=error
        serialize=AddCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def add(request):
    if request.method=='POST':
        a=random.randint(10,20)
        b=random.randint(0,5)
        cycle_co='CZ'+'-'+str(a)+str(b)
        print(cycle_co)
        print(request.POST['station_id'])
        capacity=Stationmodel.objects.get(station_id=request.POST['station_id']).capacity
        print(capacity)
        if capacity==0:
            error=Errormodel.objects.get(error_code=9)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        Stationmodel.objects.filter(station_id=request.POST['station_id']).update(capacity=capacity-1)
        if request.POST['category'].upper()=='ELECTRIC':
            battery_percentage='0'
            is_charging='NO'
        else:
            battery_percentage='NA'
            is_charging='NA'
        cycles=Cyclemodel.objects.create(station_id=request.POST['station_id'],category=request.POST['category'],is_charging=is_charging,battery_percentage=battery_percentage,model_number=cycle_co,status_id=0)
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=cycles
        filters['status']=error
        serialize=AddCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete(request):
    if request.method=='DELETE':
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        station=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).station_id
        capacity=Stationmodel.objects.get(station_id=station).capacity
        Stationmodel.objects.filter(station_id=station).update(capacity=capacity+1)
        Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).delete()
        error=Errormodel.objects.get(error_code=0)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def show(request):
    if request.method=='GET':
        cycles=Cyclemodel.objects.all()
        filters={}
        filters['response']=cycles
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=ShowCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def repair(request):
    if request.method=='GET':
        if Cyclemodel.objects.filter(status_id=1).exists==False:
            error=Errormodel.objects.get(error_code=10)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        cycles=Cyclemodel.objects.filter(status_id=1)
        filters={}
        filters['response']=cycles
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=ShowCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from operators.models import Cyclemodel
from cycles.serialization import Cycserialize
from datetime import datetime

@api_view(['POST'])
def details(request):
    if request.method=='POST':
        pk=request.POST['pk']
        results=Cyclemodel.objects.get(pk=pk)
        serialize=Cycserialize(results)
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
    


@api_view(['POST'])
def move(request):
    id=request.POST['id']
    new_loc=request.POST['hub_id']
    results=Cyclemodel.objects.filter(pk=id).update(hub_id=new_loc)
    results=Cyclemodel.objects.get(pk=id)
    serialize=Cycserialize(results)
    return Response(serialize.data,status=status.HTTP_200_OK)
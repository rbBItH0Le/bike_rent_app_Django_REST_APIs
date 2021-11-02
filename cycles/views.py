from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from cycles.models import Cyclemodel,Activetripmodel, Tripdetailsmodel, Tripmodel
from customers.models import Customodel,Custsessionmodel
from cycles.serialization import Cyclenalize,AddCycleSerializers,ShowCycleSerializers, Showgeorializers,Renterializers
from operators.serialization import Erroralize
from customers.models import Paymentmodel
from operators.models import Statusmodel,Stationmodel,Errormodel
from datetime import datetime
import random
import time
import numpy


@api_view(['POST'])
def activetripdetails(request):
    if request.method=='POST':
        pk=request.POST['cycle_id']
        results=Activetripmodel.objects.get(cycle_id=pk)
        erroro=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=results
        filters['status']=erroro
        serialize=Renterializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def track(request):
    if request.method=='POST':
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        if Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).status_id==0 or Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).status_id==1:
            station=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).station_id
            stato=Stationmodel.objects.get(station_id=station)
            error=Errormodel.objects.get(error_code=0)
            filters={}
            filters['response']=stato
            filters['status']=error
            serialize=Showgeorializers(filters)
            return Response(serialize.data,status=status.HTTP_200_OK)
        
    

@api_view(['POST'])
def move(request):
    if request.method=='POST':
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)   
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


@api_view(['POST'])
def repairstatus(request):
    if request.method=='POST':
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(status_id=0)
        filters={}
        filters['response']=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id'])
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=AddCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def report(request):
    if request.method=='POST':
        if Customodel.objects.filter(id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Custsessionmodel.objects.filter(customer_id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=1)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).update(status_id=1)
        filters={}
        filters['response']=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id'])
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=AddCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def rent(request):
    if request.method=='POST':
        if Customodel.objects.filter(id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Custsessionmodel.objects.filter(customer_id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=1)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Cyclemodel.objects.filter(cycle_id=request.POST['cycle_id']).exists()==False:
            error=Errormodel.objects.get(error_code=3)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        custo=Customodel.objects.get(id=request.POST['id']).id
        cycl=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).cycle_id
        stato=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).station_id
        modelo=Cyclemodel.objects.get(cycle_id=request.POST['cycle_id']).model_number
        addr=Stationmodel.objects.get(station_id=stato).address
        posc=Stationmodel.objects.get(station_id=stato).post_code
        locla=Stationmodel.objects.get(station_id=stato).location_lat
        loclo=Stationmodel.objects.get(station_id=stato).location_long
        started=int(round(time.time() * 1000))
        avai=Stationmodel.objects.get(station_id=stato).availability
        avail=avai-1
        endstato=random.randint(1,6)
        if endstato==stato:
            endstato=endstato+1
        if Stationmodel.objects.filter(station_id=endstato).exists==False:
            endstato=endstato-1
        endloc=Stationmodel.objects.get(station_id=endstato).location_lat
        endlon=Stationmodel.objects.get(station_id=endstato).location_long
        coordinates=numpy.linspace([locla,loclo],[endloc,endlon],10).tolist()
        Stationmodel.objects.filter(station_id=stato).update(availability=avail)
        activa=Activetripmodel.objects.create(customer_id=custo,cycle_id=cycl,station_id=stato,address=addr,post_code=posc,location_lat=locla,location_long=loclo,started_at=started,model_number=modelo)
        vb=Activetripmodel.objects.get(cycle_id=cycl).active_trip_id
        Tripdetailsmodel.objects.create(active_trip_id=vb,cycle_id=cycl,customer_id=custo,starting_lat=locla,starting_long=loclo,ending_lat=endloc,ending_long=endlon,coordinates=coordinates)
        Cyclemodel.objects.filter(cycle_id=cycl).update(status_id=2)
        Customodel.objects.filter(id=custo).update(active_trip_id=vb)
        filters={}
        filters['response']=activa
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=Renterializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def returno(request):
    if request.method=='POST':
        if Customodel.objects.filter(id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Activetripmodel.objects.filter(customer_id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=1)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        activo=Activetripmodel.objects.get(customer_id=request.POST['id'])
        credits=Customodel.objects.get(id=activo.customer_id).credits
        ended_at=int(round(time.time() * 1000))
        started_at=activo.started_at
        Activetripmodel.objects.filter(customer_id=request.POST['id']).update(ended_at=ended_at)
        charge=ended_at-started_at
        charge=charge/3600000
        print(charge)
        print(credits)
        credits=credits-charge
        Customodel.objects.filter(id=activo.customer_id).update(credits=credits)
        Customodel.objects.filter(id=activo.customer_id).update(active_trip_id=None)
        Tripmodel.objects.create(customer_id=activo.customer_id,cycle_id=activo.cycle_id,station_id=activo.station_id,address=activo.address,post_code=activo.post_code,location_lat=activo.location_lat,location_long=activo.location_long,charge=charge,ended_at=activo.ended_at,started_at=activo.started_at,model_number=activo.model_number)
        tid=Tripmodel.objects.last().rip_id
        cid=Tripmodel.objects.last().cycle_id
        now=datetime.now()
        timo=now.strftime("%d/%m/%Y %H:%M:%S")
        a=random.randint(10,20)
        b=random.randint(0,5)
        tycle_co='TZ'+'-'+str(a)+str(b)
        Paymentmodel.objects.create(trip_id=tid,customer_id=request.POST['id'],transaction_time=timo,transaction_id=tycle_co)
        Activetripmodel.objects.get(active_trip_id=activo.active_trip_id).delete()
        Cyclemodel.objects.filter(cycle_id=cid).update(status_id=0)
        erroro=Errormodel.objects.get(error_code=11)
        serialize=Erroralize(erroro)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def showactive(request):
    if request.method=='GET':
        if Cyclemodel.objects.filter(status_id=1).exists==False:
            error=Errormodel.objects.get(error_code=10)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_404_NOT_FOUND)
        cycles=Cyclemodel.objects.filter(status_id=2)
        filters={}
        filters['response']=cycles
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=ShowCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)





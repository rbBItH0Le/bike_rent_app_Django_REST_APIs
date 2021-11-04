import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from customers.models import Customodel, Custsessionmodel, Paymentmodel
from cycles.models import Cyclemodel, Activetripmodel
from cycles.serialization import ShowCycleSerializers, Renterializers
from operators.models import Errormodel, Stationmodel
from customers.serialization import Custloginalize, Custserialize, Payerialize, Singupalize
from operators.serialization import Erroralize
import random,hashlib,base64

@api_view(['POST'])
def login(request):
    if request.method=='POST':
        if Customodel.objects.filter(email=request.POST['email']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Customodel.objects.get(email=request.POST['email']).session_id!=None:
            error=Errormodel.objects.get(error_code=5)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        passo=request.POST['hashed_password']
        passcheck=Customodel.objects.get(email=request.POST['email']).hashed_password
        ido=Customodel.objects.get(email=request.POST['email'])
        ido=ido.id
        passo_bytes = passo.encode('ascii')
        passo_bytes = base64.b64encode(passo_bytes)
        passo_bytes=str(passo_bytes)
        if(passcheck==passo_bytes):
            sam=str(request.POST['email']+request.POST['hashed_password'])
            message_bytes = sam.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            cust_session=Custsessionmodel.objects.create(customer_id=ido,access_token=base64_bytes)
            Customodel.objects.filter(email=request.POST['email']).update(session_id=cust_session.id)
            error=Errormodel.objects.get(error_code=0)
            filters={}
            filters['response']=cust_session
            filters['status']=error
            serialize=Custloginalize(filters)
            return Response(serialize.data,status=status.HTTP_200_OK)
        error=Errormodel.objects.get(error_code=8)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request):
    if request.method=='POST':
        customer_id_param=request.POST['customer_id']
        if Customodel.objects.filter(id=customer_id_param).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Custsessionmodel.objects.filter(customer_id=customer_id_param).exists()==False:
            error=Errormodel.objects.get(error_code=6)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        Custsessionmodel.objects.get(customer_id=customer_id_param).delete()
        Customodel.objects.filter(id=customer_id_param).update(session_id=None)
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=None
        filters['status']=error
        serialize=Singupalize(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        emailParam = request.POST['email']
        if Customodel.objects.filter(email=emailParam).exists():
            error=Errormodel.objects.get(error_code=7)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        hashed_password=request.POST['hashed_password']
        hashed_password_bytes = base64.b64encode(hashed_password.encode('ascii'))
        custo=Customodel.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],hashed_password=hashed_password_bytes,phone=request.POST['phone'])
        customer_id = custo.id
        accessTokenParams = str(emailParam + hashed_password)
        accessToken_bytes = base64.b64encode(accessTokenParams.encode('ascii'))
        cust_session=Custsessionmodel.objects.create(customer_id=customer_id,access_token=accessToken_bytes)
        Customodel.objects.filter(id = customer_id).update(session_id = cust_session.id)
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=Customodel.objects.get(id=customer_id)
        filters['status']=error
        serialize=Singupalize(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def details(request):
    if request.method=='POST':
        filters={}
        try:
            customerId = request.POST['customer_id']
            custo = Customodel.objects.get(id = customerId)
            error=Errormodel.objects.get(error_code=0)
            filters['response']=custo
            filters['status']=error
            serialize=Singupalize(filters)
            return Response(serialize.data,status=status.HTTP_200_OK)
        except:
            error=Errormodel.objects.get(error_code=4)
            filters['response']=None
            filters['status']=error
            serialize=Singupalize(filters)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def shownearest(request):
    if request.method=='GET':
        if Customodel.objects.filter(id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Custsessionmodel.objects.filter(customer_id=request.POST['id']).exists()==False:
            error=Errormodel.objects.get(error_code=1)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        posc=Customodel.objects.get(id=request.POST['id']).post_code
        if Stationmodel.objects.filter(post_code=posc).exists()==False:
            error=Errormodel.objects.get(error_code=12)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        station=Stationmodel.objects.get(post_code=posc).station_id
        if Cyclemodel.objects.filter(station_id=station,status_id=0).exists()==False:
            error=Errormodel.objects.get(error_code=13)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        cycles=Cyclemodel.objects.filter(station_id=station)
        filters={}
        filters['response']=cycles
        filters['status']=Errormodel.objects.get(error_code=0)
        serialize=ShowCycleSerializers(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def activetripforcustomer(request):
    if request.method=='POST':
        filters={}
        try:
            customer_id_param=request.POST['customer_id']
            active_trip=Activetripmodel.objects.get(cycle_id=customer_id_param)
            error=Errormodel.objects.get(error_code=0)
            filters['response']=active_trip
            filters['status']=error
            serialize=Renterializers(filters)
            return Response(serialize.data,status=status.HTTP_200_OK)
        except:
            error=Errormodel.objects.get(error_code=3)
            filters['response']=None
            filters['status']=error
            serialize=Renterializers(filters)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)









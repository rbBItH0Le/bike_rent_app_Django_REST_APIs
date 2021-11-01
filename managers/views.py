from cryptography import fernet
from django.db.models import base
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from cycles.models import Cyclemodel
from managers.models import Managermodel,Managessionmodel
from operators.models import Operatormodel,Errormodel
from managers.serialization import Loginalize, Managerialize, Managesignalize, Onboardanlize, Operationalize
from operators.serialization import Erroralize
from cryptography.fernet import Fernet
import base64

@api_view(['POST'])
def reports(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    key=Fernet.generate_key()
    Manager=Managermodel()
    fernet=Fernet(key)
    if request.method=='POST':
        if Managermodel.objects.filter(email=request.POST['email']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Managermodel.objects.get(email=request.POST['email']).session_id!=None:
            error=Errormodel.objects.get(error_code=5)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        passo=request.POST['hashed_password']
        passcheck=Managermodel.objects.get(email=request.POST['email']).hashed_password
        ido=Managermodel.objects.get(email=request.POST['email'])
        ido=ido.id
        passo_bytes = passo.encode('ascii')
        passo_bytes = base64.b64encode(passo_bytes)
        passo_bytes=str(passo_bytes)
        if(passcheck==passo_bytes):
            sam=str(request.POST['email']+request.POST['hashed_password'])
            message_bytes = sam.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            manage_session=Managessionmodel.objects.create(manager_id=ido,access_token=base64_bytes)
            Managermodel.objects.filter(email=request.POST['email']).update(session_id=manage_session.id)
            error=Errormodel.objects.get(error_code=0)
            filters={}
            filters['response']=manage_session
            filters['status']=error
            serialize=Loginalize(filters)
            return Response(serialize.data,status=status.HTTP_200_OK)
        error=Errormodel.objects.get(error_code=8)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request): 
    if request.method=='POST':
        if Managermodel.objects.filter(email=request.POST['email']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Managessionmodel.objects.filter(access_token=request.POST['access_token']).exists()==False:
            error=Errormodel.objects.get(error_code=6)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        access=Managessionmodel.objects.get(access_token=request.POST['access_token']).access_token
        ido=Managermodel.objects.get(id=Managessionmodel.objects.get(access_token=access).manager_id).id
        Managessionmodel.objects.get(access_token=access).delete()
        Managermodel.objects.filter(id=ido).update(session_id=None)
        error=Errormodel.objects.get(error_code=0)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_200_OK)



@api_view(['POST'])
def signup(request):     
    if request.method=='POST':
        if Managermodel.objects.filter(email=request.POST['email']).exists():
            error=Errormodel.objects.get(error_code=7)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        hashed=request.POST['hashed_password']
        message_bytes = hashed.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        manage=Managermodel.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],hashed_password=base64_bytes,phone=request.POST['phone'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=manage
        filters['status']=error
        serialize=Managesignalize(filters)
        return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def operatoronboard(request):
    if request.method=='POST':
        if Operatormodel.objects.filter(email=request.POST['email']).exists():
            error=Errormodel.objects.get(error_code=7)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        hashed=request.POST['hashed_password']
        message_bytes = hashed.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        operat=Operatormodel.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],hashed_password=base64_bytes,phone=request.POST['phone'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=operat
        filters['status']=error
        serialize=Onboardanlize(filters)
        return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def showpie(request):
    if request.method=='GET':
        available=Cyclemodel.objects.filter(status_id=0).count()
        damaged=Cyclemodel.objects.filter(status_id=1).count()
        rented=Cyclemodel.objects.filter(status_id=2).count()
        data={}
        data['response']=[available,damaged,rented]
        data['status']={"error_code": 0,"status":"HTTP_200_OK\n","error_message":None}
        return Response(data,status=status.HTTP_200_OK)






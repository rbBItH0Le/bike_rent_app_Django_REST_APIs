from cryptography import fernet
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from managers.models import Managermodel,Managessionmodel
from operators.models import Operatormodel
from managers.serialization import Managerialize, Operationalize
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
            data={}
            data['Message']='User is not registered'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        if Managermodel.objects.get(email=request.POST['email']).session_id!=None:
            data={}
            data['Message']='Already logged in'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        passo=request.POST['hashed_password']
        passcheck=Managermodel.objects.get(email=request.POST['email']).hashed_password
        ido=Managermodel.objects.get(email=request.POST['email'])
        ido=ido.id
        passo_bytes = passo.encode('ascii')
        passo_bytes = base64.b64encode(passo_bytes)
        passo_bytes=str(passo_bytes)
        if(passcheck==passo_bytes):
            Managesess=Managessionmodel()
            sam=str(request.POST['email']+request.POST['hashed_password'])
            message_bytes = sam.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            manage_session=Managessionmodel.objects.create(manager_id=ido,access_token=base64_bytes)
            Managermodel.objects.filter(email=request.POST['email']).update(session_id=manage_session.id)
            data={}
            data['Message']='Logged in'
            return Response(data,status=status.HTTP_200_OK)
        data={}
        data['Message']='Wrong Password'
        return Response(data,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout(request): 
    if request.method=='POST':
        if Managermodel.objects.filter(email=request.POST['email']).exists()==False:
            data={}
            data['Message']="User doesn't exist"
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        if Managessionmodel.objects.filter(access_token=request.POST['access_token']).exists()==False:
            data={}
            data['Message']="Already Logged out"
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        access=Managessionmodel.objects.get(access_token=request.POST['access_token']).access_token
        print(access)
        ido=Managermodel.objects.get(id=Managessionmodel.objects.get(access_token=access).manager_id).id
        print(ido)
        Managessionmodel.objects.get(access_token=access).delete()
        Managermodel.objects.filter(id=ido).update(session_id=None)
        data={}
        data['Message']="Logged out"
        return Response(data,status=status.HTTP_200_OK)



@api_view(['POST'])
def signup(request):  
    hashed=request.POST['hashed_password']
    message_bytes = hashed.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    manage=Managermodel()
    manage.hashed_password=base64_bytes   
    if request.method=='POST':
        if Managermodel.objects.filter(email=request.POST['email']).exists():
            data={}
            data['Message']='User is already created'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        serialize=Managerialize(manage,request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def operatoronboard(request):
    hashed=request.POST['hashed_password']
    message_bytes = hashed.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    operat=Operatormodel()  
    operat.hashed_password=base64_bytes  
    if request.method=='POST':
        if Operatormodel.objects.filter(email=request.POST['email']).exists():
            data={}
            data['Message']='Operator is already added'
            return Response(data,status=status.HTTP_401_UNAUTHORIZED)
        serialize=Operationalize(operat,request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_200_OK)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)






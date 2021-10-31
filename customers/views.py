import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from customers.models import Customodel, Custsessionmodel, Paymentmodel
from operators.models import Errormodel
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
        if Customodel.objects.filter(email=request.POST['email']).exists()==False:
            error=Errormodel.objects.get(error_code=4)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        if Custsessionmodel.objects.filter(access_token=request.POST['access_token']).exists()==False:
            error=Errormodel.objects.get(error_code=6)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        access=Custsessionmodel.objects.get(access_token=request.POST['access_token']).access_token
        ido=Customodel.objects.get(id=Custsessionmodel.objects.get(access_token=access).customer_id).id
        Custsessionmodel.objects.get(access_token=access).delete()
        Customodel.objects.filter(id=ido).update(session_id=None)
        error=Errormodel.objects.get(error_code=0)
        serialize=Erroralize(error)
        return Response(serialize.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        if Customodel.objects.filter(email=request.POST['email']).exists():
            error=Errormodel.objects.get(error_code=7)
            serialize=Erroralize(error)
            return Response(serialize.data,status=status.HTTP_401_UNAUTHORIZED)
        hashed=request.POST['hashed_password']
        message_bytes = hashed.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        custo=Customodel.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],hashed_password=base64_bytes,phone=request.POST['phone'],post_code=request.POST['post_code'],security_question=request.POST['security_question'],security_answer=request.POST['security_answer'],favorite_station_id=request.POST['favorite_station_id'])
        error=Errormodel.objects.get(error_code=0)
        filters={}
        filters['response']=custo
        filters['status']=error
        serialize=Singupalize(filters)
        return Response(serialize.data,status=status.HTTP_200_OK)







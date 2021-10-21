import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from customers.models import Customodel, Custsessionmodel, Paymentmodel
from customers.serialization import Custserialize, Payerialize
import random,hashlib,base64

@api_view(['POST'])
def login(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def details(request):
    custo=Customodel()
    if request.method=='POST':
        serialize=Custserialize(custo,request.data)
        emailo=str(request.POST['email'])
        custo=int(request.POST['id'])
        time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sec=str(random.randint(5000,10000))
        sam=emailo+time+sec
        message_bytes = sam.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        h = hashlib.new('ripemd160')
        h.update(base64_bytes)
        acc=h.hexdigest()
        customer_session=Custsessionmodel.objects.create(customer_id=custo,access_token=acc)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def rent(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def returns(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def report(request):
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message='Clock in server in live real time is'
    return Response(data=message+date,status=status.HTTP_200_OK)

@api_view(['POST'])
def pay(request):
    paying=Paymentmodel()
    date=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    paying.transaction_time=date
    if request.method=='POST':
        serialize=Payerialize(paying,request.data)
        data={}
        if serialize.is_valid():
            serialize.save()
            data['Message']='Payment Successful'
            return Response(data,status=status.HTTP_200_OK)
        return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)





from django.shortcuts import render,redirect
from .models import Payment
from django.db.models import Sum
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm,PaymentForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PaymentSerializer,MySerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
import base64
import json
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
# Create your views here.


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user)
        # Add custom claims
        token['username'] = user.username
        # ...
        print(token['username'])
        print(user.id)
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyUserViewset(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = PaymentSerializer
    pagination_class = None

    def get_object(self):
        request = self.request
        token = http_auth = request.META.get('HTTP_AUTHORIZATION', None)
        token = token.replace("Token ", "")
        user_json = json.loads(base64.b64decode(token.split(".")[1]))
        user_id = user_json['id']
        User = get_user_model()
        user_obj = User.objects.get(id=user_id)
        return user_obj







@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def apiOverview(request):
    api_urls ={
        'List':'/Payment-list/',
        'Detail View':'/Payment-detail/<str:pk>/',
        'Create':'/Payment-create/',
        'Update':'/Payment-update/<str:pk>/',
        'Delete':'/Payment-delete/<str:pk>/',

    }
    return Response(api_urls)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def PaymentList(request):
    #payments =Payment.objects.all().order_by('-id')
    #user_pay = payments.filter(user=request.user)
    user=request.user
    payments = user.payment_set.all().order_by('-id')
    #Payments = Payment.objects.all().order_by('-id')
    
    serializer = MySerializer(payments, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def PaymentDetail(request,pk):
    Payments = Payment.objects.get(id=pk)
    serializer = MySerializer(Payments, many=False)
    if request.user == Payments.user:
       return Response(serializer.data)
    else:
        return redirect('api-overview')
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def PaymentCreate(request):
    #################
    print(request.user.id)
    #####################
    payload ={}
    serializer = PaymentSerializer(data= {**request.data,'user':request.user.id})
    #serializer.data.user = request.user.id
    print('request',request.data)
    print('serializer',serializer)
    try:
        print(serializer.data)
    except:
        print('nu merge')
    if serializer.is_valid():
        serializer.save()
    serializer = MySerializer(request.data)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def PaymentUpdate(request,pk):
    Payments = Payment.objects.get(id=pk)
    serializer = MySerializer(instance=Payments, data = request.data)
    if request.user == Payments.user:
        if serializer.is_valid():
            serializer.save()
    else:
        return redirect('api-overview')
    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def PaymentDelete(request,pk):
    Payments = Payment.objects.get(id=pk)
    if request.user == Payments.user:
        Payments.delete()
        return Response('Item deleted')
    else:
        return redirect('api-overview')


@unauthenticated_user
def loginPage(request):
    
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('api-overview')
        else:
            messages.info(request,"Username or password are incorrect")
            return redirect('login')
    context={}
    return render(request,'base/login.html',context)

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'base/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

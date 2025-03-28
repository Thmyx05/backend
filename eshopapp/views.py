from django.shortcuts import render
from rest_framework.response import Response
from .models import Products
from .serializer import ProductsSerializer, UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

#EMAIL ------------------------------------------------------------------------------------
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

from django.views.generic import View
#----------------------------------------------------------------------------------------



#Produkty --------------------------------------------
@api_view(['GET'])
def getRoutes(request):
    return Response('Ahoj Tomasi')

@api_view(['GET', 'OPTIONS'])  # Přidán OPTIONS pro CORS preflight
def getProducts(request):
    # Pokud je to OPTIONS požadavek, vrátíme CORS hlavičky
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    try:
        # Zalogování detailů požadavku
        logger.info(f"Přijat požadavek: {request.method}")
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Origin: {request.headers.get('Origin', 'Nezjištěn')}")

        # Kontrola počtu produktů
        products = Products.objects.all()
        logger.info(f"Počet nalezených produktů: {products.count()}")

        # Serializace produktů
        serializer = ProductsSerializer(products, many=True)
        
        # Přidání CORS hlaviček do response
        response = Response(serializer.data)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response
    
    except Exception as e:
        logger.error(f"Chyba při načítání produktů: {str(e)}")
        error_response = Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        error_response['Access-Control-Allow-Origin'] = '*'
        return error_response

@api_view(['GET'])
def getProduct(request, pk):
    product=Products.objects.get(_id=pk)
    serializer=ProductsSerializer(product)
    return Response(serializer.data)

#--------------------------------------------

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user=request.user
    serializer=UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    user=User.objects.all()
    serializer=UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registerUser(request):
    data=request.data
    if User.objects.filter(username=data['email']).exists():
        return Response({"detail": "Uživatel s tímto emailem již existuje!"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create_user(
    first_name=data['fname'],
    last_name=data['lname'],
    username=data['email'],
    email=data['email'],
    password=data['password'],
    )
        serializer=UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        message={'details':e}
        print(e)
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            return render(request,"activatesuccess.html")
        else:
            return render(request,"activatefail.html")   



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer=UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        return data
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
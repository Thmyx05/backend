from eshopapp import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    path('', views.getRoutes, name='getRoutes'),
    path('produkty/', views.getProducts, name='getProducts'),
    path('produkt/<str:pk>/', views.getProduct, name='getProduct'),   
    path('uzivatele/prihlaseni/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('uzivatele/profil/',views.getUserProfile, name="getUserProfile"),
    path('uzivatele/',views.getUsers, name="getUsers"),
    path('uzivatele/registrace/', views.registerUser, name="registerUser"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
]

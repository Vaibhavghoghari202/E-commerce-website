# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('tracker/',views.tracker,name='tracker'),
    path('search/',views.search,name='search'),
    path('products/<int:myid>/', views.productView, name='productView'), 
    path('checkout/',views.checkout,name='checkout'),
    path('handlerequest/',views.handle_razorpay_request,name='handleRequest'),
    path('login/',views.login,name='login'),
    path('Registration/',views.register,name='Registration'),
            
]

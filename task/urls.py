from django.contrib import admin
from django.urls import path , include 

from urlGenerator.views import Redirector
from urlGenerator.views import ShortenLinks  
from urlGenerator.views import getIndex  

from rest_framework.routers import DefaultRouter





router = DefaultRouter()
router.register('url' ,ShortenLinks)


urlpatterns = [
   path('' , getIndex , name ="index"),
   # path('shortner' , getIndex , name ="index"),
   path('', include(router.urls)),    
   path('<str:shortener_link>/' , Redirector.as_view() , name="redirect"),

    ]

from django.http import Http404, JsonResponse
from django.shortcuts import redirect

from rest_framework.views import View ,APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView , CreateAPIView 
from rest_framework import status
from django.conf import settings


from urlGenerator.models import Link
from urlGenerator.serializer import LinkSerializers

from django.conf import settings


class ListShortenLinks(ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializers

class CreateShortenerLink(CreateAPIView):
    serializer_class = LinkSerializers


class Redirector(View):
    
    def getIdFromHash(self ,hashed_url):
        
        id = 0
        hashed_url_length = len(hashed_url)

        for i in range (hashed_url_length):
            if(ord(hashed_url[i])>= ord('a') and ord(hashed_url[i])<= ord('z')):
                index = ord(hashed_url[i]) - ord('a')
            elif(ord(hashed_url[i])>= ord('A') and ord(hashed_url[i])<= ord('Z')):
                index = ord(hashed_url[i]) - ord('A') + 26
            else:
                index = 52 + ord(hashed_url[i]) - ord('0')
            
            id += pow(62, hashed_url_length-1-i)*index
        return id

    def get(self,request,shortener_link):

        url_id =self.getIdFromHash(shortener_link) 

        
        try:
            filtered_data = Link.objects.get(pk=url_id)
        except Link.DoesNotExist:
            raise Http404("Page does not exist")


        redirect_link = filtered_data.actual_url
        filtered_data.delete()
        
        return redirect(redirect_link,)


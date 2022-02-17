from django.http import Http404, JsonResponse
from django.shortcuts import redirect,render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


from rest_framework.views import View ,APIView
from rest_framework.response import Response
from rest_framework import viewsets 
from rest_framework import status
from django.conf import settings


from urlGenerator.models import Link
from urlGenerator.serializer import LinkSerializers

from django.conf import settings

def getIndex(request):        
    
    return render(request , 'index.html')



# Responsible for create/read Only 
class ShortenLinks(viewsets.ReadOnlyModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializers

    def getLastID(self):
        if Link.objects.exists():
            id = Link.objects.last().id
        else:
            id = 0

        return id 

    def getHashValueFromId(self , id):
        row_id = id 

        # length of eligible_chars is == 62
        eligible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        hashed_url = ""
        
        # find the base 62
        # remainder can be [0-61] 
        # then we retrive the value from eligible_chars using remainder and append it to hashed_url.
        while(row_id > 0):
            remainder = row_id % 62
            hashed_url = eligible_chars[remainder] + hashed_url
            row_id //= 62

        return settings.HOST_URL+'/' + hashed_url
    
    def isValidURL(self, url_string):
        validate_url = URLValidator()

        try:
            validate_url(url_string)
        except ValidationError as e:
            try:
                validate_url("https://"+url_string)
            except ValidationError as e:
                return False

        return True

    def create(self,request,*args,**kwargs):
        link_data = request.data

        id = self.getLastID()+1
        actual_url = request.POST.get('actual_url')

        # check if given test is a valid URL
        if self.isValidURL(actual_url) is False:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        shorten_url = self.getHashValueFromId(id)

        new_link_obj = Link.objects.create(id= id  , actual_url= actual_url  ,shorten_url=shorten_url , hit_count=0)
        new_link_obj.save()
        serialize_data = LinkSerializers(new_link_obj)

        return Response(data= serialize_data.data)


# Invokes when user hit the url
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
            return render(request,'404.html')


# redirect link
        redirect_link = filtered_data.actual_url

# tracker update
        last_hit_count = filtered_data.hit_count
        filtered_data.hit_count = last_hit_count +1
        filtered_data.save()

        return redirect(redirect_link,)


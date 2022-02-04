from django.db import models
from django.conf import settings

class Link(models.Model):
    id = models.AutoField(primary_key=True)
    actual_url = models.URLField()
    shorten_url = models.URLField(blank=True, null=True)

    def getHashValueFromId(self):
        # if there is no data in DB , intialize id from 1
        # otherwise set id = last inserted id+1
        if Link.objects.exists():
            model_id = Link.objects.last().id +1
        else:
            model_id = 1

        self.id = model_id

        # length of eligible_chars is == 62
        eligible_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        hashed_url = ""
        
        # find the base 62
        # remainder can be [0-61] 
        # then we retrive the value from eligible_chars using remainder and append it to hashed_url.
        while(model_id > 0):
            remainder = model_id % 62
            hashed_url = eligible_chars[remainder] + hashed_url
            model_id //= 62

        return settings.HOST_URL+'/' + hashed_url
    

    def save(self,*args, **kwargs):
        new_link=self.getHashValueFromId()
        self.shorten_url=new_link
        return super().save(*args, **kwargs) 


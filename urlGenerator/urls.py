
from django.urls import path

from urlGenerator.views import CreateShortenerLink, ListShortenLinks  


urlpatterns = [
    path('', ListShortenLinks.as_view() , name="all_links" ),
    path('create', CreateShortenerLink.as_view() , name="create_link"),

]
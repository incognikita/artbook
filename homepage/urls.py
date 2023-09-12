from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name='homepage'),
    path('search', homepage, name='search_post')
]


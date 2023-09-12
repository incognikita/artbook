from django.urls import path
from .views import *


urlpatterns = [
    path('create-post/', create_post, name='create_post'),
    path('show-post/<slug:slug>/<int:author>/<int:pk>', show_post, name='show_post'),
]
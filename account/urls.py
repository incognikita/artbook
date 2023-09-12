from django.urls import path
from .views import *


urlpatterns = [
    path('sign-up/', sing_up, name='sign_up'),
    path('sign-in/', sign_in, name='sign_in'),
    path('sign-out/', sign_out, name='sign_out'),
    path('profile-edit/', profile_edit, name='profile_edit')
]
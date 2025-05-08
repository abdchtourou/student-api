
from os import path
from django.urls import path
from .views import signup, login, get_user_data


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('user/', get_user_data, name='user'),
]


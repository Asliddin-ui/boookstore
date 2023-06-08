from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='Index'),
    path('<int:id>/', categories, name='Category')
]
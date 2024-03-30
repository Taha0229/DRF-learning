from django.urls import path
from .views import *

urlpatterns = [
    path('', SearchListView.as_view(), name='search')
]
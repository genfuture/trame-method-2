from django.urls import path
from .views import trame_view

urlpatterns = [
    path('trame/', trame_view, name='trame_view'),
]

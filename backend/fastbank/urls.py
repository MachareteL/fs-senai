from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import *
rota = DefaultRouter()

rota.register('cliente', viewset=Cliente)

urlpatterns = []+rota.urls
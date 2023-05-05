from django.shortcuts import render
from .serializer import *
from rest_framework import viewsets


class Cliente(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    

# Create your views here.

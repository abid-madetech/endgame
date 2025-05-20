from rest_framework import viewsets
from .models import KSB
from .serializers import KSBSerializer
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class KSBViewSet(viewsets.ModelViewSet):
    queryset = KSB.objects.all()
    serializer_class = KSBSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
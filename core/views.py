from rest_framework import viewsets

from .filters import KSBFilter
from .models import KSB
from .serializers import KSBSerializer
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

def index(request):
    return render(request, 'index.html')

class KSBViewSet(viewsets.ModelViewSet):
    queryset = KSB.objects.select_related('ksb_type').all()
    serializer_class = KSBSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = KSBFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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

    @swagger_auto_schema(
        operation_description="List KSBs with optional filtering by type, name, and completion status.",
        manual_parameters=[
            openapi.Parameter(
                'type',
                openapi.IN_QUERY,
                description="Filter by KSB type (e.g. knowledge, skill, behaviour)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Filter by name (partial match, case-insensitive)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'completed',
                openapi.IN_QUERY,
                description="Filter by completion status (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
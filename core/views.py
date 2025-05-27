from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .filters import KSBFilter
from .models import KSB, KSBType
from .serializers import KSBSerializer, KSBTypeSerializer
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
import requests

def index(request):
    response = requests.get('http://localhost:8000/api/ksbs/')
    ksbs = response.json()
    return render(request, 'ksbs/index.html', {'ksbs': ksbs})

class KSBViewSet(viewsets.ModelViewSet):
    queryset = KSB.objects.select_related('ksb_type').all()
    serializer_class = KSBSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = KSBFilter
    ordering_fields = ['name', 'last_updated']

    @swagger_auto_schema(
        operation_description="List KSBs with optional filtering by type, name, and completion status.",
        manual_parameters=[
            openapi.Parameter(
                'ksb_type',
                openapi.IN_QUERY,
                description="Filter by KSB type id. see end point /api/ksb-types/ for what id stands for",
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
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description=(
                        "Order results by one or more fields. "
                        "Use commas to separate multiple fields. "
                        "Prefix with '-' for descending.\n\n"
                        "**Examples:**\n"
                        "`ordering=name` (ascending)\n"
                        "`ordering=-last_updated` (descending)\n"
                        "`ordering=name,-last_updated` (multi-sort)"
                ),
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class KSBTypeViewSet(viewsets.ModelViewSet):
    queryset = KSBType.objects.all()
    serializer_class = KSBTypeSerializer
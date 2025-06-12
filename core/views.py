from urllib.parse import urljoin
import logging
import os
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .filters import KSBFilter
from .models import KSB, KSBType, Theme
from .serializers import KSBSerializer, KSBTypeSerializer, ThemeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters as drf_filters
import requests
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

logger = logging.getLogger(__name__)
def index(request):
    # logger.warning(f"BASE_URL is: {settings.BASE_URL}")
    # ksbs = requests.get(urljoin(settings.BASE_URL, 'api/ksbs/')).json()
    # return render(request, 'ksbs/index.html', {'ksbs': ksbs})

    url = urljoin(settings.BASE_URL, 'api/ksbs/')
    logger.warning(f"Attempting request to: {url}")
    try:
        response = requests.get(url, timeout=10)
        logger.warning(f"Response status: {response.status_code}")
        ksbs = response.json()
    except Exception as e:
        logger.error(f"Failed to fetch KSBs: {e}")
        ksbs = []
    return render(request, 'ksbs/index.html', {'ksbs': ksbs})


def ksb_detail_view(request, ksb_id):
    ksb = requests.get(urljoin(settings.BASE_URL, f'api/ksbs/{ksb_id}')).json()
    return render(request, 'ksbs/view_ksb.html', {'ksb': ksb})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def create_ksb_view(request):
    if request.method == "POST":
        payload = {
            'name': request.POST['name'],
            'description': request.POST['description'],
            'ksb_type': int(request.POST['ksb_type']),
            'theme_id': int(request.POST['theme_id']) if request.POST['theme_id'] else None,
            'completed': 'completed' in request.POST,
        }

        csrf_token = request.COOKIES.get('csrftoken')
        api_url = urljoin(settings.BASE_URL, 'api/ksbs/')
        headers = {'Content-Type': 'application/json', 'X-CSRFToken': csrf_token}
        sessionid = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        cookies = {
            settings.SESSION_COOKIE_NAME: sessionid,
            'csrftoken': csrf_token
        }

        response = requests.post(api_url, json=payload, headers=headers, cookies=cookies)
        if response.status_code == 201:
            return redirect('home')
        else:
            try:
                errors = response.json()
            except ValueError:
                errors = {'error': 'Unexpected error. Try again.'}
            for field, msg in errors.items():
                messages.error(request, f"{field}: {msg}")
            ksb_types = KSBType.objects.all().values('id', 'name')
            themes = Theme.objects.all().values('id', 'name')
            return render(request, "ksbs/create_ksb.html", {'ksb_types': ksb_types, 'themes': themes})
    ksb_types = KSBType.objects.all().values('id', 'name')
    themes = Theme.objects.all().values('id', 'name')
    return render(request, "ksbs/create_ksb.html", {'ksb_types': ksb_types, 'themes': themes})


@login_required
def update_ksb_view(request, ksb_id):
    api_url = urljoin(settings.BASE_URL, f'api/ksbs/{ksb_id}/')
    ksb = requests.get(api_url).json()
    ksb_types = KSBType.objects.all().values('id', 'name')
    themes = Theme.objects.all().values('id', 'name')
    if request.method == "POST":
        payload = {
            'name': request.POST['name'],
            'description': request.POST['description'],
            'ksb_type': int(request.POST['ksb_type']),
            'theme_id': int(request.POST['theme_id']) if request.POST['theme_id'] else None,
            'completed': 'completed' in request.POST,
        }
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'Content-Type': 'application/json', 'X-CSRFToken': csrf_token}
        sessionid = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        cookies = {
            settings.SESSION_COOKIE_NAME: sessionid,
            'csrftoken': csrf_token
        }

        response = requests.patch(api_url, json=payload, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return redirect('home')
        else:
            try:
                errors = response.json()
            except ValueError:
                errors = {'error': 'Unexpected error. Try again.', 'status code': f'{response.status_code}'}
            for field, msg in errors.items():
                messages.error(request, f"{field}: {msg}")
            return render(request, "ksbs/update_ksb.html", {
                'ksb': ksb,
                'ksb_types': ksb_types,
                'themes': themes
            })

    return render(request, "ksbs/update_ksb.html", {
        'ksb': ksb,
        'ksb_types': ksb_types,
        'themes': themes
    })


@login_required
def delete_ksb(request, ksb_id):
    if request.method == 'POST':
        api_url = urljoin(settings.BASE_URL, f'api/ksbs/{ksb_id}/')
        csrf_token = request.COOKIES.get('csrftoken')
        headers = {'Content-Type': 'application/json', 'X-CSRFToken': csrf_token}
        sessionid = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        cookies = {
            settings.SESSION_COOKIE_NAME: sessionid,
            'csrftoken': csrf_token
        }

        response = requests.delete(api_url, headers=headers, cookies=cookies)

        if response.status_code == 204:
            messages.success(request, 'KSB deleted successfully.')
        else:
            messages.error(request, 'Failed to delete the KSB.')

        return redirect('home')
    return redirect('home')


class KSBViewSet(viewsets.ModelViewSet):
    queryset = KSB.objects.select_related('ksb_type', 'theme').all()
    serializer_class = KSBSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = KSBFilter
    ordering_fields = ['name', 'last_updated']
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Create a new KSB by providing required fields. Use theme_id (not nested theme).",
        request_body=KSBSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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
    permission_classes = [IsAuthenticatedOrReadOnly]


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

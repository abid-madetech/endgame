"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from core.views import (KSBViewSet, index, KSBTypeViewSet, create_ksb_view, signup_view, ThemeViewSet,
                        update_ksb_view, ksb_detail_view, delete_ksb)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'ksbs', KSBViewSet, basename='ksbs')
router.register(r'ksb-types', KSBTypeViewSet, basename='ksbtype')
router.register(r'themes', ThemeViewSet, basename='themes')

schema_view = get_schema_view(
    openapi.Info(
        title="Endgame KSB API",
        default_version="v1",
        description="API documentation with swagger UI",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('', index, name='home'),
    path('ksbs/create', create_ksb_view, name='create_ksb'),
    path('ksbs/<uuid:ksb_id>/update', update_ksb_view, name='update_ksb'),
    path('ksbs/<uuid:ksb_id>/delete', delete_ksb, name='delete_ksb'),
    path('ksbs/<uuid:ksb_id>', ksb_detail_view, name='view_ksb'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

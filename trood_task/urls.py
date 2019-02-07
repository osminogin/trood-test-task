"""trood_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import ImportViewSet, ActivityViewSet, ClientSearchViewSet


# OpenAPI schema and API documentation
schema_view = get_schema_view(
    openapi.Info(
        title='Trood Test API',
        default_version='v1',
        contact=openapi.Contact(email='oc@co.ru'),
        license=openapi.License(name='Private License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

docs_view = include_docs_urls(
    permission_classes=(permissions.AllowAny,)
)


# Default router
router = DefaultRouter()
router.register(r'import', ImportViewSet, basename='import')
router.register(r'activity', ActivityViewSet, basename='activity')
router.register(r'search', ClientSearchViewSet, basename='search')


# Urlpatterns
urlpatterns = [

    # API v1
    url(r'^$', RedirectView.as_view(url=reverse_lazy('schema-swagger-ui'))),
    url(r'^v1/', include((router.urls, 'v1'), namespace='v1')),

    # OpenAPI schema & docs
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),

    path('admin/', admin.site.urls),
]

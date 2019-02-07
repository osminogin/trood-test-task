import re
import csv
import codecs

from rest_framework import status
from django.db.models import Q
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .forms import UploadForm
from .serializers import ActivitySerializer, UserSerializer
from .models import Upload, User


class ImportViewSet(CreateModelMixin, GenericViewSet):
    """
    Importing users from CSV,
    """
    form_class = UploadForm

    def create(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Читаем CSV-файл из формы построчно и пишем в базу
            _file = form.files['file']
            csv_reader = csv.reader(codecs.iterdecode(_file, 'utf-8'))
            for row in csv_reader:
                if len(row) != 4:
                    continue
                User.objects.create(
                    first_name=row[0],
                    last_name=row[1],
                    birth_date=row[2],
                    position=row[3]
                )
            # Is all ok
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(ListModelMixin, GenericViewSet):
    """
    Shows active imports.
    """
    queryset = Upload.objects.filter(state=Upload.ACTIVE_STATE)
    serializer_class = ActivitySerializer


class ClientSearchViewSet(ListModelMixin, GenericViewSet):
    """
    Searching users by first and last names.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search_term = self.request.query_params.get('str', None)

        # Возвраем полный список, если в поиске ничего не указано
        if search_term is None:
            return qs

        # XXX: Грязновато, но там в самом задании слишком общее описание
        #   по входным параметрам на поиск и возможным вариациям, поэтому так
        if ' ' in search_term:
            first_name, last_name = re.split(r'\s+', search_term)
            qs = qs.filter(
                Q(first_name__iexact=first_name) &
                Q(last_name__iexact=last_name)
            )
        else:
            qs = qs.filter(
                Q(first_name__iexact=search_term) |
                Q(last_name__iexact=search_term)
            )
        return qs

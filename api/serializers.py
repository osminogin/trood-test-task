from rest_framework import serializers

from .models import Upload, User


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Upload
        fields = ('file_name', 'started',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

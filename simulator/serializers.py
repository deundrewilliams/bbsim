from django.conf import settings
from rest_framework import serializers
from .models import *

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'

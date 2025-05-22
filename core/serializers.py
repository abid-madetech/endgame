from rest_framework import serializers
from .models import KSB, KSBType

class KSBSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSB
        fields = '__all__'

class KSBTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSBType
        fields = '__all__'

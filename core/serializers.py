from rest_framework import serializers
from .models import KSB

class KSBSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSB
        fields = '__all__'
from rest_framework import serializers
from .models import KSB, KSBType, Theme

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'

class KSBSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSB
        fields = ['id', 'name', 'description', 'completed', 'ksb_type', 'theme', 'last_updated']

class KSBTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSBType
        fields = '__all__'

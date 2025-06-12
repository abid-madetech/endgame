from rest_framework import serializers
from .models import KSB, KSBType, Theme


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class KSBSerializer(serializers.ModelSerializer):
    theme_id = serializers.PrimaryKeyRelatedField(
        queryset=Theme.objects.all(),
        source='theme',
        write_only=True,
        required=False
    )
    theme = serializers.SerializerMethodField()

    def get_theme(self, obj):
        return obj.theme.name if obj.theme else None

    class Meta:
        model = KSB
        fields = [
            'id',
            'name',
            'description',
            'ksb_type',
            'theme_id',  # Used in POST/PUT/PATCH
            'theme',  # Just the name, read-only
            'completed',
            'last_updated'
        ]


class KSBTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KSBType
        fields = '__all__'

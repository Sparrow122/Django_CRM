from rest_framework import serializers
from .models import Record

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'
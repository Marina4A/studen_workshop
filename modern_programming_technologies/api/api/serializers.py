from rest_framework import serializers
from modern_programming_technologies.api.api.models import RepairJob

class RepairJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairJob
        fields = ['id', 'car_make', 'car_model', 'description', 'price']
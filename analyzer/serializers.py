from rest_framework import serializers
from .models import QueryLog

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()

class ActionSerializer(serializers.Serializer):
    action_code = serializers.CharField()
    display_text = serializers.CharField()

class AnalysisResponseSerializer(serializers.Serializer):
    query = serializers.CharField()
    analysis = serializers.DictField()
    suggested_actions = ActionSerializer(many=True)

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = '__all__'
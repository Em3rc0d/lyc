"""
Serializadores para la API de autómatas.
"""
from rest_framework import serializers
from .models import AutomataModel

class AutomataSerializer(serializers.ModelSerializer):
    """Serializador para el modelo AutomataModel."""
    
    automataType = serializers.CharField(source='automata_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = AutomataModel
        fields = [
            'id', 'name', 'description', 'automataType',
            'nodes', 'edges', 'createdAt', 'updatedAt'
        ]
    
    def create(self, validated_data):
        """Crea una instancia de AutomataModel."""
        automata_type = validated_data.pop('automata_type')
        return AutomataModel.objects.create(
            automata_type=automata_type,
            **validated_data
        )
    
    def update(self, instance, validated_data):
        """Actualiza una instancia de AutomataModel."""
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.automata_type = validated_data.get('automata_type', instance.automata_type)
        instance.nodes = validated_data.get('nodes', instance.nodes)
        instance.edges = validated_data.get('edges', instance.edges)
        instance.save()
        return instance


class ValidateSerializer(serializers.Serializer):
    """Serializador para la validación de cadenas."""
    
    input = serializers.CharField(required=True)
    automataType = serializers.CharField(required=True)
    automataData = serializers.JSONField(required=True)
    automataId = serializers.IntegerField(required=False)


class ConvertSerializer(serializers.Serializer):
    """Serializador para la conversión de autómatas."""
    
    nodes = serializers.JSONField(required=True)
    edges = serializers.JSONField(required=True)

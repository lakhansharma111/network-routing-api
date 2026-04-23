from rest_framework import serializers
from .models import Node, Edge, RouteHistory


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'name']


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ['id', 'source', 'destination', 'latency']

    def validate(self, data):
        if data['latency'] <= 0:
            raise serializers.ValidationError("Latency must be > 0")

        if data['source'] == data['destination']:
            raise serializers.ValidationError("Source and destination cannot be same")

        return data


class ShortestRouteSerializer(serializers.Serializer):
    source_id = serializers.IntegerField()
    destination_id = serializers.IntegerField()
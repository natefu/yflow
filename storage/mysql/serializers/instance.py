from rest_framework import serializers
from domain import Instance
from storage.mysql.models import Instance as InstanceModel

from .node import NodeSerializer


class InstanceSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    scheme = serializers.JSONField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    completed = serializers.DateTimeField(read_only=True)

    class Meta:
        model = InstanceModel
        fields = ('id', 'node', 'state', 'scheme', 'created', 'updated', 'completed')

    @staticmethod
    def to_model(instance: Instance):
        instance_dict = instance.to_dict()
        return InstanceModel(**instance_dict)

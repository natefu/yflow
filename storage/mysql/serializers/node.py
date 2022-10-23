from rest_framework import serializers
from domain import Node, NodeFlow
from storage.mysql.models import Node as NodeModel
from storage.mysql.models import NodeFlow as NodeFlowModel


class NodeSerializer(serializers.ModelSerializer):
    variables = serializers.JSONField()
    context = serializers.JSONField()
    scheme = serializers.JSONField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    completed = serializers.DateTimeField(read_only=True)

    class Meta:
        model = NodeModel
        fields = (
            'id', 'ticket', 'identifier', 'name', 'state', 'element', 'variables', 'context', 'scheme', 'condition',
            'created', 'updated', 'completed'
        )

    @staticmethod
    def to_model(node: Node):
        node_dict = node.to_dict()
        return NodeModel(**node_dict)


class NodeFlowSerializer(serializers.ModelSerializer):
    source = NodeSerializer(read_only=True)
    target = NodeSerializer(read_only=True)

    class Meta:
        model = NodeFlowModel
        fields = ('id', 'source', 'target', 'condition', 'name')

    @staticmethod
    def to_model(flow: NodeFlow):
        flow_dict = flow.to_dict()
        return NodeFlowModel(**flow_dict)

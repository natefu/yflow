from rest_framework import serializers
from domain import Ticket
from storage.mysql.models import Ticket as TicketModel
from .node import NodeSerializer


class TicketSerializer(serializers.ModelSerializer):
    scheme = serializers.JSONField()
    nodes = NodeSerializer(many=True, read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    completed = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TicketModel
        fields = ('id', 'name', 'state', 'variables', 'context', 'scheme', 'process', 'created', 'updated', 'completed')

    @staticmethod
    def to_model(ticket: Ticket):
        ticket_dict = ticket.to_dict()
        return TicketModel(**ticket_dict)

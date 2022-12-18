from rest_framework import serializers
from domain import Ticket, TicketToken
from storage.mysql.models import Ticket as TicketModel
from storage.mysql.models import TicketToken as TicketTokenModel
from .node import NodeSerializer


class TicketSerializer(serializers.ModelSerializer):
    scheme = serializers.JSONField()
    nodes = NodeSerializer(many=True, read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    completed = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TicketModel
        fields = ('id', 'name', 'state', 'variables', 'context', 'scheme', 'nodes', 'process', 'created', 'updated', 'completed')

    @staticmethod
    def to_model(ticket: Ticket):
        ticket_dict = ticket.to_dict()
        return TicketModel(**ticket_dict)


class TicketTokenSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TicketTokenModel
        fields = ('id', 'ticket', 'token', 'count', 'created', 'updated')

    @staticmethod
    def to_model(ticket_token: TicketToken):
        ticket_token_dict = ticket_token.to_dict()
        return TicketTokenModel(**ticket_token_dict)

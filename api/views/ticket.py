from constants import RUN
from domain import Ticket
from framework import generics
from engine.scheduler import ticket_scheduler
from storage.mysql.serializers import TicketSerializer
from storage.mysql import process_operator, ticket_operator
from rest_framework import status
from rest_framework.response import Response


class TicketCreateListView(generics.ListCreateAPIView):

    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        process: str = data.get('process')
        if process.isdigit():
            data['scheme'] = process_operator.get(pk=process)
        else:
            data['scheme'] = process_operator.get_by_query(name=process, deprecated=False)
        ticket = Ticket(**data)
        ticket = ticket_operator.create(ticket)
        ticket_scheduler.apply_async(
            kwargs={'ticket_id': ticket.id, 'ticket_command': RUN}
        )
        headers = self.get_success_headers(ticket)
        return Response(ticket, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = ticket_operator.query()
        a = ''
        a.isdigit()
        return Response(queryset)

from constants import FAILED, FINISHED, TERMINATED, REVOKED, CLOSED
from django.utils.timezone import now
from domain import Ticket
from storage.ticket_performer import TicketOperator
from .base_operator_mysql import BaseOperatorMysql
from .models import Ticket as TicketModel
from .serializers import TicketSerializer


class TicketMysqlOperator(TicketOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=Ticket, model=TicketModel, serializer=TicketSerializer
        )

    def create_ticket(self, ticket: Ticket) -> Ticket:
        return self.base_operator.create_object(domain=ticket, times={'created': now(), 'updated': now()})

    def update_ticket(self, pk: int, partial: bool, **updates) -> Ticket:
        if 'state' in updates and updates['state'] in [FAILED, FINISHED, TERMINATED, REVOKED, CLOSED]:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now(), 'completed': now}, **updates
            )
        else:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now()}, **updates
            )

    def get_ticket(self, pk: int) -> Ticket:
        return self.base_operator.get_object(pk=pk)

    def query_tickets(self, **query_params) -> list[Ticket]:
        return self.base_operator.query_objects(**query_params)

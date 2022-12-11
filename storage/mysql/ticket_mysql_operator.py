from constants import FAILED, FINISHED, TERMINATED, REVOKED, CLOSED
from django.utils.timezone import now
from domain import Ticket, TicketToken
from storage.ticket_performer import TicketOperator, TicketTokenOperator
from .base_operator_mysql import BaseOperatorMysql
from .models import Ticket as TicketModel
from .models import TicketToken as TicketTokenModel
from .serializers import TicketSerializer, TicketTokenSerializer


class TicketMysqlOperator(TicketOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=Ticket, model=TicketModel, serializer=TicketSerializer
        )

    def create(self, ticket: Ticket) -> Ticket:
        return self.base_operator.create_object(domain=ticket, times={'created': now(), 'updated': now()})

    def update(self, pk: int, partial: bool, **updates) -> Ticket:
        if 'state' in updates and updates['state'] in [FAILED, FINISHED, TERMINATED, REVOKED, CLOSED]:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now(), 'completed': now}, **updates
            )
        else:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now()}, **updates
            )

    def get(self, pk: int) -> Ticket:
        return self.base_operator.get_object(pk=pk)

    def query(self, **query_params) -> list[Ticket]:
        return self.base_operator.query_objects(**query_params)


class TicketTokenMysqlOperator(TicketTokenOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=TicketToken, model=TicketTokenModel, serializer=TicketTokenSerializer
        )

    def create(self, token: TicketToken) -> TicketToken:
        return self.base_operator.create_object(domain=token, times={'created': now(), 'updated': now()})

    def update(self, pk: int, partial: bool, **updates) -> TicketToken:
        return self.base_operator.update_object(
            pk=pk, partial=partial, times={'updated': now()}, **updates
        )

    def get(self, pk: int) -> TicketToken:
        return self.base_operator.get_object(pk=pk)

    def get_by_query(self, **query_params) -> TicketToken:
        return self.base_operator.get_objects_by_query(**query_params)

    def query(self, **query_params) -> list[TicketToken]:
        return self.base_operator.query_objects(**query_params)

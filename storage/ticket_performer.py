from abc import ABCMeta
from domain import Ticket


class TicketOperator(metaclass=ABCMeta):

    def create_ticket(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    def update_ticket(self, pk: int, partial: bool, **updates) -> Ticket:
        raise NotImplementedError

    def get_ticket(self, pk: int) -> Ticket:
        raise NotImplementedError

    def query_tickets(self, **query_params) -> list[Ticket]:
        raise NotImplementedError

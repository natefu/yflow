from abc import ABCMeta
from domain import Ticket, TicketToken


class TicketOperator(metaclass=ABCMeta):

    def create(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    def update(self, pk: int, partial: bool, **updates) -> Ticket:
        raise NotImplementedError

    def get(self, pk: int) -> Ticket:
        raise NotImplementedError

    def query(self, **query_params) -> list[Ticket]:
        raise NotImplementedError


class TicketTokenOperator(metaclass=ABCMeta):
    def create(self, token: TicketToken) -> TicketToken:
        raise NotImplementedError

    def update(self, pk: int, partial: bool, **updates) -> TicketToken:
        raise NotImplementedError

    def get(self, pk: int) -> TicketToken:
        raise NotImplementedError

    def get_by_query(self, **query_params) -> TicketToken:
        raise NotImplementedError

    def query(self, **query_params) -> list[TicketToken]:
        raise NotImplementedError

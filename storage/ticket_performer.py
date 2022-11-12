from abc import ABCMeta
from domain import Ticket, TicketToken


class TicketOperator(metaclass=ABCMeta):

    def create_ticket(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    def update_ticket(self, pk: int, partial: bool, **updates) -> Ticket:
        raise NotImplementedError

    def get_ticket(self, pk: int) -> Ticket:
        raise NotImplementedError

    def query_tickets(self, **query_params) -> list[Ticket]:
        raise NotImplementedError


class TicketTokenOperator(metaclass=ABCMeta):
    def create_ticket_token(self, token: TicketToken) -> TicketToken:
        raise NotImplementedError

    def update_ticket_token(self, pk: int, partial: bool, **updates) -> TicketToken:
        raise NotImplementedError

    def get_ticket_token(self, pk: int) -> TicketToken:
        raise NotImplementedError

    def get_ticket_token_by_query(self, **query_params) -> TicketToken:
        raise NotImplementedError

    def query_ticket_tokens(self, **query_params) -> list[TicketToken]:
        raise NotImplementedError

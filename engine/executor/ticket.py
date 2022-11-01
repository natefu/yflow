from engine.scheduler import SchedulerMixin
from storage.mysql import ticket_operator


class TicketExecutor(SchedulerMixin):

    def __init__(self, ticket_id):
        self.ticket = ticket_operator.get_ticket(pk=ticket_id)

    def set_state(self, state):
        ticket_operator.update_ticket(pk=self.ticket.id, partial=True, state=state)

    def get_state(self):
        return self.ticket.state

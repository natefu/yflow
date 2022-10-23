from engine.scheduler import SchedulerMixin


class TicketExecutor(SchedulerMixin):

    def __init__(self, ticket_id):
        self.ticket = ticket_id

    def set_state(self, state):
        self.ticket.state = state
        self.ticket.save()

    def get_state(self):
        return self.ticket.state

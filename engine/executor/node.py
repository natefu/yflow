from engine.scheduler import SchedulerMixin
from storage.mysql import node_operator, ticket_operator


class NodeExecutor(SchedulerMixin):

    def __init__(self, ticket_id, node_id):
        self.node = node_operator.get_node(pk=node_id)
        self.ticket = ticket_operator.get_ticket(pk=ticket_id)

    def set_state(self, state):
        node_operator.update_node(pk=self.node.id, partial=True, state=state)

    def get_state(self):
        return self.node.state

from engine.scheduler import SchedulerMixin


class NodeExecutor(SchedulerMixin):

    def __init__(self, node):
        self.node = node
        self.ticket = self.node.ticket

    def set_state(self, state):
        self.node.state = state
        self.node.save()

    def get_state(self):
        return self.node.state

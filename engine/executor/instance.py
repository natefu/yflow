from engine.scheduler import SchedulerMixin


class InstanceExecutor(SchedulerMixin):
    def __init__(self, instance):
        self.instance = instance
        self.node = self.instance.node
        self.ticket = self.node.ticket

    def set_state(self, state):
        self.instance.state = state
        self.instance.save()

    def get_state(self):
        return self.instance.state

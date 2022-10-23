from constants import INSTANCE, NODE, TICKET
from domain import Node, Ticket


class CallbackRuntime:
    def __init__(self, resource):
        self.resource = resource

    def ticket(self):
        pass

    def node(self):
        pass

    def instance(self):
        pass

    @staticmethod
    def build_callback(category, identity):
        if category == INSTANCE:
            pass
        elif category == NODE:
            return CallbackRuntime(Node.objects.get(pk=identity))
        elif category == TICKET:
            return CallbackRuntime(Ticket.objects.get(pk=identity))

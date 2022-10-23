from abc import abstractmethod, ABCMeta
from constants import READY, RUNNING, RUN, START_EVENT
from domain import Ticket, Node, NodeFlow


class TicketState(metadata=ABCMeta):

    def __init__(self, runtime):
        self.runtime = runtime

    @abstractmethod
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def terminate(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def close(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def revoke(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class TicketReadyState(TicketState):
    def run(self):
        ticket = self.runtime.ticket
        node_configs = ticket.scheme.get('nodes', {})
        flow_configs = ticket.scheme.get('flows', {})
        nodes = []
        for node_config in node_configs:
            node = Node(
                ticket=ticket, identifier=node_config.get('identifier'), name=node_config.get('name'),
                state=READY, element=node_config.get('element'), variables={}, context={}, scheme=node_config,
                condition=node_config.get('condition')
            )
            nodes.append(node)
        Node.objects.bulk_create(nodes)
        flows = []
        for flow_config in flow_configs:
            flow = NodeFlow(
                source=Node.objects.get(ticket=ticket, identifier=flow_config.get('source')),
                target=Node.objects.get(ticket=ticket, identifier=flow_config.get('target')),
                condition=flow_config.get('condition'), name=flow_config.get('name')
            )
            flows.append(flow)
        NodeFlow.objects.bulk_create(flows)
        self.runtime.executor.set_state(RUNNING)
        self.runtime.executor.dispatch_ticket()
        node = Node.objects.get(ticket=ticket, element=START_EVENT)
        self.runtime.executor.dispatch_node(ticket_id=ticket.id, node_id=node.id, command=RUN)

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass


class TicketRunningState(TicketState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass


class TicketFinishedState(TicketState):

    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass


class TicketFailedState(TicketState):

    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass


class TicketTerminatedState(TicketState):
    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass


class TicketClosedState(TicketState):

    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass


class TicketRevokedState(TicketState):

    def run(self):
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def terminate(self):
        pass

    def close(self):
        pass

    def revoke(self):
        pass

    def retry(self):
        pass
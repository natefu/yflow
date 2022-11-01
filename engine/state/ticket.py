from abc import abstractmethod, ABCMeta
from constants import (
    READY, RUNNING, RUN, START_EVENT, FINISHED, FAILED, TERMINATED, CLOSED, REVOKED, FAIL
)
from django.utils.timezone import now
from engine.runtime import TicketRuntime
from domain import Ticket, Node, NodeFlow
from storage.mysql import node_operator, node_flow_operator


class TicketState(metadata=ABCMeta):

    def __init__(self, runtime):
        self.runtime: TicketRuntime = runtime

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
        ticket: Ticket = self.runtime.executor.ticket
        node_configs = ticket.scheme.get('nodes', {})
        flow_configs = ticket.scheme.get('flows', {})
        nodes = []
        for node_config in node_configs:
            node = Node(
                ticket=ticket.id, identifier=node_config.get('identifier'), name=node_config.get('name'),
                state=READY, element=node_config.get('element'), variables={}, context={},
                scheme=node_config.get('scheme', {}), condition=node_config.get('condition', ''), created=now(),
                updated=now()
            )
            nodes.append(node)
        node_operator.batch_create_nodes(nodes=nodes)
        flows = []
        for flow_config in flow_configs:
            flow = NodeFlow(
                source=node_operator.get_node_by_query(ticket=ticket.id, identifier=flow_config.get('source')),
                target=node_operator.get_node_by_query(ticket=ticket.id, identifier=flow_config.get('target')),
                condition=flow_config.get('condition'), name=flow_config.get('name')
            )
            flows.append(flow)
        node_flow_operator.batch_create_node_flows(node_flows=flows)
        self.runtime.set_state(RUNNING)
        node = node_operator.get_node_by_query(ticket=ticket.id, element=START_EVENT)
        self.runtime.executor.dispatch_node(ticket_id=ticket.id, node_id=node.id, command=RUN)

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def terminate(self):
        self.runtime.set_state(TERMINATED)

    def close(self):
        self.runtime.set_state(CLOSED)

    def revoke(self):
        self.runtime.set_state(REVOKED)

    def retry(self):
        raise NotImplementedError


class TicketRunningState(TicketState):
    def run(self):
        raise NotImplementedError

    def complete(self):
        self.runtime.set_state(FINISHED)

    def fail(self):
        self.runtime.set_state(FAILED)

    def terminate(self):
        self.runtime.set_state(TERMINATED)

    def close(self):
        self.runtime.set_state(CLOSED)

    def revoke(self):
        self.runtime.set_state(REVOKED)

    def retry(self):
        raise NotImplementedError


class TicketFinishedState(TicketState):

    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def revoke(self):
        raise NotImplementedError

    def retry(self):
        raise NotImplementedError


class TicketFailedState(TicketState):

    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def terminate(self):
        self.runtime.set_state(TERMINATED)

    def close(self):
        self.runtime.set_state(CLOSED)

    def revoke(self):
        self.runtime.set_state(REVOKED)

    def retry(self):
        self.runtime.set_state(RUNNING)
        for node in self.runtime.ticket.nodes.filter(state=FAILED):
            self.runtime.dispatch_node(
                ticket_id=self.runtime.ticket.id, node_id=node.id, command=FAIL
            )


class TicketTerminatedState(TicketState):
    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def revoke(self):
        raise NotImplementedError

    def retry(self):
        raise NotImplementedError


class TicketClosedState(TicketState):

    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def revoke(self):
        raise NotImplementedError

    def retry(self):
        raise NotImplementedError


class TicketRevokedState(TicketState):

    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def revoke(self):
        raise NotImplementedError

    def retry(self):
        raise NotImplementedError

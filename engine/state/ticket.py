import uuid
from abc import abstractmethod, ABCMeta
from constants import (
    READY, RUNNING, RUN, START_EVENT, FINISHED, FAILED, TERMINATED, CLOSED, REVOKED, FAIL
)
from django.utils.timezone import now
from domain import Ticket, Node, NodeFlow, TicketToken
from storage.mysql import node_operator, node_flow_operator, ticket_token_operator


class TicketState:

    def __init__(self, runtime):
        from engine.runtime import TicketRuntime
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


"""
{
    "nodes": [
        {
            "identifier": "start_event",
            "name": "start_event",
            "element": "startEvent"
        },
        {
            "identifier": "review_task",
            "name": "review_task",
            "element": "review",
            "scheme": {
                "partitions": [1]
            }
        },
        {
            "identifier": "end_event",
            "name": "end_event",
            "element": "endEvent"
        }
    ],
    "flows": [
        {
            "source": "start_event",
            "target": "review_task"
        },
        {
            "source": "review_task",
            "target": "end_event"
        }
    ]
}
"""


# Before completing the ticket, needs to check if all tokens is used
class TicketReadyState(TicketState):
    def run(self):
        ticket: Ticket = self.runtime.executor.ticket
        node_configs = ticket.scheme.get('nodes', [])
        flow_configs = ticket.scheme.get('flows', [])
        token = TicketToken(None, self.runtime.executor.ticket.id, str(uuid.uuid1()), 1)
        ticket_token_operator.create(token)
        nodes = []
        for node_config in node_configs:
            node = Node(
                ticket=ticket.id, identifier=node_config.get('identifier'), name=node_config.get('name'),
                state=READY, element=node_config.get('element'), variables={}, context={},
                scheme=node_config.get('scheme', {}), condition=node_config.get('condition', ''), created=now(),
                updated=now()
            )
            nodes.append(node)
        node_operator.batch_create(nodes=nodes, times={'created': now(), 'updated': now()})
        flows = []
        for flow_config in flow_configs:
            flow = NodeFlow(
                source=node_operator.get_by_query(ticket_id=ticket.id, identifier=flow_config.get('source')).id,
                target=node_operator.get_by_query(ticket_id=ticket.id, identifier=flow_config.get('target')).id,
                condition=flow_config.get('condition', ''), name=flow_config.get('name', '')
            )
            flows.append(flow)
        node_flow_operator.batch_create(node_flows=flows)
        self.runtime.set_state(RUNNING)
        node = node_operator.get_by_query(ticket=ticket.id, element=START_EVENT)
        self.runtime.executor.dispatch_node(ticket_id=ticket.id, node_id=node.id, tokens=[token.token], command=RUN)

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

from abc import abstractmethod, ABCMeta
from constants import (
    BUILT_IN_TASK, HTTP_TASK, REVIEW_TASK, SUB_TICKET, READY, RUN, RUNNING, DENIED, FAILED, APPROVED, FINISHED,
    PENDING, SKIPPED, FINISH, FAIL, WAIT, EXCLUSIVE_GATEWAY, END_EVENT,
)
from django.utils.timezone import now
from domain import Node, Instance, Ticket
from storage.mysql import instance_operator, node_operator, ticket_operator


'''
{
    "identifier": "identifier",
    "name": "name",
    "state": "state",
    "element": "element",
    "variables": [{
        "name": "name",
        "value": "value"
    }],
    "contexts": [{
        "name": "name",
        "value": "value"
    }],
    "scheme": {
        "partitions": ["partition"],
        "config": {}
    },
    "condition": "condition"
}
'''


class NodeState:

    def __init__(self, runtime):
        self.runtime = runtime

    def run(self):
        self.runtime.set_state(RUNNING)
        state = self.runtime.executor.run()
        if state == RUNNING:
            return
        elif state == FAILED:
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
                tokens=self.runtime.executor.tokens, command=FAIL
            )
        elif state == FINISHED:
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
                tokens=self.runtime.executor.tokens, command=FINISH
            )
        elif state == WAIT:
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executornode.id,
                tokens=self.runtime.executor.tokens, command=WAIT
            )

    @abstractmethod
    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodeReadyState(NodeState):
    def run(self):
        super().run()

    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodeRunningState(NodeState):

    def _base_action(self):
        node = self.runtime.executor.node
        instances = instance_operator.query(node_id=node.id)
        total_instances = len(instances)
        running_instances = len([instance for instance in instances if instance.state == RUNNING])
        if running_instances > 0:
            return
        failed_instances = len([instance for instance in instances if instance.state in [FAILED, DENIED]])
        condition = self.runtime.executor.node.condition or 1
        state = (APPROVED, DENIED) if node.element == REVIEW_TASK else (FINISHED, FAILED)
        context = self.runtime.executor.node.context or {}
        if (total_instances - failed_instances) / total_instances >= condition:
            self.runtime.set_state(state[0])
            context[f'{self.runtime.executor.node.name}_state'] = state[0]
            node_operator.update(pk=self.runtime.executor.node.id, partial=True, context=context)
            for node in self.runtime.executor.get_next_nodes():
                self.runtime.executor.dispatch_node(
                    ticket_id=self.runtime.executor.ticket.id, node_id=node, tokens=self.runtime.executor.tokens,
                    command=RUN
                )
        else:
            self.runtime.set_state(state[1])
            context[f'{self.runtime.executor.node.name}_state'] = state[1]
            node_operator.update(pk=self.runtime.executor.node.id, partial=True, context=context)
            if state == DENIED:
                next_nodes = self.runtime.executor.get_next_nodes()
                if next_nodes:
                    for node in next_nodes:
                        self.runtime.executor.dispatch_node(
                            ticket_id=self.runtime.executor.ticket.id, node_id=node,
                            tokens=self.runtime.executor.tokens, command=RUN
                        )
                    return
            self.runtime.executor.dispatch_ticket(ticket_id=self.runtime.executor.ticket.id, command=FAIL)

    def run(self):
        super().run()
        return

    def complete(self):
        if self.runtime.executor.node.element in [REVIEW_TASK, HTTP_TASK]:
            self._base_action()
        else:
            self.runtime.set_state(FINISHED)
            if self.runtime.executor.node.element == END_EVENT:
                self.runtime.executor.dispatch_ticket(ticket_id=self.runtime.executor.ticket.id, command=FINISH)
            else:
                for node in self.runtime.executor.get_next_nodes():
                    self.runtime.executor.dispatch_node(
                        ticket_id=self.runtime.executor.ticket.id, node_id=node, tokens=self.runtime.executor.tokens,
                        command=RUN
                    )

    def fail(self):
        if self.runtime.executor.node.element in [REVIEW_TASK, HTTP_TASK]:
            self._base_action()
        else:
            self.runtime.set_state(FAILED)
            self.runtime.executor.dispatch_ticket(ticket_id=self.runtime.executor.ticket.id, command=FAIL)

    def wait(self):
        self.runtime.set_state(PENDING)

    def approved(self):
        self._base_action()

    def deny(self):
        self._base_action()

    def skip(self):
        raise NotImplementedError

    def retry(self):
        raise NotImplementedError


class NodeSkippedState(NodeState):
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodeFailedState(NodeState):
    def run(self):
        super().run()

    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        self.runtime.set_state(SKIPPED)
        for node in self.runtime.executor.get_next_nodes():
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=node, tokens=self.runtime.executor.tokens,
                command=RUN
            )

    def retry(self):
        self.runtime.set_state(READY)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
            tokens=self.runtime.executor.tokens, command=RUN
        )


class NodeApprovedState(NodeState):
    def run(self):
        super().run()

    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodeDeniedState(NodeState):
    def run(self):
        super().run()

    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        self.runtime.set_state(SKIPPED)
        for node in self.runtime.executor.get_next_nodes():
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=node, tokens=self.runtime.executor.tokens,
                command=RUN
            )

    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodePendingState(NodeState):
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        self.runtime.set_state(FINISHED)
        for node in self.runtime.executor.get_next_nodes:
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=node, tokens=self.runtime.executor.tokens,
                command=RUN
            )

    def fail(self):
        self.runtime.set_state(FAILED)
        self.runtime.executor.dispatch_ticket(
            ticket_id=self.runtime.executor.ticket.id, command=FAIL
        )

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')


class NodeFinishedState(NodeState):
    def run(self):
        super().run()

    def complete(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def fail(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def wait(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def approved(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def skip(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def retry(self):
        raise NotImplementedError('NOT IMPLEMENT')

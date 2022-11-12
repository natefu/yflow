from abc import abstractmethod, ABCMeta
from constants import (
    BUILT_IN_TASK, HTTP_TASK, REVIEW_TASK, SUB_TICKET, READY, RUN, RUNNING, DENIED, FAILED, APPROVED, FINISHED,
    PENDING, SKIPPED, FINISH
)
from django.utils.timezone import now
from engine.runtime import NodeRuntime
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


class NodeState(metadata=ABCMeta):

    def __init__(self, runtime):
        self.runtime: NodeRuntime = runtime

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
        node: Node = self.runtime.executor.node
        _, tokens = self.runtime.executor.run()
        node.variables['tokens'] = tokens
        node_operator.update_node(pk=node.id, partial=True, variables=node.variables)
        self.runtime.set_state(RUNNING)


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
        instances = instance_operator.query_instance(node_id=node.id)
        total_instances = len(instances)
        running_instances = len([instance for instance in instances if instance.state == RUNNING])
        if running_instances > 0:
            return
        failed_instances = len([instance for instance in instances if instance.state in [FAILED, DENIED]])
        condition = self.runtime.executor.node.condition
        state = (APPROVED, DENIED) if node.element == REVIEW_TASK else (FINISHED, FAILED)
        if (total_instances - failed_instances) / total_instances >= condition:
            self.runtime.set_state(state[0])
        else:
            self.runtime.set_state(state[1])
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=node.id, command=FINISH
        )

    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        self._base_action()

    def fail(self):
        self._base_action()

    def wait(self):
        self.runtime.set_state(PENDING)

    def approved(self):
        self._base_action()

    def deny(self):
        self._base_action()

    def skip(self):
        self.runtime.set_state(SKIPPED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, command=FINISH
        )

    def retry(self):
        self.runtime.set_state(READY)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, command=RUN
        )


class NodeSkippedState(NodeState):
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        for node in self.runtime.executor.get_next_nodes():
            self.runtime.executor.dispatch_node(
                ticket_id=self.runtime.executor.ticket.id, node_id=node.id, command=RUN
            )

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
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        nodes = self.runtime.executor.get_next_nodes()
        if not nodes:
            self.runtime.executor.dispatch_ticket(
                ticket_id=self.runtime.executor.ticket.id, command=DETECT
            )
        else:


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


class NodeApprovedState(NodeState):
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        pass

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
        pass

    def complete(self):
        pass

    def fail(self):
        pass

    def wait(self):
        pass

    def approved(self):
        pass

    def deny(self):
        pass

    def skip(self):
        pass

    def retry(self):
        pass


class NodePendingState(NodeState):
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        pass

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


class NodeFinishedState(NodeState):
    def run(self):
        raise NotImplementedError('NOT IMPLEMENT')

    def complete(self):
        pass

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

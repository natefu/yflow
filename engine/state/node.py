from abc import abstractmethod, ABCMeta
from constants import (
    BUILT_IN_TASK, HTTP_TASK, REVIEW_TASK, SUB_TICKET, READY, RUN, RUNNING, DENIED, FAILED, APPROVED, FINISHED,
    PENDING, SKIPPED,
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
        ticket: Ticket = self.runtime.executor.ticket
        instance_operator.delete_instances(node_id=node.id)
        if ticket.state != RUNNING:
            return
        if node.element in [BUILT_IN_TASK, SUB_TICKET, HTTP_TASK, REVIEW_TASK]:
            instances = []
            instance_scheme: dict = node.scheme
            '''
            partition 还没有想好怎么弄
            '''
            for partition in instance_scheme.get('partitions', []):
                scheme: dict = {
                    'partition': partition,
                    'element': node.element,
                    'config': instance_scheme.get('config', [])
                }
                instances.append(
                    Instance(
                        node=node.id, state=READY, scheme=scheme, created=now(), updated=now()
                    )
                )
            instance_operator.batch_create_instances(instances=instances)
            instances = instance_operator.query_instance(node=node.id)
            self.runtime.set_state(RUNNING)
            for instance in instances:
                self.runtime.executor.dispatch_instance(
                    ticket_id=node.ticket, node_id=node.id, instance_id=instance.id, command=RUN
                )

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

    def retry(self):
        self.runtime.set_state(READY)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, command=RUN
        )


class NodeSkippedState(NodeState):
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


class NodeFailedState(NodeState):
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


class NodeApprovedState(NodeState):
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


class NodeFinishedState(NodeState):
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

from abc import abstractmethod, ABCMeta
from constants import RUNNING, FAILED, FINISHED, FAIL, FINISH, APPROVED, APPROVE, DENIED, DENY
from domain import Instance, Node, Ticket
from engine.runtime import InstanceRuntime


class InstanceState(metaclass=ABCMeta):

    def __init__(self, runtime):
        self.runtime: InstanceRuntime = runtime

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
    def approve(self):
        raise NotImplementedError('NOT IMPLEMENT')

    @abstractmethod
    def deny(self):
        raise NotImplementedError('NOT IMPLEMENT')


class InstanceReadyState(InstanceState):
    def run(self):
        node: Node = self.runtime.executor.node
        ticket: Ticket = self.runtime.executor.ticket
        if ticket.state != RUNNING or node.state != RUNNING:
            return
        self.runtime.set_state(RUNNING)
        self.runtime.executor.run()

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def approve(self):
        raise NotImplementedError

    def deny(self):
        raise NotImplementedError


class InstanceRunningState(InstanceState):
    def run(self):
        pass

    def complete(self):
        self.runtime.set_state(FINISHED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
            command=FINISH
        )

    def fail(self):
        self.runtime.set_state(FAILED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
            command=FAIL
        )

    def approve(self):
        self.runtime.set_state(APPROVED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
            command=APPROVE
        )

    def deny(self):
        self.runtime.set_state(DENIED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
            command=DENY
        )


class InstanceFinishedState(InstanceState):
    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def approve(self):
        raise NotImplementedError

    def deny(self):
        raise NotImplementedError


class InstanceFailedState(InstanceState):
    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def approve(self):
        raise NotImplementedError

    def deny(self):
        raise NotImplementedError


class InstanceApprovedState(InstanceState):
    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def approve(self):
        raise NotImplementedError

    def deny(self):
        raise NotImplementedError


class InstanceDeniedState(InstanceState):
    def run(self):
        raise NotImplementedError

    def complete(self):
        raise NotImplementedError

    def fail(self):
        raise NotImplementedError

    def approve(self):
        raise NotImplementedError

    def deny(self):
        raise NotImplementedError

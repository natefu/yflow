from abc import abstractmethod, ABCMeta
from constants import RUNNING, FAILED, FINISHED, FAIL, FINISH, APPROVED, APPROVE, DENIED, DENY
from domain import Instance, Node, Ticket


class InstanceState:

    def __init__(self, runtime):
        from engine.runtime import InstanceRuntime
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
        state = self.runtime.executor.run()
        if state == FAILED:
            self.runtime.executor.dispatch_instance(
                ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
                instance_id=self.runtime.executor.instance.id, command=FAIL
            )
        elif state == FINISHED:
            self.runtime.executor.dispatch_instance(
                ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id,
                instance_id=self.runtime.executor.instance.id, command=FINISH
            )

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
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, tokens=None,
            command=FINISH
        )

    def fail(self):
        self.runtime.set_state(FAILED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, tokens=None,
            command=FAIL
        )

    def approve(self):
        self.runtime.set_state(APPROVED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, tokens=None,
            command=APPROVE
        )

    def deny(self):
        self.runtime.set_state(DENIED)
        self.runtime.executor.dispatch_node(
            ticket_id=self.runtime.executor.ticket.id, node_id=self.runtime.executor.node.id, tokens=None,
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

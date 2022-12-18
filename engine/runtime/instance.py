from constants import READY, RUNNING, FAILED, FINISHED, APPROVED, DENIED
from engine.state import (
    InstanceRunningState, InstanceFinishedState, InstanceApprovedState, InstanceFailedState, InstanceDeniedState,
    InstanceReadyState, InstanceState
)
from engine.executor import InstanceExecutor


STATE_MAPPING = {
    READY: InstanceReadyState,
    RUNNING: InstanceRunningState,
    FINISHED: InstanceFinishedState,
    FAILED: InstanceFailedState,
    APPROVED: InstanceApprovedState,
    DENIED: InstanceDeniedState,
}


class InstanceRuntime:
    def __init__(self, ticket_id, node_id, instance_id):
        self.executor = InstanceExecutor(ticket_id, node_id, instance_id)
        self.state = self.get_state()

    def run(self):
        self.state.run()

    def approve(self):
        self.state.approve()

    def deny(self):
        self.state.deny()

    def finish(self):
        self.state.complete()

    def fail(self):
        self.state.fail()

    def get_state(self) -> InstanceState:
        if self.executor.instance.state in STATE_MAPPING:
            return STATE_MAPPING[self.executor.instance.state](self)

    def set_state(self, state):
        self.executor.set_state(state)
        self.state = STATE_MAPPING[state](self)

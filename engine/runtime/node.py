from constants import READY, RUNNING, FAILED, FINISHED, APPROVED, DENIED, SKIPPED, PENDING
from engine.state import (
    NodeState, NodeFailedState, NodeDeniedState, NodeFinishedState, NodePendingState, NodeApprovedState,
    NodeRunningState, NodeSkippedState, NodeReadyState,
)


STATE_MAPPING = {
    READY: NodeReadyState,
    RUNNING: NodeRunningState,
    FAILED: NodeFailedState,
    FINISHED: NodeFinishedState,
    APPROVED: NodeApprovedState,
    DENIED: NodeDeniedState,
    SKIPPED: NodeSkippedState,
    PENDING: NodePendingState,
}


class NodeRuntime:
    def __init__(self, ticket_id, node_id):
        self.ticket = ticket_id
        self.node = node_id
        self.state = self.get_state()

    def run(self):
        self.state.run()

    def approve(self):
        self.state.approved()

    def deny(self):
        self.state.deny()

    def finish(self):
        self.state.complete()

    def skip(self):
        self.state.skip()

    def fail(self):
        self.state.fail()

    def wait(self):
        self.state.wait()

    def retry(self):
        self.state.retry()

    def get_state(self) -> NodeState:
        if self.ticket.state in STATE_MAPPING:
            return STATE_MAPPING[self.ticket.state](self)
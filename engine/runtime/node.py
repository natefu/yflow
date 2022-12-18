from constants import (
    READY, RUNNING, FAILED, FINISHED, APPROVED, DENIED, SKIPPED, PENDING, REVIEW_TASK, HTTP_TASK,
)
from engine.state import (
    NodeState, NodeFailedState, NodeDeniedState, NodeFinishedState, NodePendingState, NodeApprovedState,
    NodeRunningState, NodeSkippedState, NodeReadyState,
)
from engine.executor import NodeExecutor


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
    def __init__(self, ticket_id: int, node_id: int, tokens: list[str] = None):
        self.executor: NodeExecutor = NodeExecutor(ticket_id, node_id, tokens)
        self.state = self.get_state()

    def run(self):
        self.state.run()

    def approve(self):
        if self.executor.node.element == REVIEW_TASK:
            self.state.approved()
        else:
            raise TypeError

    def deny(self):
        if self.executor.node.element == REVIEW_TASK:
            self.state.deny()
        else:
            raise TypeError

    def finish(self):
        self.state.complete()

    def skip(self):
        if self.executor.node.element in [REVIEW_TASK, HTTP_TASK]:
            self.state.skip()
        else:
            raise TypeError

    def fail(self):
        self.state.fail()

    def wait(self):
        if self.executor.node.element == HTTP_TASK:
            self.state.wait()
        else:
            raise TypeError

    def retry(self):
        if self.executor.node.element == HTTP_TASK:
            self.state.retry()
        else:
            raise TypeError

    def get_state(self) -> NodeState:
        if self.executor.ticket.state in STATE_MAPPING:
            return STATE_MAPPING[self.executor.ticket.state](self)

    def set_state(self, state):
        self.executor.set_state(state)
        self.state = STATE_MAPPING[state](self)

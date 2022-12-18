from constants import READY, RUNNING, FAILED, FINISHED, CLOSED, TERMINATED, REVOKED
from engine.state import (
    TicketRunningState, TicketTerminatedState, TicketFinishedState, TicketClosedState, TicketRevokedState,
    TicketFailedState, TicketReadyState, TicketState,
)
from engine.executor import TicketExecutor


STATE_MAPPING = {
    READY: TicketReadyState,
    RUNNING: TicketRunningState,
    FAILED: TicketFailedState,
    FINISHED: TicketFinishedState,
    CLOSED: TicketClosedState,
    TERMINATED: TicketTerminatedState,
    REVOKED: TicketRevokedState
}


class TicketRuntime:
    def __init__(self, ticket_id):
        self.executor: TicketExecutor = TicketExecutor(ticket_id)
        self.state: TicketState = self.get_state()

    def run(self):
        self.state.run()

    def fail(self):
        self.state.fail()

    def finish(self):
        self.state.complete()

    def terminate(self):
        self.state.terminate()

    def revoke(self):
        self.state.revoke()

    def close(self):
        self.state.close()

    def get_state(self) -> TicketState:
        if self.executor.ticket.state in STATE_MAPPING:
            return STATE_MAPPING[self.executor.ticket.state](self)

    def set_state(self, state: str):
        self.executor.set_state(state)
        self.state = STATE_MAPPING[state](self)

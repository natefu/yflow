from django.utils.translation import gettext_lazy as _

# state
READY = 'ready'
RUNNING = 'running'
FINISHED = 'finished'
FAILED = 'failed'
TERMINATED = 'terminated'
CLOSED = 'closed'
REVOKED = 'revoked'
APPROVED = 'approved'
DENIED = 'denied'
SKIPPED = 'skipped'
PENDING = 'pending'

# states
TICKET_STATE_CHOICES: tuple[tuple[str, str], ...] = (
    (READY, _('I18N_MSG_STATE_READY')),
    (RUNNING, _('I18N_MSG_STATE_RUNNING')),
    (FAILED, _('I18N_MSG_STATE_FAILED')),
    (FINISHED, _('I18N_MSG_STATE_FINISHED')),
    (REVOKED, _('I18N_MSG_STATE_REVOKED')),
    (TERMINATED, _('I18N_MSG_STATE_TERMINATED')),
    (CLOSED, _('I18N_MSG_STATE_CLOSED')),
)

NODE_STATE_CHOICES: tuple[tuple[str, str], ...] = (
    (READY, _('I18N_MSG_STATE_READY')),
    (RUNNING, _('I18N_MSG_STATE_RUNNING')),
    (FAILED, _('I18N_MSG_STATE_FAILED')),
    (FINISHED, _('I18N_MSG_STATE_FINISHED')),
    (APPROVED, _('I18N_MSG_STATE_APPROVED')),
    (DENIED, _('I18N_MSG_STATE_DENIED')),
    (SKIPPED, _('I18N_MSG_STATE_SKIPPED')),
    (PENDING, _('I18N_MSG_STATE_PENDING')),
)
INSTANCE_STATE_CHOICES: tuple[tuple[str, str], ...] = (
    (READY, _('I18N_MSG_STATE_READY')),
    (RUNNING, _('I18N_MSG_STATE_RUNNING')),
    (FAILED, _('I18N_MSG_STATE_FAILED')),
    (FINISHED, _('I18N_MSG_STATE_FINISHED')),
    (APPROVED, _('I18N_MSG_STATE_APPROVED')),
    (DENIED, _('I18N_MSG_STATE_DENIED')),
)

# runtime
RUN = 'run'
APPROVE = 'approve'
DENY = 'deny'
FINISH = 'finish'
SKIP = 'skip'
FAIL = 'fail'
WAIT = 'wait'
RETRY = 'retry'
TERMINATE = 'terminate'
REVOKE = 'revoke'
CLOSE = 'close'

# http task
HTTP_INTERVAL: str = 'interval'
CONDITION: str = 'condition'

# variables config
VAR_TICKET_ID: str = 'id'
VAR_TICKET_STATE: str = 'state'
VAR_TICKET_PROCESS: str = 'process'
VAR_TICKET_APPLICANT: str = 'TICKET_APPLICANT'
VAR_TICKET_APPLICANT_NAME: str = 'TICKET_APPLICANT_NAME'
VAR_NODE_ID: str = 'id'
VAR_NODE_STATE: str = 'state'
VAR_NODE_ISSUER: str = 'issuer'
VAR_NODE_ISSUER_NAME: str = 'issuer_name'

INSTANCE_STATE_ACTION_MAP: dict = {
    APPROVED: APPROVE,
    DENIED: DENY,
    RUNNING: RUN,
    FAILED: FAIL,
    FINISHED: FINISH
}

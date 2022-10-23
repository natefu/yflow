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

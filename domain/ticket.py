from .base import Base


class Ticket(Base):
    def __init__(
            self, name, state, variables, context, scheme, process=None, created=None, updated=None, id=None,
            completed=None, **args
    ):
        self._id = id
        self._name = name
        self._state = state
        self._variables = variables
        self._context = context
        self._scheme = scheme
        self._process = process
        self._created = created
        self._updated = updated
        self._completed = completed

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: str):
        self._state = state

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables: dict):
        self._variables = variables

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context: dict):
        self._context = context

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: dict):
        self._scheme = scheme

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, process):
        self._process = process

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, created):
        self._created = created

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, updated):
        self._updated = updated

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        self._completed = completed


class TicketToken(Base):
    def __init__(self, id, ticket, token, count, created=None, updated=None, **args):
        self._id = id
        self._ticket = ticket
        self._token = token
        self._count = count
        self._created = created
        self._updated = updated

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def ticket(self):
        return self._ticket

    @ticket.setter
    def ticket(self, ticket):
        self._ticket = ticket

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, created):
        self._created = created

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, updated):
        self._updated = updated

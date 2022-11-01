from .base import Base


class Node(Base):
    def __init__(
            self, id, ticket, identifier, name, state, element, variables, context, scheme, condition, created=None,
            updated=None, completed=None, **args
    ):
        self._id = id
        self._ticket = ticket
        self._identifier = identifier
        self._name = name
        self._state = state
        self._element = element
        self._variables = variables
        self._context = context
        self._scheme = scheme
        self._condition = condition
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
    def ticket(self):
        return self._ticket

    @ticket.setter
    def ticket(self, ticket):
        self._ticket = ticket

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        self._identifier = identifier

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
    def element(self):
        return self._element

    @element.setter
    def element(self, element: str):
        self._element = element

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables: dict):
        self._variables = variables

    @property
    def context(self):
        return self._context

    @variables.setter
    def context(self, context):
        self._context = context

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: dict):
        self._scheme = scheme

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, condition: str):
        self._condition = condition

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


class NodeFlow(Base):
    def __init__(self, id, source, target, condition, name, **args):
        self._id = id
        self._source = source
        self._target = target
        self._condition = condition
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, condition: str):
        self._condition = condition

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

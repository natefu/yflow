from .base import Base
from .node import Node


class Instance(Base):
    def __init__(self, node, state, scheme, id=None, created=None, updated=None, completed=None, **args):
        self._id = id
        if isinstance(node, dict):
            self._node = Node(**node)
        else:
            self._node = node
        self._state = state
        self._scheme = scheme
        self._created = created
        self._updated = updated
        self._completed = completed

    def parse_request(self, data):
        return Instance(**data)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node = node

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: dict):
        self._scheme = scheme

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

from .base import Base


class Process(Base):
    def __init__(
            self, name, version, scheme, id=None,  deprecated=False, created=None, updated=None, **args
    ):
        self._id = id
        self._name = name
        self._version = version
        self._scheme = scheme
        self._deprecated = deprecated
        self._created = created
        self._updated = updated

    def parse_request(self, data):
        return Process(**data)

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
    def version(self):
        return self._version

    @version.setter
    def version(self, state: int):
        self._version = state

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, scheme: dict):
        self._scheme = scheme

    @property
    def deprecated(self):
        return self._deprecated

    @deprecated.setter
    def deprecated(self, deprecated: bool):
        self._deprecated = deprecated

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

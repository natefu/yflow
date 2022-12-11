from abc import ABCMeta
from domain import Instance


class InstanceOperator(metaclass=ABCMeta):

    def create(self, instance: Instance) -> Instance:
        raise NotImplementedError

    def batch_create(self, instances: list[Instance]):
        raise NotImplementedError

    def update(self, pk: int, partial: bool, **updates) -> Instance:
        raise NotImplementedError

    def get(self, pk: int) -> Instance:
        raise NotImplementedError

    def query(self, **query_params) -> list[Instance]:
        raise NotImplementedError

    def delete(self, **query_params):
        raise NotImplementedError

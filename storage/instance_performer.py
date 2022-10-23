from abc import ABCMeta
from domain import Instance


class InstanceOperator(metaclass=ABCMeta):

    def create_instance(self, instance: Instance) -> Instance:
        raise NotImplementedError

    def update_instance(self, pk: int, partial: bool, **updates) -> Instance:
        raise NotImplementedError

    def get_instance(self, pk: int) -> Instance:
        raise NotImplementedError

    def query_instance(self, **query_params) -> list[Instance]:
        raise NotImplementedError

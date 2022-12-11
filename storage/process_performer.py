from abc import ABCMeta
from domain import Process


class ProcessOperator(metaclass=ABCMeta):

    def create(self, process: Process) -> Process:
        raise NotImplementedError

    def update(self, pk: int, partial: bool,  **updates) -> Process:
        raise NotImplementedError

    def get(self, pk: int) -> Process:
        raise NotImplementedError

    def get_by_query(self, **query_params) -> Process:
        raise NotImplementedError

    def query(self, **query_params) -> list[Process]:
        raise NotImplementedError

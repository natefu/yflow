from abc import ABCMeta
from domain import Process


class ProcessOperator(metaclass=ABCMeta):

    def create_process(self, process: Process) -> Process:
        raise NotImplementedError

    def update_process(self, pk: int, partial: bool,  **updates) -> Process:
        raise NotImplementedError

    def get_process(self, pk: int) -> Process:
        raise NotImplementedError

    def query_processes(self, **query_params) -> list[Process]:
        raise NotImplementedError

from domain import Instance
from storage.instance_performer import InstanceOperator


class InstanceRedisOperator(InstanceOperator):
    def create(self, instance: Instance) -> Instance:
        pass

    def batch_create(self, instances: list[Instance]):
        pass

    def update(self, pk: int, partial: bool, **updates) -> Instance:
        pass

    def get(self, pk: int) -> Instance:
        pass

    def query(self, **query_params) -> list[Instance]:
        pass

    def delete(self, **query_params):
        pass
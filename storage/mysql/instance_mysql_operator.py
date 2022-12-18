from constants import FAILED, FINISHED, APPROVED, DENIED
from django.utils.timezone import now
from domain import Instance
from storage.instance_performer import InstanceOperator
from .base_operator_mysql import BaseOperatorMysql
from .models import Instance as InstanceModel
from .serializers import InstanceSerializer


class InstanceMysqlOperator(InstanceOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=Instance, model=InstanceModel, serializer=InstanceSerializer
        )

    def create(self, instance: Instance) -> Instance:
        return self.base_operator.create_object(domain=instance, times={'created': now(), 'updated': now()})

    def batch_create(self, instances: list[Instance]):
        return self.base_operator.batch_create_objects(domains=instances)

    def update(self, pk: int, partial: bool, **updates) -> Instance:
        if 'state' in updates and updates['state'] in [FAILED, FINISHED, APPROVED, DENIED]:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now(), 'completed': now()}, **updates
            )
        else:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now()}, **updates
            )

    def get(self, pk: int) -> Instance:
        return self.base_operator.get_object(pk=pk)

    def query(self, **query_params) -> list[Instance]:
        return self.base_operator.query_objects(**query_params)

    def delete(self, **query_params):
        return self.base_operator.delete_objects(**query_params)

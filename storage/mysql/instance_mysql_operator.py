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

    def create_instance(self, instance: Instance) -> Instance:
        return self.base_operator.create_object(domain=instance, times={'created': now(), 'updated': now()})

    def update_instance(self, pk: int, partial: bool, **updates) -> Instance:
        if 'state' in updates and updates['state'] in [FAILED, FINISHED, APPROVED, DENIED]:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now(), 'completed': now}, **updates
            )
        else:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now()}, **updates
            )

    def get_instance(self, pk: int) -> Instance:
        return self.base_operator.get_object(pk=pk)

    def query_instance(self, **query_params) -> list[Instance]:
        return self.base_operator.query_objects(**query_params)

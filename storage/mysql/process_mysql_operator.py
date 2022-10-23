from django.utils.timezone import now
from domain import Process
from storage.process_performer import ProcessOperator
from .base_operator_mysql import BaseOperatorMysql
from .models import Process as ProcessModel
from .serializers import ProcessSerializer


class ProcessMysqlOperator(ProcessOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=Process, model=ProcessModel, serializer=ProcessSerializer
        )

    def create_process(self, process: Process) -> Process:
        return self.base_operator.create_object(domain=process, times={'created': now(), 'updated': now()})

    def update_process(self, pk: int, partial: bool, **updates) -> Process:
        return self.base_operator.update_object(
            pk=pk, partial=partial, times={'updated': now()}, **updates
        )

    def get_process(self, pk: int) -> Process:
        return self.base_operator.get_object(pk=pk)

    def query_processes(self, **query_params) -> list[Process]:
        return self.base_operator.query_objects(**query_params)

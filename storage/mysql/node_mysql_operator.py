from constants import APPROVED, DENIED, FAILED, FINISHED, SKIPPED
from django.utils.timezone import now
from domain import Node, NodeFlow
from storage.node_performer import NodeOperator, NodeFlowOperator
from .base_operator_mysql import BaseOperatorMysql
from .models import Node as NodeModel
from .models import NodeFlow as NodeFlowModel
from .serializers import NodeSerializer, NodeFlowSerializer


class NodeMysqlOperator(NodeOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=Node, model=NodeModel, serializer=NodeSerializer
        )

    def create_node(self, node: Node) -> Node:
        return self.base_operator.create_object(domain=node, times={'created': now(), 'updated': now()})

    def batch_create_nodes(self, nodes: list[Node]) -> None:
        self.base_operator.batch_create_objects(domains=nodes)

    def update_node(self, pk: int, partial: bool, **updates) -> Node:
        if 'state' in updates and updates['state'] in [APPROVED, DENIED, FAILED, FINISHED, SKIPPED]:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now(), 'completed': now}, **updates
            )
        else:
            return self.base_operator.update_object(
                pk=pk, partial=partial, times={'updated': now()}, **updates
            )

    def get_node(self, pk: int) -> Node:
        return self.base_operator.get_object(pk=pk)

    def get_node_by_query(self, **query_params) -> Node:
        return self.base_operator.get_objects_by_query(**query_params)

    def query_nodes(self, **query_params) -> list[Node]:
        return self.base_operator.query_objects(**query_params)


class NodeFlowMysqlOperator(NodeFlowOperator):

    def __init__(self):
        self.base_operator = BaseOperatorMysql(
            domain=NodeFlow, model=NodeFlowModel, serializer=NodeFlowSerializer
        )

    def create_node_flow(self, node_flow: NodeFlow) -> NodeFlow:
        return self.base_operator.create_object(domain=node_flow)

    def batch_create_node_flows(self, node_flows: list[NodeFlow]):
        return self.base_operator.batch_create_objects(domains=node_flows)

    def get_node_flow(self, pk: int) -> NodeFlow:
        return self.base_operator.get_object(pk=pk)

    def query_node_flows(self, **query_params) -> list[NodeFlow]:
        return self.base_operator.query_objects(**query_params)

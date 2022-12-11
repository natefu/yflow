from abc import ABCMeta
from domain import Node, NodeFlow


class NodeOperator(metaclass=ABCMeta):

    def create(self, node: Node) -> Node:
        raise NotImplementedError

    def batch_create(self, nodes: list[Node]) -> None:
        raise NotImplementedError

    def update(self, pk: int, partial: bool, **updates) -> Node:
        raise NotImplementedError

    def get(self, pk: int) -> Node:
        raise NotImplementedError

    def get_by_query(self, **query_params) -> Node:
        raise NotImplementedError

    def query(self, **query_params) -> list[Node]:
        raise NotImplementedError


class NodeFlowOperator(metaclass=ABCMeta):

    def create(self, node_flow: NodeFlow) -> NodeFlow:
        raise NotImplementedError

    def batch_create(self, node_flows: list[NodeFlow]):
        raise NotImplementedError

    def get(self, pk: int) -> NodeFlow:
        raise NotImplementedError

    def query(self, **query_params) -> list[NodeFlow]:
        raise NotImplementedError

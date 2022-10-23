from abc import ABCMeta
from domain import Node, NodeFlow


class NodeOperator(metaclass=ABCMeta):

    def create_node(self, node: Node) -> Node:
        raise NotImplementedError

    def update_node(self, pk: int, partial: bool, **updates) -> Node:
        raise NotImplementedError

    def get_node(self, pk: int) -> Node:
        raise NotImplementedError

    def query_nodes(self, **query_params) -> list[Node]:
        raise NotImplementedError


class NodeFlowOperator(metaclass=ABCMeta):

    def create_node_flow(self, node_flow: NodeFlow) -> NodeFlow:
        raise NotImplementedError

    def get_node_flow(self, pk: int) -> NodeFlow:
        raise NotImplementedError

    def query_node_flows(self, **query_params) -> list[NodeFlow]:
        raise NotImplementedError

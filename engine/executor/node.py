import uuid
from constants import (
    FAILED, DENIED, APPROVED, FINISHED, SKIPPED, EXCLUSIVE_GATEWAY, START_EVENT, HTTP_TASK, REVIEW_TASK, SUB_TICKET,
    INCLUSIVE_DIVERGING_GATEWAY, PARALLEL_DIVERGING_GATEWAY, INCLUSIVE_CONVERGING_GATEWAY, RUNNING, READY, RUN,
    PARALLEL_CONVERGING_OR_GATEWAY, PARALLEL_CONVERGING_AND_GATEWAY, END_EVENT,
)
from django.utils.timezone import now
from domain import Node, NodeFlow, TicketToken, Instance
from engine.scheduler import SchedulerMixin
from storage.mysql import (
    node_operator, ticket_operator, node_flow_operator, ticket_token_operator, instance_operator
)
from utils.engine import is_qualified


class NodeExecutor(SchedulerMixin):

    def __init__(self, ticket_id: int, node_id: int, tokens: list[str] = None):
        self.node = node_operator.get(pk=node_id)
        self.ticket = ticket_operator.get(pk=ticket_id)
        if tokens:
            self.update_tokens(tokens)
        else:
            self.tokens = self.node.context.get('tokens')

    def set_state(self, state):
        self.node = node_operator.update(pk=self.node.id, partial=True, state=state)

    def get_state(self) -> str:
        return self.node.state

    def update_tokens(self, tokens: list[str]):
        self.tokens = tokens
        self.node.context['tokens'] = tokens
        node_operator.update(pk=self.node.id, partial=True, context=self.node.context)

    def run(self) -> str:
        state, token = self.get_executor().run()
        self.update_tokens(tokens=token)
        return state

    def get_next_nodes(self) -> list[int]:
        return self.get_executor().get_next_nodes()

    def set_ticket_state(self, state):
        ticket_operator.update(pk=self.ticket.id, partial=True, state=state)

    def get_ticket_state(self) -> str:

        """
        工单状态 ready，running，finished，terminated，closed，failed
        RUNNING: 当工单节点 !(failed不在parallel和or之间)，(节点不可以正常往下流转)
        FINISHED: 当运行到END
        TERMINATED: 当节点无法运行下去
        CLOSED: 当用户手动关闭工单
        FAILED: 当失败节点不在parallel和or之间


        1. 当工单节点有failed，并且未来存在or网关，并且其他通路还在正常运行，则工单状态不变
        2. 若工单正在running，并且节点状态，则状态不变
        """

        if node_operator.get_by_query(ticket_id=self.ticket.id, state__in=[FAILED]):
            return FAILED
        return RUNNING

    def get_executor(self):
        if self.node.element == START_EVENT:
            return StartNodeExecutor(self)
        elif self.node.element == END_EVENT:
            return EndNodeExecutor(self)
        elif self.node.element == HTTP_TASK:
            return HttpNodeExecutor(self)
        elif self.node.element == REVIEW_TASK:
            return ReviewNodeExecutor(self)
        elif self.node.element == PARALLEL_DIVERGING_GATEWAY:
            return ParallelGatewayNodeExecutor(self)
        elif self.node.element == EXCLUSIVE_GATEWAY:
            return ExclusiveGatewayNodeExecutor(self)
        elif self.node.element == INCLUSIVE_DIVERGING_GATEWAY:
            return InclusiveDivergingGatewayNodeExecutor(self)
        elif self.node.element == PARALLEL_CONVERGING_AND_GATEWAY:
            return AndConvergingGatewayNodeExecutor(self)
        elif self.node.element == PARALLEL_CONVERGING_OR_GATEWAY:
            return OrConvergingGatewayNodeExecutor(self)
        elif self.node.element == INCLUSIVE_CONVERGING_GATEWAY:
            return InclusiveConvergingGatewayNodeExecutor(self)


class BaseNodeExecutor:

    def __init__(self, executor: NodeExecutor):
        self.executor = executor

    def run(self):
        pass

    def get_next_nodes(self):
        node_flows: list[NodeFlow] = node_flow_operator.query(source_id=self.executor.node.id)
        return [node_flow.target for node_flow in node_flows]

    def get_ticket_token(self):
        token = self.executor.tokens[-1]
        return ticket_token_operator.get_by_query(ticket_id=self.executor.node.ticket, token=token)


class HttpNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        instance_operator.delete(node_id=self.executor.node.id)
        instances = []
        instance_scheme: dict = self.executor.node.scheme
        for partition in instance_scheme.get('partitions', []):
            scheme: dict = {
                'partition': partition,
                'element': self.executor.node.element,
                'config': instance_scheme.get('config', [])
            }
            instances.append(
                Instance(id=None, node=self.executor.node.id, state=READY, scheme=scheme, created=now(), updated=now())
            )
        instance_operator.batch_create(instances=instances)
        instances = instance_operator.query(node=self.executor.node.id)
        for instance in instances:
            self.executor.dispatch_instance(
                ticket_id=self.executor.node.ticket, node_id=self.executor.node.id, instance_id=instance.id, command=RUN
            )
        return RUNNING, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        if len(nodes) != 1:
            return
        return nodes


class ReviewNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        instance_operator.delete(node_id=self.executor.node.id)
        instances = []
        instance_scheme: dict = self.executor.node.scheme
        for partition in instance_scheme.get('partitions', []):
            scheme: dict = {
                'partition': partition,
                'element': self.executor.node.element,
                'config': instance_scheme.get('config', [])
            }
            instances.append(
                Instance(node=self.executor.node.id, state=READY, scheme=scheme, created=now(), updated=now())
            )
        instance_operator.batch_create(instances=instances)
        instances = instance_operator.query(node=self.executor.node.id)
        for instance in instances:
            self.executor.dispatch_instance(
                ticket_id=self.executor.node.ticket, node_id=self.executor.node.id, instance_id=instance.id, command=RUN
            )
        return RUNNING, self.executor.tokens

    def get_next_nodes(self):
        node_ids = super().get_next_nodes()
        if len(node_ids) != 1:
            return
        node_id = node_ids[0]
        node = node_operator.get(pk=node_id)
        if node.element == EXCLUSIVE_GATEWAY:
            return node_ids
        elif self.executor.node.state == APPROVED:
            return node_ids


class SubTicketNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        return RUNNING, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        if len(nodes) != 1:
            return
        return nodes


class StartNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        return FINISHED, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        if len(nodes) != 1:
            return
        return nodes


class EndNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        if len(self.executor.tokens) == 1:
            ticket_token = ticket_token_operator.get_by_query(
                ticket_id=self.executor.ticket.id, token=self.executor.tokens[0]
            )
            ticket_token.count -= 1
            ticket_token_operator.update(pk=ticket_token.id, partial=True, count=ticket_token.count)
            if ticket_token.count == 0:
                return FINISHED, []
            else:
                return FAILED, [ticket_token.token]
        else:
            return FAILED, self.executor.tokens

    def get_next_nodes(self):
        return []


class ParallelGatewayNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        token = TicketToken(None, self.executor.node.ticket, str(uuid.uuid1()), 0)
        ticket_token_operator.create(token)
        self.executor.tokens.append(token.token)
        return FINISHED, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        token = ticket_token_operator.get_by_query(
            ticket_id=self.executor.node.ticket, token=self.executor.tokens[-1]
        )
        for _ in nodes:
            token.count += 1
        ticket_token_operator.update(pk=token.id, partial=True, count=token.count)
        return nodes


class ExclusiveGatewayNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        return FINISHED, self.executor.tokens

    def get_next_nodes(self):
        flows: list[NodeFlow] = node_flow_operator.query(source_id=self.executor.node.id)
        for flow in flows:
            if is_qualified(self.executor.node, flow.condition):
                return [flow.target]
        return []


class InclusiveDivergingGatewayNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        token = TicketToken(None, self.executor.node.ticket, str(uuid.uuid1()), 0)
        ticket_token_operator.create(token)
        self.executor.tokens.append(token.token)
        return FINISHED, self.executor.tokens

    def get_next_nodes(self):
        flows: list[NodeFlow] = node_flow_operator.query(source_id=self.executor.node.id)
        next_nodes = []
        token = ticket_token_operator.get_by_query(
            ticket_id=self.executor.node.ticket, token=self.executor.tokens[-1]
        )
        for flow in flows:
            if is_qualified(self.executor.node, flow.condition):
                token.count += 1
                next_nodes.append(flow.target)
        ticket_token_operator.update(pk=token.id, partial=True, count=token.count)
        return next_nodes


class AndConvergingGatewayNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        ticket_token = self.get_ticket_token()
        ticket_token.count -= 1
        ticket_token_operator.update(pk=ticket_token.id, partial=True, count=ticket_token.count)
        if ticket_token.count == 0:
            self.executor.tokens.pop()
            return FINISHED, self.executor.tokens
        else:
            return RUNNING, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        if len(nodes) != 1:
            return
        return nodes


class OrConvergingGatewayNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        ticket_token = self.get_ticket_token()
        ticket_token.count = 0
        ticket_token_operator.update(pk=ticket_token.id, partial=True, count=0)
        self.executor.tokens.pop()
        return FINISHED, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        if len(nodes) != 1:
            return
        return nodes


class InclusiveConvergingGatewayNodeExecutor(BaseNodeExecutor):
    def __init__(self, executor: NodeExecutor):
        super().__init__(executor)

    def run(self):
        ticket_token = self.get_ticket_token()
        ticket_token.count -= 1
        ticket_token_operator.update(pk=ticket_token.id, partial=True, count=ticket_token.count)
        if ticket_token.count == 0:
            self.executor.tokens.pop()
            return FINISHED, self.executor.tokens
        else:
            return RUNNING, self.executor.tokens

    def get_next_nodes(self):
        nodes = super().get_next_nodes()
        if len(nodes) != 1:
            return
        return nodes

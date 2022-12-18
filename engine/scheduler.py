import logging

from abc import ABC
from celery import Task
from constants import TICKET, NODE, INSTANCE
from yflow import celery_app

logger = logging.getLogger('engine')


class Scheduler(Task, ABC):
    def before_start(self, task_id, args, kwargs):
        logger.debug(f'before start: {task_id=}, {args=}, {kwargs=}')

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.debug(f'after return: {status=}, {retval=}, {task_id=}, {args=}, {kwargs=}, {einfo=}')


class TicketScheduler(Scheduler):
    name = 'TicketScheduler'

    def run(self, ticket_id: int, ticket_command: str):
        from engine.runtime import TicketRuntime
        runtime = TicketRuntime(ticket_id=ticket_id)
        try:
            handler = getattr(runtime, ticket_command)
            return handler()
        except AttributeError as e:
            raise


class TicketCallbackScheduler(Scheduler):
    name = 'TicketCallbackScheduler'

    def run(self, ticket_id: int, ticket_command: str):
        from engine.runtime import CallbackRuntime
        runtime = CallbackRuntime.build_callback(category=TICKET, identity=ticket_id)
        try:
            handler = getattr(runtime, ticket_command)
            return handler()
        except AttributeError as e:
            raise


class NodeScheduler(Scheduler):
    name = 'NodeScheduler'

    def run(self, ticket_id: int, node_id: int, tokens: list[str], node_command: str):
        from engine.runtime import NodeRuntime
        runtime = NodeRuntime(ticket_id=ticket_id, node_id=node_id, tokens=tokens)
        try:
            handler = getattr(runtime, node_command)
            return handler()
        except AttributeError as e:
            raise


class NodeCallbackScheduler(Scheduler):
    name = 'NodeCallbackScheduler'

    def run(self, node_id: int, node_command: str):
        from engine.runtime import CallbackRuntime
        runtime = CallbackRuntime.build_callback(category=NODE, identity=node_id)
        try:
            handler = getattr(runtime, node_command)
            return handler()
        except AttributeError as e:
            raise


class InstanceScheduler(Scheduler):
    name = 'InstanceScheduler'

    def run(self, ticket_id: int, node_id: int, instance_id: int, instance_command: str):
        from engine.runtime import InstanceRuntime
        runtime = InstanceRuntime(ticket_id=ticket_id, node_id=node_id, instance_id=instance_id)
        try:
            handler = getattr(runtime, instance_command)
            return handler()
        except AttributeError as e:
            raise


class InstanceCallbackScheduler(Scheduler):
    name = 'InstanceCallbackScheduler'

    def run(self, instance_id: int, instance_command: str):
        from engine.runtime import CallbackRuntime
        runtime = CallbackRuntime.build_callback(category=INSTANCE, identity=instance_id)
        try:
            handler = getattr(runtime, instance_command)
            return handler()
        except AttributeError as e:
            raise


class SchedulerMixin:
    def dispatch_instance(self, ticket_id: int, node_id: int, instance_id: int, command: str) -> None:
        instance_scheduler.apply_async(
            kwargs={'ticket_id': ticket_id, 'node_id': node_id, 'instance_id': instance_id, 'instance_command': command}
        )

    def dispatch_instance_callback(self, instance_id: int, command: str) -> None:
        instance_callback.apply_async(
            kwargs={'instance_id': instance_id, 'instance_command': command}
        )

    def dispatch_node(self, ticket_id: int, node_id: int, tokens: list[str], command: str) -> None:
        node_scheduler.apply_async(
            kwargs={'ticket_id': ticket_id, 'node_id': node_id, 'tokens': tokens, 'node_command': command}
        )

    def dispatch_node_callback(self, node_id: int, command: str) -> None:
        node_callback.apply_async(
            kwargs={'node_id': node_id, 'node_command': command}
        )

    def dispatch_ticket(self, ticket_id: int, command: str) -> None:
        ticket_scheduler.apply_async(
            kwargs={'ticket_id': ticket_id, 'ticket_command': command}
        )

    def dispatch_ticket_callback(self, ticket_id: int, command: str) -> None:
        ticket_callback.apply_async(
            kwargs={'ticket_id': ticket_id, 'ticket_command': command}
        )


instance_callback = celery_app.register_task(InstanceCallbackScheduler())
instance_scheduler = celery_app.register_task(InstanceScheduler())
node_callback = celery_app.register_task(NodeCallbackScheduler())
node_scheduler = celery_app.register_task(NodeScheduler())
ticket_callback = celery_app.register_task(TicketCallbackScheduler())
ticket_scheduler = celery_app.register_task(TicketScheduler())

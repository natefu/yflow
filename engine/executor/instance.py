import json
import time

from client.http.implement.simple_client import HttpClient
from constants import (
    FINISHED, FAILED, HTTP_INTERVAL, CONDITION, HTTP_DEFAULT_MAX_RETRY_INTERVAL, HTTP_DEFAULT_RETRY_ATTEMPTS,
    HTTP_DEFAULT_MIN_RETRY_INTERVAL, HTTP_TASK, BUILT_IN_TASK, REVIEW_TASK, SUB_TICKET, RUNNING,
    INSTANCE_STATE_ACTION_MAP,
)
from domain import Instance
from engine.scheduler import SchedulerMixin
from storage.mysql import instance_operator, node_operator, ticket_operator
from utils import is_qualified, build_ticket_variables, build_node_variables


class InstanceExecutor(SchedulerMixin):
    def __init__(self, ticket_id, node_id, instance_id):
        self.instance = instance_operator.get(pk=instance_id)
        self.node = node_operator.get(pk=node_id)
        self.ticket = ticket_operator.get(pk=ticket_id)

    def set_state(self, state):
        instance_operator.update(pk=self.instance.id, partial=True, state=state)

    def get_state(self):
        return self.instance.state

    def run(self):
        parameters: dict = build_node_variables(node=self.node, ticket=self.ticket)
        scheme: dict = self.instance.scheme
        executor = ActivityExecutor(parameters=parameters, scheme=scheme)
        state = executor.run()
        self.dispatch_instance(
            ticket_id=self.ticket.id, node_id=self.node.id, instance_id=self.instance.id,
            command=INSTANCE_STATE_ACTION_MAP[state]
        )


class HttpExecutor:
    def __init__(self, parameters: dict, config: dict):
        self.config: dict = {
            'method': config.get('method'),
            'url': config.get('url'),
            'headers': config.get('headers', None),
            'timeout': config.get('timeout', None),
            'form_urlencoded': config.get('form_urlencoded', False),
            'max_retry_attempts': config.get('max_retry_attempts', HTTP_DEFAULT_RETRY_ATTEMPTS),
            'min_retry_interval': config.get('min_retry_interval', HTTP_DEFAULT_MIN_RETRY_INTERVAL),
            'max_retry_interval': config.get('max_retry_interval', HTTP_DEFAULT_MAX_RETRY_INTERVAL),
            'log_id': config.get('log_id', None)
        }

    def loop(run):
        def wrapper(self, *args, **kwargs):
            if self.loop_task:
                interval: int = self.loop_task.get(HTTP_INTERVAL, 3)
                until_condition: str = self.loop_task.get(CONDITION)
                if is_qualified(instance=self.parameters, evaluation=until_condition):
                    return FINISHED
                state, response = run(self)
                if state == FAILED:
                    return FAILED, {}
                time.sleep(interval)
            else:
                state, response = run(self)
                return state, response
        return wrapper

    @loop
    def run(self):
        try:
            client = HttpClient(**self.config)
            response = client.request()
            try:
                return FINISHED
            except json.decoder.JSONDecodeError:
                return FINISHED
        except Exception as e:
            return FAILED


class ReviewExecutor:
    def run(self):
        return RUNNING


class ActivityExecutor:
    def __init__(self, parameters: dict, scheme: dict):
        self.parameters = parameters
        self.element = scheme.get('element')
        self.scheme = scheme.get('scheme')

    def run(self):
        if self.element == HTTP_TASK:
            executor = HttpExecutor(parameters=self.parameters, config=self.scheme)
            return executor.run()
        elif self.element == REVIEW_TASK:
            executor = ReviewExecutor()
            return executor.run()

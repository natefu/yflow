import re

from functools import reduce
from typing import Union, Any

from constants import (
    VAR_NODE_ID, VAR_NODE_STATE, VAR_TICKET_STATE, VAR_TICKET_ID,
    VAR_TICKET_PROCESS, READY,
)
from domain import Ticket, Node


def get_variable_dict(prefix: str, variables: list[dict]) -> dict:
    variable_dict = {}
    for variable in variables:
        variable_dict.update({prefix.format(variable.get('name')): variable.get('value')})
    return variable_dict


def get_context_dict(prefix: str, context: list[dict]) -> dict:
    return {}


def build_node_variables(node: Node, ticket: Ticket) -> dict:
    variables: dict = {
        f'{node.name}_{VAR_NODE_ID}': node.id,
        f'{node.name}_{VAR_NODE_STATE}': node.state
    }
    variables.update(get_variable_dict(prefix=f'{node.name}'+'_{}', variables=node.variables))
    variables.update(get_context_dict(prefix=f'{node.name}' + '_{}', context=node.context))
    variables.update(build_ticket_variables(ticket))
    return variables


def build_ticket_variables(ticket: Ticket) -> dict:
    variables: dict = {
        VAR_TICKET_PROCESS: ticket.process,
        VAR_TICKET_ID: ticket.id,
        VAR_TICKET_STATE: ticket.state
    }
    variables.update(get_variable_dict(prefix='{}', variables=ticket.variables))
    return variables


def get_variable_context(instance: Union[Ticket, Node]) -> dict:
    variable_context = {}
    if isinstance(instance, Ticket):
        variable_context = build_ticket_variables(ticket=instance)
    elif isinstance(instance, Node):
        variable_context = build_ticket_variables(ticket=instance.ticket)
    return variable_context


def substitute(
        variable_context: dict, expression: Union[str, dict, list]
) -> Any:
    if not expression:
        return expression

    pattern = re.compile(r'\$\{\w+(\.\w+)*\}')
    if isinstance(expression, str):
        has_variable = re.search(pattern, expression)
    else:
        has_variable = re.search(pattern, str(expression))

    if has_variable:
        evaluation = re.sub(
            pattern,
            lambda match: reduce(
                lambda x, y: x + '.get("' + y + '", {})',
                map(
                    lambda item: 'variable_context.get("' + item[1] + '", {})' if item[0] == 0 else item[1],
                    enumerate(match.group(0)[2:-1].split('.')[:-1])
                )
            ) + '.get("' + match.group(0)[2:-1].split('.')[:-1] + '")' if len(
                match.group(0)[2:-1].split('.')
            ) > 1 else 'variable_context.get("' + match.group(0)[2:-1] + '")',
            expression
        )
    else:
        evaluation = expression
    try:
        if isinstance(evaluation, bool):
            return evaluation
        return eval(evaluation)
    except:
        raise


def is_qualified(instance: Union[Ticket, Node], evaluation: str) -> bool:
    variable_context = get_variable_context(instance=instance)
    result = substitute(variable_context=variable_context, expression=evaluation)
    if isinstance(result, bool):
        return result
    else:
        return False

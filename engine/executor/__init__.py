"""

--------------------------------------------------------------------------------------------------------------------------

工单节点实例状态会有 ready，running，failed，finished，denied，approved

当工单节点实例状态从ready -> running时，会有一个`同步`任务，真正去调度任务 在实例调度过程中，需要去判断当前工单节点和当前工单状态是否出去运行状态
    node.state ticket.state is in running state
当工单节点实例状态从running -> failed，finished，denied，approved，会有一个`异步`任务，去通知工单节点状态发生改变。工单节点实例上只存在这种情况

--------------------------------------------------------------------------------------------------------------------------

工单节点状态会有 ready，running，failed，finished，denied，approved，skipped，pending，

当工单节点状态从ready -> running时
1. ticket.state is in running state
2. 若是任务节点，会有一个`异步`任务，去调度工单节点实例
3. 若是网关节点，会有一个`同步`任务，去判断网关状态
4. 若是start end节点，会有一个`同步`任务去开始，或者结束

当工单节点状态从running -> failed
1. 会将工单节点状态设置成failed
2. 会有一个`同步`任务，去判断当前工单状态
3. 会根据工单状态，工单节点状态，调度回调任务

当工单节点状态从running -> finished
1. 会将工单节点状态设置成finished
2. 会有一个`同步`任务，去判断当前工单状态
3. 会根据工单状态，工单节点状态，往后流转，`异步`调度接下去的节点
4. 会根据工单状态，工单节点状态，调度回调任务

当工单节点状态从running -> denied
1. 会将工单节点状态设置成denied
2. 会有一个`同步`任务，去判断当前工单状态
3. 会根据工单状态，工单节点状态，工单后续节点，`异步`调度接下去的节点
4. 会根据工单状态，工单节点状态，调度回调任务

当工单节点状态从running -> approved
1. 会将工单节点设置成approved
2. 会有一个`同步`任务，去判断当前工单状态
3. 会根据工单状态，工单节点状态，工单后续节点，`异步`调度接下去的节点
4. 会根据工单状态，工单节点状态，调度回调任务

当工单节点状态从failed -> skipped
1. 判断当前工单状态是否是是failed
2. 将当前工单节点设置成running，并且将当前工单状态设置成running
3. 会根据工单状态，工单节点状态，异步调度回调任务

当工单节点状态从running -> pending
1. 判断当前工单节点状态是否是running
2. 将当前工单节点设置成pending
3. 会根据工单状态，工单节点状态，异步调度回调任务

--------------------------------------------------------------------------------------------------------------------------

工单状态会有 ready，running，failed，finished，revoked，terminated，closed

1. 当工单状态发生变化时，会根据当前的状态，异步调度回调任务
"""

from .instance import InstanceExecutor
from .node import NodeExecutor
from .ticket import TicketExecutor


__all__ = [
    # instance
    'InstanceExecutor',

    # node
    'NodeExecutor',

    # ticket
    'TicketExecutor',
]

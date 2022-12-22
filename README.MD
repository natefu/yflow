# cookbook
`simple example:`
```
{
    'nodes': [
        {
            'identifier': 'start_event', 
            'name': 'start_event', 
            'element': 'startEvent'
        }, {
            'identifier': 'review_task', 
            'name': 'review_task', 
            'element': 'review', 
            'scheme': {
                'partitions': [1]
            }
        }, {
            'identifier': 'exclusiveGateway', 
            'name': 'exclusiveGateway', 
            'element': 'exclusiveGateway'
        }, {
            'identifier': 'review_task_1', 
            'name': 'review_task_1', 
            'element': 'review', 
            'scheme': {
                'partitions': [1]
            }
        }, {
            'identifier': 'parallel', 
            'name': 'parallel', 
            'element': 'parallelGateway'
        }, {
            'identifier': 'review_task_2', 
            'name': 'review_task_2', 
            'element': 'review', 
            'scheme': {
                'partitions': [1]
            }
        }, {
            'identifier': 'review_task_3', 
            'name': 'review_task_3', 
            'element': 'review', 
            'scheme': {
                'partitions': [1]
            }
        }, {
            'identifier': 'convergingAndGateway', 
            'name': 'convergingAndGateway', 
            'element': 'convergingAndGateway'
        }, {
            'identifier': 'end_event', 
            'name': 'end_event', 
            'element': 'endEvent'
        }
    ], 
    'flows': [
        {
            'source': 'start_event', 
            'target': 'review_task'
        }, 
        {
            'source': 'review_task', 
            'target': 'exclusiveGateway'
        }, 
        {
            'source': 'exclusiveGateway', 
            'target': 'review_task_1', 
            'condition': '${review_task_state} == "approved"'
        }, 
        {
            'source': 'review_task_1', 
            'target': 'parallel'
        }, 
        {
            'source': 'parallel', 
            'target': 'review_task_2'
        }, 
        {
            'source': 'parallel', 
            'target': 'review_task_3'
        }, 
        {
            'target': 'convergingAndGateway', 
            'condition': '${review_task_2_state} == "approved"', 
            'source': 'review_task_2'
        }, 
        {
            'source': 'review_task_3', 
            'target': 'convergingAndGateway', 
            'condition': '${review_task_3_state} == "approved"'
        }, 
        {
            'source': 'convergingAndGateway', 'target': 'end_event'
        }
    ]
}
```
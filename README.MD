# cookbook
`simple example:`
```commandline
{
    "nodes": [
        {
            "identifier": "start_event",
            "name": "start_event",
            "element": "startEvent"
        },
        {
            "identifier": "review_task",
            "name": "review_task",
            "element": "review",
            "scheme": {
                "partitions": [1]
            }
        },
        {
            "identifier": "exclusiveGateway",
            "name": "exclusiveGateway",
            "element": "exclusiveGateway"
        },
        {
            "identifier": "end_event",
            "name": "end_event",
            "element": "endEvent"
        }
    ],
    "flows": [
        {
            "source": "start_event",
            "target": "review_task"
        },
        {
            "source": "review_task",
            "target": "exclusiveGateway"
        },
        {
            "source": "exclusiveGateway",
            "target": "end_event",
            "condition": "${exclusiveGateway_state} == approved"
        }
    ]
}
```
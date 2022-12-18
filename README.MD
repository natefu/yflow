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
            "target": "end_event"
        }
    ]
}
```
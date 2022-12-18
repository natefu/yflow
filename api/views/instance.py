from domain import Instance, Node
from engine.scheduler import instance_scheduler
from framework import generics
from storage.mysql import instance_operator, node_operator
from storage.mysql.serializers import InstanceSerializer
from rest_framework import status
from rest_framework.response import Response


class InstanceUpdateView(generics.UpdateAPIView):

    domain = Instance
    operator = instance_operator
    serializer_class = InstanceSerializer

    def update(self, request, *args, **kwargs):
        action = request.data.get('action', None)
        if not action:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        instance: Instance = self.get_object()
        instance_scheduler.apply_async(
            kwargs={'ticket_id': instance.node.ticket, 'node_id': instance.node.id, 'instance_id': instance.id, 'instance_command': action}
        )
        return Response(status=status.HTTP_202_ACCEPTED)
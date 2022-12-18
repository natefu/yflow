from domain import Process
from framework import generics
from storage.mysql import process_operator
from storage.mysql.serializers import ProcessSerializer
from rest_framework import status
from rest_framework.response import Response


class ProcessCreateListView(generics.ListCreateAPIView):

    domain = Process
    operator = process_operator
    serializer_class = ProcessSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        process = Process(**data)
        process = process_operator.create(process)
        headers = self.get_success_headers(process)
        return Response(process, status=status.HTTP_201_CREATED, headers=headers)

'''
    def list(self, request, *args, **kwargs):
        queryset = process_operator.query()
        data = []
        for object in queryset:
            data.append(object.to_dict())
        return Response(data)
'''
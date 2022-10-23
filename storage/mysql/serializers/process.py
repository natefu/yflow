from rest_framework import serializers
from domain import Process
from storage.mysql.models import Process as ProcessModel


class ProcessSerializer(serializers.ModelSerializer):
    scheme = serializers.JSONField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProcessModel
        fields = ('id', 'name', 'version', 'scheme', 'deprecated', 'created', 'updated')

    @staticmethod
    def to_model(process: Process):
        process_dict = process.to_dict()
        return ProcessModel(**process_dict)

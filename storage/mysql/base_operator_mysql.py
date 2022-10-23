from domain import Base
from rest_framework.serializers import SerializerMetaclass
from django.db.models.base import ModelBase


class BaseOperatorMysql:

    def __init__(self, domain: type, model: ModelBase, serializer: SerializerMetaclass):
        self.domain: type = domain
        self.model: ModelBase = model
        self.serializer: SerializerMetaclass = serializer

    def create_object(self, domain: Base, times=None):
        serializer = self.serializer(data=domain.to_dict())
        serializer.is_valid(raise_exception=True)
        if not times:
            serializer.save()
        else:
            serializer.save(**times)
        return self.domain(**serializer.data)

    def update_object(self, pk: int, partial=False, times=None, **updates):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer(instance=instance, data=updates, partial=partial)
        serializer.is_valid(raise_exception=True)
        if not times:
            serializer.save()
        else:
            serializer.save(**times)
        return self.domain(**serializer.data)

    def get_object(self, pk: int):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer(instance=instance)
        return self.domain(**serializer.data)

    def query_objects(self, **query_params) -> list:
        instances = self.model.objects.filter(**query_params)
        serializer = self.serializer(instances, many=True)
        # todo pagination
        return [self.domain(**data) for data in serializer.data]

    def delete_object(self, pk: int) -> None:
        self.model.objects.filter(pk=pk).delete()

    def delete_objects(self, **query_params) -> None:
        self.model.objects.filter(**query_params).delete()

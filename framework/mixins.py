from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CreateModelMixin:
    def retrieve(self, data):
        try:
            return self.domain(**data)
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = self.retrieve(request.data)
        self.operator.create(data)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(queryset)
        return Response(queryset)


class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(instance)


class UpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        if 'pk' in filter_kwargs:
            identity = filter_kwargs.get('pk')
        elif 'id' in filter_kwargs:
            identity = filter_kwargs.get('id')
        else:
            identity = self.get_object().id
        data = self.operator.update(pk=identity, partial=partial, **request.data)
        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.operator.delete(id=instance.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

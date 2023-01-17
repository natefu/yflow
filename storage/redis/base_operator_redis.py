import json

from domain import Base


class BaseOperatorRedis:

    def create_object(self, domain: Base):
        pass

    def add_index(self, key, value):
        pass

    def update_object(self, name: str, **updates):
        pass

    def delete_object(self, name: str):
        pass

    def generate_id(self, domain: Base):
        pass
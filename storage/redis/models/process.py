from storage.redis.models.base import BaseModel, Field, Category, DatetimeField


class Process(BaseModel):
    name = Field(category=Category.STRING, unique=True)
    version = Field(category=Category.INT)
    scheme = Field(category=Category.DICT)
    deprecated = Field(category=Category.BOOL)
    created = DatetimeField(auto_now_add=True)
    updated = DatetimeField(auto_now=True)

    class Meta:
        index_name = 'process'
        unique_keys = []

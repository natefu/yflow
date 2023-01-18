import json
from datetime import datetime
from enum import Enum
from storage.redis.client import redis_conn as conn

DATETIME_PATTERN = '%Y-%m-%d %H:%M:%S'


class Category(Enum):
    INT = (0, int)
    STRING = (1, str)
    BOOL = (2, bool)
    DICT = (3, dict)
    LIST = (4, list)
    DEFINED = (5, int)

    def __init__(self, num, category):
        self.num = num
        self.category = category

    def is_instance(self, value):
        return isinstance(value, self.category)

    @staticmethod
    def non_serialized_field():
        return [Category.INT, Category.STRING, Category.BOOL, Category.DEFINED]


class Field:
    def __init__(self, category: Category, primary: bool = False, unique: bool = False):
        self._category: Category = category
        self._primary = primary
        self._unique = unique
        self._value = None

    @property
    def value(self):
        if self.category in Category.non_serialized_field():
            return self._value
        else:
            return json.loads(self._value)

    def get_ori_value(self):
        return self._value

    def _set_value(self, value):
        if self.category and self.category.is_instance(value):
            if self.category in Category.non_serialized_field():
                self._value = value
            else:
                try:
                    self._value = json.dumps(value)
                except:
                    raise AttributeError
        elif isinstance(value, str):
            self._value = value
        else:
            raise AttributeError

    @value.setter
    def value(self, value):
        self._set_value(value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, primary):
        self._primary = primary

    @property
    def unique(self):
        return self._unique

    @unique.setter
    def unique(self, unique):
        self._unique = unique


class DatetimeField(Field):
    def __init__(self, auto_now_add: bool = False, auto_now: bool = False, primary: bool = False, unique: bool = False):
        super().__init__(Category.DEFINED, primary, unique)
        self._auto_now_add = auto_now_add
        self._auto_now = auto_now

    @property
    def auto_now_add(self):
        return self._auto_now_add

    @auto_now_add.setter
    def index_name(self, auto_now_add):
        self._auto_now_add = auto_now_add

    @property
    def auto_now(self):
        return self._auto_now

    @auto_now.setter
    def index_name(self, auto_now):
        self._auto_now = auto_now

    @property
    def value(self):
        return datetime.strptime(self._value, DATETIME_PATTERN)

    @value.setter
    def value(self, value):
        if isinstance(value, datetime):
            self._value = value.strftime(DATETIME_PATTERN)
        else:
            self._value = value


class ForeignField(Field):
    def __init__(self, model, primary: bool = False, unique: bool = False):
        super().__init__(Category.DEFINED, primary, unique)
        self._model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def index_name(self, model):
        self._model = model

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, str) or isinstance(value, int):
            self._value = value
        else:
            raise AttributeError


class BaseModel:
    # 还有一些问题，失败的怎么处理
    # 怎么通过外键/unique获取主键
    # 怎么更新普通字段，外键，unique
    class Meta:
        PARTITION_LENGTH = 10000
        primary_key = 'id'
        foreign_keys = []
        unique_keys = []
        index_name = 'default'

    def __init__(self, **kwargs):
        self.id = Field(category=Category.INT, primary=True)
        for key in self.__dir__():
            if isinstance(getattr(self, key), Field):
                self.__dict__[key] = getattr(self, key)
                if key in kwargs:
                    self.__dict__.get(key).value = kwargs.get(key)
        if not self.id.value:
            self.id.value = self.generate_id()
        if self.Meta.index_name:
            BaseModel.Meta.index_name = self.Meta.index_name
        self.set_primary_key()
        self.set_foreign_keys()
        self.set_unique_keys()

    def set_primary_key(self):
        for key, value in self.__dict__.items():
            if value.primary:
                assert Category.INT.is_instance(value.value) or Category.STRING.is_instance(value.value)
                BaseModel.Meta.primary_key = key
                break

    def set_foreign_keys(self):
        for key, value in self.__dict__.items():
            if isinstance(value, ForeignField):
                BaseModel.Meta.foreign_keys.append(key)

    def set_unique_keys(self):
        for key, value in self.__dict__.items():
            if value.unique:
                BaseModel.Meta.unique_keys.append(key)
        for value in self.Meta.unique_keys:
            BaseModel.Meta.unique_keys.append(sorted(value))

    def _check_unique(self, name):
        for value in BaseModel.Meta.unique_keys:
            if isinstance(value, str) and value in self.__dict__:
                unique_field: Field = self.__dict__.get(value)
                key = f'{self.Meta.index_name}-unique-{value}-{unique_field.get_ori_value()}'
                if not conn.setnx(key, name):
                    raise AssertionError
            elif isinstance(value, list) or isinstance(value, set):
                key = f'{self.Meta.index_name}-unique'
                for key_name in value:
                    if isinstance(key_name, str) and key_name in self.__dict__:
                        unique_field: Field = self.__dict__.get(key_name)
                        key += f'-{value}-{unique_field.get_ori_value()}'
                if not conn.setnx(key, name):
                    raise AssertionError

    def _delete_unique(self, name):
        for value in BaseModel.Meta.unique_keys:
            if isinstance(value, str) and value in self.__dict__:
                unique_field: Field = self.__dict__.get(value)
                key = f'{self.Meta.index_name}-unique-{name}-{unique_field.get_ori_value()}'
                conn.delete(key)
            elif isinstance(value, list) or isinstance(value, set):
                key = f'{self.Meta.index_name}-unique-{name}'
                for key_name in value:
                    if isinstance(key_name, str) and key_name in self.__dict__:
                        unique_field: Field = self.__dict__.get(key_name)
                        key += f'{unique_field.get_ori_value()}'
                conn.delete(key)

    def _save_foreign_key(self, name): # key job_id, foreign_key: process_id
        metadata = {}
        for foreign_key in BaseModel.Meta.foreign_keys:
            _foreign_key: ForeignField = self.__dict__.get(foreign_key, '')
            assert isinstance(_foreign_key, ForeignField)
            assert conn.exists(f'{_foreign_key.model.Meta.index_name}-{_foreign_key.value}')
            # primary -> foreign index || write in the same key with whole model body
            conn.hset(f'{self.Meta.index_name}-{name}', _foreign_key.get_ori_value(), 1)

            # foreign index -> primary
            prefix = f'{self.Meta.index_name}-{foreign_key}-{_foreign_key.get_ori_value()}'
            foreign_position = conn.incr(f'{prefix}_incr_count')
            conn.incr(f'{prefix}_real_count')
            if foreign_position % BaseModel.Meta.PARTITION_LENGTH == 1:
                partition = conn.incr(f'{prefix}_partition')
            else:
                partition = conn.get(f'{prefix}_partition')
            conn.hset(f'{prefix}_partition_{partition}', f'{_foreign_key.get_ori_value()}-{name}', 1)
            metadata[foreign_key] = foreign_position
        return metadata

    def _delete_foreign_key(self, name, metadata):
        for foreign_key in BaseModel.Meta.foreign_keys:
            _foreign_key: ForeignField = self.__dict__.get(foreign_key, '')
            assert isinstance(_foreign_key, ForeignField)
            # delete foreign index -> primary
            prefix = f'{self.Meta.index_name}-{foreign_key}-{_foreign_key.get_ori_value()}'
            conn.decr(f'{prefix}_real_count')
            foreign_position = metadata.get(foreign_key, -1)
            assert foreign_position != -1
            partition = (foreign_position-1) // BaseModel.Meta.PARTITION_LENGTH + 1
            conn.hdel(f'{prefix}_partition_{partition}', f'{_foreign_key.get_ori_value()}-{name}')

    def _hset(self, name, key, value):
        if isinstance(value, dict):
            conn.hset(name, key, json.dumps(value))
        elif isinstance(value, list):
            conn.hset(name, key, json.dumps(value))
        elif isinstance(value, str):
            conn.hset(name, key, value)
        elif isinstance(value, int):
            conn.hset(name, key, value)

    def save(self):
        name = self.get_primary_value().value
        self._check_unique(name)
        metadata = self._save_foreign_key(name)
        for key, value in self.__dict__.items():
            if isinstance(value, DatetimeField):
                if not value.get_ori_value() and (value.auto_now or value.auto_now_add):
                    value.value = datetime.now()
                elif value.get_ori_value() and value.auto_now:
                    value.value = datetime.now()
            self._hset(f'{self.Meta.index_name}-{name}', key, value.get_ori_value())
        self._hset(f'{self.Meta.index_name}-{name}', 'metadata', metadata)
        return name

    def delete(self):
        name = self.get_primary_value().value
        self._delete_unique(name)
        metadata = json.loads(conn.hget(f'{self.Meta.index_name}-{name}', 'metadata'))
        self._delete_foreign_key(name, metadata)
        conn.delete(f'{self.Meta.index_name}-{name}')

    def update(self, **values):
        for key, value in values.items():
            self.__dict__.get(key).value = value
        self.save()

    def query(self, **params): # only support for one foreign field
        if len(params.items()):
            raise NotImplementedError

        key, value = list(params.items())[0]
        prefix = f'{self.Meta.index_name}-{key}-{value}'
        partition = conn.get(f'{prefix}_partition')
        ans = []
        for i in range(1, partition+1):
            result = conn.hgetall(f'{prefix}_partition_{partition}')
            ans.extend([key.split('-')[1] for _, round2 in result.items() for key, _ in round2.items()])
        return ans


    @classmethod
    def from_redis(cls, id):
        value: dict = conn.hgetall(f'{cls.Meta.index_name}-{id}')
        value['id'] = id
        return cls(**value)

    @classmethod
    def from_redis_unique_params(cls, **kargs):
        key_list = sorted([key for key, _ in kargs.items()])
        for foreign_pairs in cls.Meta.foreign_keys:
            if key_list == foreign_pairs:
                f'{cls.Meta.index_name}-unique-' + '-'.join(key_list)
                value: dict = conn.hgetall(conn.get(f'{cls.Meta.index_name}-unique-' + '-'.join(key_list)))
                return cls(**value)
        return AttributeError

    def generate_id(self):
        return conn.incr(f'{self.Meta.index_name}_id')

    def get_primary_value(self):
        return self.__dict__.get(BaseModel.Meta.primary_key)

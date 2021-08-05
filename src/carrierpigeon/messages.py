from collections import OrderedDict
import copy
import os

from . import exceptions

# from .fields import Field
from .handlers.json import JSONHandler


class BaseMessage(object):
    version_field = "version"

    def __init__(self, *args, **kwargs):
        self._orig_data = {}
        self._data = {}

        for field_name in self._fields:
            if field_name in kwargs:
                self._orig_data[field_name] = kwargs[field_name]

        if kwargs:
            self.from_dict(kwargs)

        if self.version_field:
            if self.version_field not in self._orig_data and self.version_field not in self._data:
                self._orig_data[self.version_field] = 1

    def __str__(self):
        return f"{self.__class__.__name__}: {self.all_data()}"

    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]
        elif key in self._orig_data:
            return self._orig_data[key]

        raise AttributeError(f"No attribute named {key}")

    def __setattr__(self, key, value):
        if key in self._fields:
            self._data[key] = value
        else:
            super().__setattr__(key, value)

    def __delattr__(self, key):
        self._data.pop(key, None)

    def _is_dirty(self):
        if not self._data:
            return False

        for key, value in self._data.items():
            if key in self._orig_data:
                if value != self._orig_data[key]:
                    return True
            else:
                # There's a new key present.
                return True

        return False

    def all_data(self):
        all_data = copy.deepcopy(self._orig_data)
        all_data.update(self._data)
        return all_data

    def from_dict(self, data):
        for field_name in self._fields:
            if field_name in data:
                self._data[field_name] = data[field_name]

    @classmethod
    def read(cls, raw_msg):
        data = cls._handler.read(raw_msg)
        cls._handler.validate(data)
        return cls(**data)

    def create(self):
        data = self.all_data()

        if self.version_field:
            if self.version_field not in data:
                raise exceptions.CarrierLost(f"No version information '{self.version_field}' present in the message!")

        self._handler.validate(data)
        return self._handler.write(data)


class MessageFactory(object):
    def __init__(self, schema, handler=JSONHandler, message_cls=BaseMessage):
        self.schema_path = schema
        self.handler = handler(self.schema_path)
        self.message_cls = message_cls

    def construct(self, name=None):
        fields = OrderedDict()
        title, schema_info = self.handler.from_contract()

        if not name:
            name = title

        # TODO: For now, ghetto.
        fields = schema_info

        # Allow for overriding the base.
        bases = (self.message_cls,)
        attrs = {
            "_fields": fields,
            "_handler": self.handler,
            "_orig_data": {},
            "_data": {},
        }

        klass = type(name, bases, attrs)
        return klass


def message_for(schema, name=None):
    mf = MessageFactory(schema)
    return mf.construct(name=name)

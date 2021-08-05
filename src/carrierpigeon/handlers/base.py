from collections import OrderedDict
import os

from .. import exceptions


class BaseHandler(object):
    def __init__(self, schema_path=None):
        self.schema_path = schema_path
        self.schema = None

    def from_contract(self):
        raise NotImplementedError("Subclasses must define this method")

    def read(self, raw_msg):
        raise NotImplementedError("Subclasses must define this method")

    def write(self, data):
        raise NotImplementedError("Subclasses must define this method")

    def validate(self, raw_data):
        raise NotImplementedError("Subclasses must define this method")

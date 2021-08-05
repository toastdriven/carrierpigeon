import glob
import os

from . import exceptions
from . import messages


class Library(object):
    def __init__(self, base_contract_dir):
        self.base_contract_dir = base_contract_dir
        self._classes = {}

    def __getattr__(self, possible_class):
        if possible_class in self._classes:
            return self._classes[possible_class]

        raise AttributeError(f"No attribute named {possible_class}")

    def check_exists(self):
        if not os.path.exists(self.base_contract_dir):
            raise exceptions.InvalidContractDirectory(f"No contracts found at {self.base_contract_dir}")

    def collect_contracts(self):
        # FIXME: This is JSON-specific for now.
        return glob.glob(os.path.join(self.base_contract_dir, "*.json"))

    def load(self, contract):
        return messages.message_for(contract)

    def available_classes(self):
        return [key for key in self._classes]

    @classmethod
    def load_all(cls, base_contract_dir):
        obj = cls(base_contract_dir)
        obj.check_exists()
        contract_paths = obj.collect_contracts()

        for contract_path in contract_paths:
            klass = obj.load(contract_path)
            obj._classes[klass.__name__] = klass

        return obj


def load_library(base_contract_dir):
    return Library.load_all(base_contract_dir)

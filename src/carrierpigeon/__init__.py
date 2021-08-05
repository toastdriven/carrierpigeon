from .libraries import Library, load_library
from .messages import MessageFactory, message_for


__author__ = "Daniel Lindsley"
__license__ = "New BSD"
__version__ = (0, 3, 0, "alpha")


def get_short_version():
    return ".".join([str(digit) for digit in __version__[0:3]])


def get_full_version():
    return "-".join([get_short_version(), "-".join([str(bit) for bit in __version__[3:]])])


__all__ = [
    MessageFactory,
    message_for,
    get_short_version,
    get_full_version,
    Library,
    load_library,
]

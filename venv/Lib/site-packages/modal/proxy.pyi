import modal.object
import typing

class _Proxy(modal.object._Object):
    @staticmethod
    def from_name(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> _Proxy: ...

class Proxy(modal.object.Object):
    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def from_name(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> Proxy: ...

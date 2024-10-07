import enum
import modal.functions
import modal_proto.api_pb2
import typing

class _PartialFunctionFlags(enum.IntFlag):
    FUNCTION: int = 1
    BUILD: int = 2
    ENTER_PRE_SNAPSHOT: int = 4
    ENTER_POST_SNAPSHOT: int = 8
    EXIT: int = 16

    @staticmethod
    def all() -> "_PartialFunctionFlags":
        return ~_PartialFunctionFlags(0)  # type: ignore #  for some reason mypy things this has type int

class _PartialFunction:
    raw_f: typing.Callable[..., typing.Any]
    flags: _PartialFunctionFlags
    webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None]
    is_generator: typing.Union[bool, None]
    keep_warm: typing.Union[int, None]

    def __init__(
        self,
        raw_f: typing.Callable[..., typing.Any],
        flags: _PartialFunctionFlags,
        webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None] = None,
        is_generator: typing.Union[bool, None] = None,
        keep_warm: typing.Union[int, None] = None,
    ): ...
    def __get__(self, obj, objtype=None) -> modal.functions._Function: ...
    def __del__(self): ...
    def add_flags(self, flags) -> _PartialFunction: ...

class PartialFunction:
    raw_f: typing.Callable[..., typing.Any]
    flags: _PartialFunctionFlags
    webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None]
    is_generator: typing.Union[bool, None]
    keep_warm: typing.Union[int, None]

    def __init__(
        self,
        raw_f: typing.Callable[..., typing.Any],
        flags: _PartialFunctionFlags,
        webhook_config: typing.Union[modal_proto.api_pb2.WebhookConfig, None] = None,
        is_generator: typing.Union[bool, None] = None,
        keep_warm: typing.Union[int, None] = None,
    ): ...
    def __get__(self, obj, objtype=None) -> modal.functions.Function: ...
    def __del__(self): ...
    def add_flags(self, flags) -> PartialFunction: ...

def _find_partial_methods_for_user_cls(
    user_cls: typing.Type, flags: _PartialFunctionFlags
) -> typing.Dict[str, _PartialFunction]: ...
def _find_callables_for_cls(
    user_cls: typing.Type, flags: _PartialFunctionFlags
) -> typing.Dict[str, typing.Callable]: ...
def _find_callables_for_obj(
    user_obj: typing.Any, flags: _PartialFunctionFlags
) -> typing.Dict[str, typing.Callable]: ...
def _method(
    _warn_parentheses_missing=None,
    *,
    is_generator: typing.Union[bool, None] = None,
    keep_warm: typing.Union[int, None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], _PartialFunction]: ...
def _parse_custom_domains(
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.List[modal_proto.api_pb2.CustomDomainConfig]: ...
def _web_endpoint(
    _warn_parentheses_missing=None,
    *,
    method: str = "GET",
    label: typing.Union[str, None] = None,
    docs: bool = False,
    wait_for_response: bool = True,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], _PartialFunction]: ...
def _asgi_app(
    _warn_parentheses_missing=None,
    *,
    label: typing.Union[str, None] = None,
    wait_for_response: bool = True,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], _PartialFunction]: ...
def _wsgi_app(
    _warn_parentheses_missing=None,
    *,
    label: typing.Union[str, None] = None,
    wait_for_response: bool = True,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], _PartialFunction]: ...
def _web_server(
    port: int,
    *,
    startup_timeout: float = 5.0,
    label: typing.Union[str, None] = None,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], _PartialFunction]: ...
def _disallow_wrapping_method(f: _PartialFunction, wrapper: str) -> None: ...
def _build(
    _warn_parentheses_missing=None,
) -> typing.Callable[[typing.Union[typing.Callable[[typing.Any], typing.Any], _PartialFunction]], _PartialFunction]: ...
def _enter(
    _warn_parentheses_missing=None, *, snap: bool = False
) -> typing.Callable[[typing.Union[typing.Callable[[typing.Any], typing.Any], _PartialFunction]], _PartialFunction]: ...
def _exit(
    _warn_parentheses_missing=None,
) -> typing.Callable[
    [
        typing.Union[
            typing.Callable[
                [
                    typing.Any,
                    typing.Union[typing.Type[BaseException], None],
                    typing.Union[BaseException, None],
                    typing.Any,
                ],
                None,
            ],
            typing.Callable[[typing.Any], None],
        ]
    ],
    _PartialFunction,
]: ...
def method(
    _warn_parentheses_missing=None,
    *,
    is_generator: typing.Union[bool, None] = None,
    keep_warm: typing.Union[int, None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], PartialFunction]: ...
def web_endpoint(
    _warn_parentheses_missing=None,
    *,
    method: str = "GET",
    label: typing.Union[str, None] = None,
    docs: bool = False,
    wait_for_response: bool = True,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], PartialFunction]: ...
def asgi_app(
    _warn_parentheses_missing=None,
    *,
    label: typing.Union[str, None] = None,
    wait_for_response: bool = True,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], PartialFunction]: ...
def wsgi_app(
    _warn_parentheses_missing=None,
    *,
    label: typing.Union[str, None] = None,
    wait_for_response: bool = True,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], PartialFunction]: ...
def web_server(
    port: int,
    *,
    startup_timeout: float = 5.0,
    label: typing.Union[str, None] = None,
    custom_domains: typing.Union[typing.Iterable[str], None] = None,
) -> typing.Callable[[typing.Callable[..., typing.Any]], PartialFunction]: ...
def build(
    _warn_parentheses_missing=None,
) -> typing.Callable[[typing.Union[typing.Callable[[typing.Any], typing.Any], PartialFunction]], PartialFunction]: ...
def enter(
    _warn_parentheses_missing=None, *, snap: bool = False
) -> typing.Callable[[typing.Union[typing.Callable[[typing.Any], typing.Any], PartialFunction]], PartialFunction]: ...
def exit(
    _warn_parentheses_missing=None,
) -> typing.Callable[
    [
        typing.Union[
            typing.Callable[
                [
                    typing.Any,
                    typing.Union[typing.Type[BaseException], None],
                    typing.Union[BaseException, None],
                    typing.Any,
                ],
                None,
            ],
            typing.Callable[[typing.Any], None],
        ]
    ],
    PartialFunction,
]: ...

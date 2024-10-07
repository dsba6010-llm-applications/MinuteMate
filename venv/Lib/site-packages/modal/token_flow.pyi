import modal.client
import modal_proto.api_pb2
import synchronicity.combined_types
import typing
import typing_extensions

class _TokenFlow:
    def __init__(self, client: modal.client._Client): ...
    def start(
        self, utm_source: typing.Union[str, None] = None, next_url: typing.Union[str, None] = None
    ) -> typing.AsyncContextManager[typing.Tuple[str, str, str]]: ...
    async def finish(
        self, timeout: float = 40.0, grpc_extra_timeout: float = 5.0
    ) -> typing.Union[modal_proto.api_pb2.TokenFlowWaitResponse, None]: ...

class TokenFlow:
    def __init__(self, client: modal.client.Client): ...

    class __start_spec(typing_extensions.Protocol):
        def __call__(
            self, utm_source: typing.Union[str, None] = None, next_url: typing.Union[str, None] = None
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[typing.Tuple[str, str, str]]: ...
        def aio(
            self, utm_source: typing.Union[str, None] = None, next_url: typing.Union[str, None] = None
        ) -> typing.AsyncContextManager[typing.Tuple[str, str, str]]: ...

    start: __start_spec

    class __finish_spec(typing_extensions.Protocol):
        def __call__(
            self, timeout: float = 40.0, grpc_extra_timeout: float = 5.0
        ) -> typing.Union[modal_proto.api_pb2.TokenFlowWaitResponse, None]: ...
        async def aio(self, *args, **kwargs) -> typing.Union[modal_proto.api_pb2.TokenFlowWaitResponse, None]: ...

    finish: __finish_spec

async def _new_token(
    *,
    profile: typing.Union[str, None] = None,
    activate: bool = True,
    verify: bool = True,
    source: typing.Union[str, None] = None,
    next_url: typing.Union[str, None] = None,
): ...
async def _set_token(
    token_id: str,
    token_secret: str,
    *,
    profile: typing.Union[str, None] = None,
    activate: bool = True,
    verify: bool = True,
): ...
def _open_url(url: str) -> bool: ...

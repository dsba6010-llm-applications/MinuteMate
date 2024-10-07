import modal._utils.async_utils
import modal.client
import modal.functions
import typing
import typing_extensions

class _SynchronizedQueue:
    async def init(self): ...
    async def put(self, item): ...
    async def get(self): ...

class SynchronizedQueue:
    def __init__(self, /, *args, **kwargs): ...

    class __init_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    init: __init_spec

    class __put_spec(typing_extensions.Protocol):
        def __call__(self, item): ...
        async def aio(self, *args, **kwargs): ...

    put: __put_spec

    class __get_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    get: __get_spec

class _OutputValue:
    value: typing.Any

    def __init__(self, value: typing.Any) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...

def _map_invocation(
    function: modal.functions._Function,
    raw_input_queue: _SynchronizedQueue,
    client: modal.client._Client,
    order_outputs: bool,
    return_exceptions: bool,
    count_update_callback: typing.Union[typing.Callable[[int, int], None], None],
): ...
def _map_sync(
    self, *input_iterators, kwargs={}, order_outputs: bool = True, return_exceptions: bool = False
) -> modal._utils.async_utils.AsyncOrSyncIteratable: ...
def _map_async(
    self,
    *input_iterators: typing.Union[typing.Iterable[typing.Any], typing.AsyncIterable[typing.Any]],
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
) -> typing.AsyncGenerator[typing.Any, None]: ...
def _for_each_sync(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False): ...
async def _for_each_async(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False): ...
def _starmap_async(
    self,
    input_iterator: typing.Union[
        typing.Iterable[typing.Sequence[typing.Any]], typing.AsyncIterable[typing.Sequence[typing.Any]]
    ],
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
) -> typing.AsyncIterable[typing.Any]: ...
def _starmap_sync(
    self,
    input_iterator: typing.Iterable[typing.Sequence[typing.Any]],
    kwargs={},
    order_outputs: bool = True,
    return_exceptions: bool = False,
) -> modal._utils.async_utils.AsyncOrSyncIteratable: ...

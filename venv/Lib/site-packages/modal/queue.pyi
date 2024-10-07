import modal.client
import modal.object
import synchronicity.combined_types
import typing
import typing_extensions

class _Queue(modal.object._Object):
    @staticmethod
    def new(): ...
    def __init__(self): ...
    @staticmethod
    def validate_partition_key(partition: typing.Union[str, None]) -> bytes: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[_Queue],
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        _heartbeat_sleep: float = 300,
    ) -> typing.AsyncContextManager[_Queue]: ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Union[str, None] = None, create_if_missing: bool = False
    ) -> _Queue: ...
    @staticmethod
    def persisted(label: str, namespace=1, environment_name: typing.Union[str, None] = None): ...
    @staticmethod
    async def lookup(
        label: str,
        namespace=1,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        create_if_missing: bool = False,
    ) -> _Queue: ...
    @staticmethod
    async def delete(
        label: str,
        *,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
    ): ...
    async def _get_nonblocking(self, partition: typing.Union[str, None], n_values: int) -> typing.List[typing.Any]: ...
    async def _get_blocking(
        self, partition: typing.Union[str, None], timeout: typing.Union[float, None], n_values: int
    ) -> typing.List[typing.Any]: ...
    async def clear(self, *, partition: typing.Union[str, None] = None, all: bool = False) -> None: ...
    async def get(
        self,
        block: bool = True,
        timeout: typing.Union[float, None] = None,
        *,
        partition: typing.Union[str, None] = None,
    ) -> typing.Union[typing.Any, None]: ...
    async def get_many(
        self,
        n_values: int,
        block: bool = True,
        timeout: typing.Union[float, None] = None,
        *,
        partition: typing.Union[str, None] = None,
    ) -> typing.List[typing.Any]: ...
    async def put(
        self,
        v: typing.Any,
        block: bool = True,
        timeout: typing.Union[float, None] = None,
        *,
        partition: typing.Union[str, None] = None,
        partition_ttl: int = 86400,
    ) -> None: ...
    async def put_many(
        self,
        vs: typing.List[typing.Any],
        block: bool = True,
        timeout: typing.Union[float, None] = None,
        *,
        partition: typing.Union[str, None] = None,
        partition_ttl: int = 86400,
    ) -> None: ...
    async def _put_many_blocking(
        self,
        partition: typing.Union[str, None],
        partition_ttl: int,
        vs: typing.List[typing.Any],
        timeout: typing.Union[float, None] = None,
    ): ...
    async def _put_many_nonblocking(
        self, partition: typing.Union[str, None], partition_ttl: int, vs: typing.List[typing.Any]
    ): ...
    async def len(self, *, partition: typing.Union[str, None] = None, total: bool = False) -> int: ...
    def iterate(
        self, *, partition: typing.Union[str, None] = None, item_poll_timeout: float = 0.0
    ) -> typing.AsyncGenerator[typing.Any, None]: ...

class Queue(modal.object.Object):
    def __init__(self): ...
    @staticmethod
    def new(): ...
    @staticmethod
    def validate_partition_key(partition: typing.Union[str, None]) -> bytes: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[Queue],
        client: typing.Union[modal.client.Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        _heartbeat_sleep: float = 300,
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Queue]: ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Union[str, None] = None, create_if_missing: bool = False
    ) -> Queue: ...
    @staticmethod
    def persisted(label: str, namespace=1, environment_name: typing.Union[str, None] = None): ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            namespace=1,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
            create_if_missing: bool = False,
        ) -> Queue: ...
        async def aio(self, *args, **kwargs) -> Queue: ...

    lookup: __lookup_spec

    class __delete_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            *,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
        ): ...
        async def aio(self, *args, **kwargs): ...

    delete: __delete_spec

    class ___get_nonblocking_spec(typing_extensions.Protocol):
        def __call__(self, partition: typing.Union[str, None], n_values: int) -> typing.List[typing.Any]: ...
        async def aio(self, *args, **kwargs) -> typing.List[typing.Any]: ...

    _get_nonblocking: ___get_nonblocking_spec

    class ___get_blocking_spec(typing_extensions.Protocol):
        def __call__(
            self, partition: typing.Union[str, None], timeout: typing.Union[float, None], n_values: int
        ) -> typing.List[typing.Any]: ...
        async def aio(self, *args, **kwargs) -> typing.List[typing.Any]: ...

    _get_blocking: ___get_blocking_spec

    class __clear_spec(typing_extensions.Protocol):
        def __call__(self, *, partition: typing.Union[str, None] = None, all: bool = False) -> None: ...
        async def aio(self, *args, **kwargs) -> None: ...

    clear: __clear_spec

    class __get_spec(typing_extensions.Protocol):
        def __call__(
            self,
            block: bool = True,
            timeout: typing.Union[float, None] = None,
            *,
            partition: typing.Union[str, None] = None,
        ) -> typing.Union[typing.Any, None]: ...
        async def aio(self, *args, **kwargs) -> typing.Union[typing.Any, None]: ...

    get: __get_spec

    class __get_many_spec(typing_extensions.Protocol):
        def __call__(
            self,
            n_values: int,
            block: bool = True,
            timeout: typing.Union[float, None] = None,
            *,
            partition: typing.Union[str, None] = None,
        ) -> typing.List[typing.Any]: ...
        async def aio(self, *args, **kwargs) -> typing.List[typing.Any]: ...

    get_many: __get_many_spec

    class __put_spec(typing_extensions.Protocol):
        def __call__(
            self,
            v: typing.Any,
            block: bool = True,
            timeout: typing.Union[float, None] = None,
            *,
            partition: typing.Union[str, None] = None,
            partition_ttl: int = 86400,
        ) -> None: ...
        async def aio(self, *args, **kwargs) -> None: ...

    put: __put_spec

    class __put_many_spec(typing_extensions.Protocol):
        def __call__(
            self,
            vs: typing.List[typing.Any],
            block: bool = True,
            timeout: typing.Union[float, None] = None,
            *,
            partition: typing.Union[str, None] = None,
            partition_ttl: int = 86400,
        ) -> None: ...
        async def aio(self, *args, **kwargs) -> None: ...

    put_many: __put_many_spec

    class ___put_many_blocking_spec(typing_extensions.Protocol):
        def __call__(
            self,
            partition: typing.Union[str, None],
            partition_ttl: int,
            vs: typing.List[typing.Any],
            timeout: typing.Union[float, None] = None,
        ): ...
        async def aio(self, *args, **kwargs): ...

    _put_many_blocking: ___put_many_blocking_spec

    class ___put_many_nonblocking_spec(typing_extensions.Protocol):
        def __call__(self, partition: typing.Union[str, None], partition_ttl: int, vs: typing.List[typing.Any]): ...
        async def aio(self, *args, **kwargs): ...

    _put_many_nonblocking: ___put_many_nonblocking_spec

    class __len_spec(typing_extensions.Protocol):
        def __call__(self, *, partition: typing.Union[str, None] = None, total: bool = False) -> int: ...
        async def aio(self, *args, **kwargs) -> int: ...

    len: __len_spec

    class __iterate_spec(typing_extensions.Protocol):
        def __call__(
            self, *, partition: typing.Union[str, None] = None, item_poll_timeout: float = 0.0
        ) -> typing.Generator[typing.Any, None, None]: ...
        def aio(
            self, *, partition: typing.Union[str, None] = None, item_poll_timeout: float = 0.0
        ) -> typing.AsyncGenerator[typing.Any, None]: ...

    iterate: __iterate_spec

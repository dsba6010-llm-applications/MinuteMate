import google.protobuf.message
import modal._resolver
import modal.client
import typing
import typing_extensions

O = typing.TypeVar("O", bound="_Object")

_BLOCKING_O = typing.TypeVar("_BLOCKING_O", bound="Object")

def _get_environment_name(
    environment_name: typing.Union[str, None], resolver: typing.Union[modal._resolver.Resolver, None] = None
) -> typing.Union[str, None]: ...

class _Object:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _load: typing.Union[
        typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None
    ]
    _preload: typing.Union[
        typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None
    ]
    _rep: str
    _is_another_app: bool
    _hydrate_lazily: bool
    _deps: typing.Union[typing.Callable[..., typing.List[_Object]], None]
    _deduplication_key: typing.Union[typing.Callable[[], typing.Awaitable[typing.Hashable]], None]
    _object_id: str
    _client: modal.client._Client
    _is_hydrated: bool

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None): ...
    def __init__(self, *args, **kwargs): ...
    def _init(
        self,
        rep: str,
        load: typing.Union[
            typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None
        ] = None,
        is_another_app: bool = False,
        preload: typing.Union[
            typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None
        ] = None,
        hydrate_lazily: bool = False,
        deps: typing.Union[typing.Callable[..., typing.List[_Object]], None] = None,
        deduplication_key: typing.Union[typing.Callable[[], typing.Awaitable[typing.Hashable]], None] = None,
    ): ...
    def _unhydrate(self): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other): ...
    def _hydrate(
        self,
        object_id: str,
        client: modal.client._Client,
        metadata: typing.Union[google.protobuf.message.Message, None],
    ): ...
    def _hydrate_metadata(self, metadata: typing.Union[google.protobuf.message.Message, None]): ...
    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]: ...
    def _init_from_other(self, other: O): ...
    def clone(self: O) -> O: ...
    @classmethod
    def _from_loader(
        cls,
        load: typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]],
        rep: str,
        is_another_app: bool = False,
        preload: typing.Union[
            typing.Callable[[O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]], None
        ] = None,
        hydrate_lazily: bool = False,
        deps: typing.Union[typing.Callable[..., typing.Sequence[_Object]], None] = None,
        deduplication_key: typing.Union[typing.Callable[[], typing.Awaitable[typing.Hashable]], None] = None,
    ): ...
    @classmethod
    def _new_hydrated(
        cls: typing.Type[O],
        object_id: str,
        client: modal.client._Client,
        handle_metadata: typing.Union[google.protobuf.message.Message, None],
        is_another_app: bool = False,
    ) -> O: ...
    def _hydrate_from_other(self, other: O): ...
    def __repr__(self): ...
    @property
    def local_uuid(self): ...
    @property
    def object_id(self): ...
    @property
    def is_hydrated(self) -> bool: ...
    @property
    def deps(self) -> typing.Callable[..., typing.List[_Object]]: ...
    async def resolve(self): ...

class Object:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _load: typing.Union[typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None]
    _preload: typing.Union[
        typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None
    ]
    _rep: str
    _is_another_app: bool
    _hydrate_lazily: bool
    _deps: typing.Union[typing.Callable[..., typing.List[Object]], None]
    _deduplication_key: typing.Union[typing.Callable[[], typing.Hashable], None]
    _object_id: str
    _client: modal.client.Client
    _is_hydrated: bool

    def __init__(self, *args, **kwargs): ...
    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None): ...

    class ___init_spec(typing_extensions.Protocol):
        def __call__(
            self,
            rep: str,
            load: typing.Union[
                typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None
            ] = None,
            is_another_app: bool = False,
            preload: typing.Union[
                typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None
            ] = None,
            hydrate_lazily: bool = False,
            deps: typing.Union[typing.Callable[..., typing.List[Object]], None] = None,
            deduplication_key: typing.Union[typing.Callable[[], typing.Hashable], None] = None,
        ): ...
        def aio(
            self,
            rep: str,
            load: typing.Union[
                typing.Callable[
                    [_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]
                ],
                None,
            ] = None,
            is_another_app: bool = False,
            preload: typing.Union[
                typing.Callable[
                    [_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], typing.Awaitable[None]
                ],
                None,
            ] = None,
            hydrate_lazily: bool = False,
            deps: typing.Union[typing.Callable[..., typing.List[Object]], None] = None,
            deduplication_key: typing.Union[typing.Callable[[], typing.Awaitable[typing.Hashable]], None] = None,
        ): ...

    _init: ___init_spec

    def _unhydrate(self): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other): ...
    def _hydrate(
        self, object_id: str, client: modal.client.Client, metadata: typing.Union[google.protobuf.message.Message, None]
    ): ...
    def _hydrate_metadata(self, metadata: typing.Union[google.protobuf.message.Message, None]): ...
    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]: ...
    def _init_from_other(self, other: _BLOCKING_O): ...
    def clone(self: _BLOCKING_O) -> _BLOCKING_O: ...
    @classmethod
    def _from_loader(
        cls,
        load: typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None],
        rep: str,
        is_another_app: bool = False,
        preload: typing.Union[
            typing.Callable[[_BLOCKING_O, modal._resolver.Resolver, typing.Union[str, None]], None], None
        ] = None,
        hydrate_lazily: bool = False,
        deps: typing.Union[typing.Callable[..., typing.Sequence[Object]], None] = None,
        deduplication_key: typing.Union[typing.Callable[[], typing.Hashable], None] = None,
    ): ...
    @classmethod
    def _new_hydrated(
        cls: typing.Type[_BLOCKING_O],
        object_id: str,
        client: modal.client.Client,
        handle_metadata: typing.Union[google.protobuf.message.Message, None],
        is_another_app: bool = False,
    ) -> _BLOCKING_O: ...
    def _hydrate_from_other(self, other: _BLOCKING_O): ...
    def __repr__(self): ...
    @property
    def local_uuid(self): ...
    @property
    def object_id(self): ...
    @property
    def is_hydrated(self) -> bool: ...
    @property
    def deps(self) -> typing.Callable[..., typing.List[Object]]: ...

    class __resolve_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    resolve: __resolve_spec

def live_method(method): ...
def live_method_gen(method): ...

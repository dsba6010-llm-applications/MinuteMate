import google.protobuf.message
import modal._output
import modal.app
import modal.client
import modal.functions
import modal.gpu
import modal.object
import modal.partial_function
import modal.retries
import modal.secret
import modal.volume
import modal_proto.api_pb2
import os
import typing
import typing_extensions

T = typing.TypeVar("T")

class _Obj:
    _functions: typing.Dict[str, modal.functions._Function]
    _inited: bool
    _entered: bool
    _user_cls_instance: typing.Union[typing.Any, None]
    _user_cls_instance_constr: typing.Union[typing.Callable[[], typing.Any], None]
    _instance_service_function: typing.Union[modal.functions._Function, None]

    def _uses_common_service_function(self): ...
    def __init__(
        self,
        user_cls: type,
        output_mgr: typing.Union[modal._output.OutputManager, None],
        class_service_function: typing.Union[modal.functions._Function, None],
        classbound_methods: typing.Dict[str, modal.functions._Function],
        from_other_workspace: bool,
        options: typing.Union[modal_proto.api_pb2.FunctionOptions, None],
        args,
        kwargs,
    ): ...
    async def keep_warm(self, warm_pool_size: int) -> None: ...
    def _create_user_cls_instance(self) -> typing.Any: ...
    def _get_user_cls_instance(self): ...
    def enter(self): ...
    @property
    def entered(self): ...
    @entered.setter
    def entered(self, val): ...
    async def aenter(self): ...
    def __getattr__(self, k): ...

class Obj:
    _functions: typing.Dict[str, modal.functions.Function]
    _inited: bool
    _entered: bool
    _user_cls_instance: typing.Union[typing.Any, None]
    _user_cls_instance_constr: typing.Union[typing.Callable[[], typing.Any], None]
    _instance_service_function: typing.Union[modal.functions.Function, None]

    def __init__(
        self,
        user_cls: type,
        output_mgr: typing.Union[modal._output.OutputManager, None],
        class_service_function: typing.Union[modal.functions.Function, None],
        classbound_methods: typing.Dict[str, modal.functions.Function],
        from_other_workspace: bool,
        options: typing.Union[modal_proto.api_pb2.FunctionOptions, None],
        args,
        kwargs,
    ): ...
    def _uses_common_service_function(self): ...

    class __keep_warm_spec(typing_extensions.Protocol):
        def __call__(self, warm_pool_size: int) -> None: ...
        async def aio(self, *args, **kwargs) -> None: ...

    keep_warm: __keep_warm_spec

    def _create_user_cls_instance(self) -> typing.Any: ...
    def _get_user_cls_instance(self): ...
    def enter(self): ...
    @property
    def entered(self): ...
    @entered.setter
    def entered(self, val): ...
    async def aenter(self): ...
    def __getattr__(self, k): ...

class _Cls(modal.object._Object):
    _user_cls: typing.Union[type, None]
    _class_service_function: typing.Union[modal.functions._Function, None]
    _method_functions: typing.Dict[str, modal.functions._Function]
    _options: typing.Union[modal_proto.api_pb2.FunctionOptions, None]
    _callables: typing.Dict[str, typing.Callable]
    _from_other_workspace: typing.Union[bool, None]
    _app: typing.Union[modal.app._App, None]

    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other: _Cls): ...
    def _set_output_mgr(self, output_mgr: modal._output.OutputManager): ...
    def _get_partial_functions(self) -> typing.Dict[str, modal.partial_function._PartialFunction]: ...
    def _hydrate_metadata(self, metadata: google.protobuf.message.Message): ...
    def _get_metadata(self) -> modal_proto.api_pb2.ClassHandleMetadata: ...
    @staticmethod
    def from_local(user_cls, app: modal.app._App, class_service_function: modal.functions._Function) -> _Cls: ...
    def _uses_common_service_function(self): ...
    @classmethod
    def from_name(
        cls: typing.Type[_Cls],
        app_name: str,
        tag: typing.Union[str, None] = None,
        namespace=1,
        environment_name: typing.Union[str, None] = None,
        workspace: typing.Union[str, None] = None,
    ) -> _Cls: ...
    def with_options(
        self: _Cls,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        secrets: typing.Collection[modal.secret._Secret] = (),
        volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume._Volume] = {},
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Union[int, None] = None,
        concurrency_limit: typing.Union[int, None] = None,
        allow_concurrent_inputs: typing.Union[int, None] = None,
        container_idle_timeout: typing.Union[int, None] = None,
        allow_background_volume_commits: typing.Union[bool, None] = None,
    ) -> _Cls: ...
    @staticmethod
    async def lookup(
        app_name: str,
        tag: typing.Union[str, None] = None,
        namespace=1,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        workspace: typing.Union[str, None] = None,
    ) -> _Cls: ...
    def __call__(self, *args, **kwargs) -> _Obj: ...
    def __getattr__(self, k): ...

class Cls(modal.object.Object):
    _user_cls: typing.Union[type, None]
    _class_service_function: typing.Union[modal.functions.Function, None]
    _method_functions: typing.Dict[str, modal.functions.Function]
    _options: typing.Union[modal_proto.api_pb2.FunctionOptions, None]
    _callables: typing.Dict[str, typing.Callable]
    _from_other_workspace: typing.Union[bool, None]
    _app: typing.Union[modal.app.App, None]

    def __init__(self, *args, **kwargs): ...
    def _initialize_from_empty(self): ...
    def _initialize_from_other(self, other: Cls): ...
    def _set_output_mgr(self, output_mgr: modal._output.OutputManager): ...
    def _get_partial_functions(self) -> typing.Dict[str, modal.partial_function.PartialFunction]: ...
    def _hydrate_metadata(self, metadata: google.protobuf.message.Message): ...
    def _get_metadata(self) -> modal_proto.api_pb2.ClassHandleMetadata: ...
    @staticmethod
    def from_local(user_cls, app: modal.app.App, class_service_function: modal.functions.Function) -> Cls: ...
    def _uses_common_service_function(self): ...
    @classmethod
    def from_name(
        cls: typing.Type[Cls],
        app_name: str,
        tag: typing.Union[str, None] = None,
        namespace=1,
        environment_name: typing.Union[str, None] = None,
        workspace: typing.Union[str, None] = None,
    ) -> Cls: ...
    def with_options(
        self: Cls,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        secrets: typing.Collection[modal.secret.Secret] = (),
        volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume.Volume] = {},
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        timeout: typing.Union[int, None] = None,
        concurrency_limit: typing.Union[int, None] = None,
        allow_concurrent_inputs: typing.Union[int, None] = None,
        container_idle_timeout: typing.Union[int, None] = None,
        allow_background_volume_commits: typing.Union[bool, None] = None,
    ) -> Cls: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            app_name: str,
            tag: typing.Union[str, None] = None,
            namespace=1,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
            workspace: typing.Union[str, None] = None,
        ) -> Cls: ...
        async def aio(self, *args, **kwargs) -> Cls: ...

    lookup: __lookup_spec

    def __call__(self, *args, **kwargs) -> Obj: ...
    def __getattr__(self, k): ...

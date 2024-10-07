import _io
import modal._output
import modal._utils.function_utils
import modal.client
import modal.cloud_bucket_mount
import modal.cls
import modal.functions
import modal.gpu
import modal.image
import modal.mount
import modal.network_file_system
import modal.object
import modal.proxy
import modal.retries
import modal.running_app
import modal.sandbox
import modal.schedule
import modal.scheduler_placement
import modal.secret
import modal.volume
import modal_proto.api_pb2
import pathlib
import synchronicity.combined_types
import typing
import typing_extensions

class _LocalEntrypoint:
    _info: modal._utils.function_utils.FunctionInfo
    _app: _App

    def __init__(self, info: modal._utils.function_utils.FunctionInfo, app: _App) -> None: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def app(self) -> _App: ...
    @property
    def stub(self) -> _App: ...

class LocalEntrypoint:
    _info: modal._utils.function_utils.FunctionInfo
    _app: App

    def __init__(self, info: modal._utils.function_utils.FunctionInfo, app: App) -> None: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...
    @property
    def info(self) -> modal._utils.function_utils.FunctionInfo: ...
    @property
    def app(self) -> App: ...
    @property
    def stub(self) -> App: ...

def check_sequence(items: typing.Sequence[typing.Any], item_type: typing.Type[typing.Any], error_msg: str) -> None: ...

CLS_T = typing.TypeVar("CLS_T", bound="typing.Type")

class _App:
    _name: typing.Union[str, None]
    _description: typing.Union[str, None]
    _indexed_objects: typing.Dict[str, modal.object._Object]
    _function_mounts: typing.Dict[str, modal.mount._Mount]
    _image: typing.Union[modal.image._Image, None]
    _mounts: typing.Sequence[modal.mount._Mount]
    _secrets: typing.Sequence[modal.secret._Secret]
    _volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume]
    _web_endpoints: typing.List[str]
    _local_entrypoints: typing.Dict[str, _LocalEntrypoint]
    _running_app: typing.Union[modal.running_app.RunningApp, None]
    _client: typing.Union[modal.client._Client, None]
    _all_apps: typing.ClassVar[typing.Dict[typing.Union[str, None], typing.List[_App]]]

    def __init__(
        self,
        name: typing.Union[str, None] = None,
        *,
        image: typing.Union[modal.image._Image, None] = None,
        mounts: typing.Sequence[modal.mount._Mount] = [],
        secrets: typing.Sequence[modal.secret._Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume] = {},
    ) -> None: ...
    @property
    def name(self) -> typing.Union[str, None]: ...
    @property
    def is_interactive(self) -> bool: ...
    @property
    def app_id(self) -> typing.Union[str, None]: ...
    @property
    def description(self) -> typing.Union[str, None]: ...
    def set_description(self, description: str): ...
    def _validate_blueprint_value(self, key: str, value: typing.Any): ...
    def _add_object(self, tag, obj): ...
    def __getitem__(self, tag: str): ...
    def __setitem__(self, tag: str, obj: modal.object._Object): ...
    def __getattr__(self, tag: str): ...
    def __setattr__(self, tag: str, obj: modal.object._Object): ...
    @property
    def image(self) -> modal.image._Image: ...
    @image.setter
    def image(self, value): ...
    def _uncreate_all_objects(self): ...
    def is_inside(self, image: typing.Union[modal.image._Image, None] = None): ...
    def _set_local_app(
        self, client: modal.client._Client, app: modal.running_app.RunningApp
    ) -> typing.AsyncContextManager[None]: ...
    def run(
        self,
        client: typing.Union[modal.client._Client, None] = None,
        stdout: typing.Union[_io.TextIOWrapper, None] = None,
        show_progress: bool = True,
        detach: bool = False,
        output_mgr: typing.Union[modal._output.OutputManager, None] = None,
    ) -> typing.AsyncContextManager[_App]: ...
    def _get_default_image(self): ...
    def _get_watch_mounts(self): ...
    def _add_function(self, function: modal.functions._Function, is_web_endpoint: bool): ...
    def _init_container(self, client: modal.client._Client, running_app: modal.running_app.RunningApp): ...
    @property
    def registered_functions(self) -> typing.Dict[str, modal.functions._Function]: ...
    @property
    def registered_classes(self) -> typing.Dict[str, modal.functions._Function]: ...
    @property
    def registered_entrypoints(self) -> typing.Dict[str, _LocalEntrypoint]: ...
    @property
    def indexed_objects(self) -> typing.Dict[str, modal.object._Object]: ...
    @property
    def registered_web_endpoints(self) -> typing.List[str]: ...
    def local_entrypoint(
        self, _warn_parentheses_missing: typing.Any = None, *, name: typing.Union[str, None] = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], None]: ...
    def function(
        self,
        _warn_parentheses_missing: typing.Any = None,
        *,
        image: typing.Union[modal.image._Image, None] = None,
        schedule: typing.Union[modal.schedule.Schedule, None] = None,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Union[int, None] = None,
        proxy: typing.Union[modal.proxy._Proxy, None] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Union[int, None] = None,
        allow_concurrent_inputs: typing.Union[int, None] = None,
        container_idle_timeout: typing.Union[int, None] = None,
        timeout: typing.Union[int, None] = None,
        keep_warm: typing.Union[int, None] = None,
        name: typing.Union[str, None] = None,
        is_generator: typing.Union[bool, None] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        checkpointing_enabled: typing.Union[bool, None] = None,
        block_network: bool = False,
        max_inputs: typing.Union[int, None] = None,
        interactive: bool = False,
        secret: typing.Union[modal.secret._Secret, None] = None,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        _experimental_boost: bool = False,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> typing.Callable[..., modal.functions._Function]: ...
    def cls(
        self,
        _warn_parentheses_missing: typing.Union[bool, None] = None,
        *,
        image: typing.Union[modal.image._Image, None] = None,
        secrets: typing.Sequence[modal.secret._Secret] = (),
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Union[int, None] = None,
        proxy: typing.Union[modal.proxy._Proxy, None] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Union[int, None] = None,
        allow_concurrent_inputs: typing.Union[int, None] = None,
        container_idle_timeout: typing.Union[int, None] = None,
        timeout: typing.Union[int, None] = None,
        keep_warm: typing.Union[int, None] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        checkpointing_enabled: typing.Union[bool, None] = None,
        block_network: bool = False,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        max_inputs: typing.Union[int, None] = None,
        interactive: bool = False,
        secret: typing.Union[modal.secret._Secret, None] = None,
        _experimental_boost: bool = False,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> typing.Callable[[CLS_T], modal.cls._Cls]: ...
    async def spawn_sandbox(
        self,
        *entrypoint_args: str,
        image: typing.Union[modal.image._Image, None] = None,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        secrets: typing.Sequence[modal.secret._Secret] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system._NetworkFileSystem
        ] = {},
        timeout: typing.Union[int, None] = None,
        workdir: typing.Union[str, None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        pty_info: typing.Union[modal_proto.api_pb2.PTYInfo, None] = None,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
    ) -> modal.sandbox._Sandbox: ...
    def include(self, /, other_app: _App): ...

class App:
    _name: typing.Union[str, None]
    _description: typing.Union[str, None]
    _indexed_objects: typing.Dict[str, modal.object.Object]
    _function_mounts: typing.Dict[str, modal.mount.Mount]
    _image: typing.Union[modal.image.Image, None]
    _mounts: typing.Sequence[modal.mount.Mount]
    _secrets: typing.Sequence[modal.secret.Secret]
    _volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume]
    _web_endpoints: typing.List[str]
    _local_entrypoints: typing.Dict[str, LocalEntrypoint]
    _running_app: typing.Union[modal.running_app.RunningApp, None]
    _client: typing.Union[modal.client.Client, None]
    _all_apps: typing.ClassVar[typing.Dict[typing.Union[str, None], typing.List[App]]]

    def __init__(
        self,
        name: typing.Union[str, None] = None,
        *,
        image: typing.Union[modal.image.Image, None] = None,
        mounts: typing.Sequence[modal.mount.Mount] = [],
        secrets: typing.Sequence[modal.secret.Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume] = {},
    ) -> None: ...
    @property
    def name(self) -> typing.Union[str, None]: ...
    @property
    def is_interactive(self) -> bool: ...
    @property
    def app_id(self) -> typing.Union[str, None]: ...
    @property
    def description(self) -> typing.Union[str, None]: ...
    def set_description(self, description: str): ...
    def _validate_blueprint_value(self, key: str, value: typing.Any): ...
    def _add_object(self, tag, obj): ...
    def __getitem__(self, tag: str): ...
    def __setitem__(self, tag: str, obj: modal.object.Object): ...
    def __getattr__(self, tag: str): ...
    def __setattr__(self, tag: str, obj: modal.object.Object): ...
    @property
    def image(self) -> modal.image.Image: ...
    @image.setter
    def image(self, value): ...
    def _uncreate_all_objects(self): ...
    def is_inside(self, image: typing.Union[modal.image.Image, None] = None): ...

    class ___set_local_app_spec(typing_extensions.Protocol):
        def __call__(
            self, client: modal.client.Client, app: modal.running_app.RunningApp
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]: ...
        def aio(
            self, client: modal.client.Client, app: modal.running_app.RunningApp
        ) -> typing.AsyncContextManager[None]: ...

    _set_local_app: ___set_local_app_spec

    class __run_spec(typing_extensions.Protocol):
        def __call__(
            self,
            client: typing.Union[modal.client.Client, None] = None,
            stdout: typing.Union[_io.TextIOWrapper, None] = None,
            show_progress: bool = True,
            detach: bool = False,
            output_mgr: typing.Union[modal._output.OutputManager, None] = None,
        ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[App]: ...
        def aio(
            self,
            client: typing.Union[modal.client.Client, None] = None,
            stdout: typing.Union[_io.TextIOWrapper, None] = None,
            show_progress: bool = True,
            detach: bool = False,
            output_mgr: typing.Union[modal._output.OutputManager, None] = None,
        ) -> typing.AsyncContextManager[App]: ...

    run: __run_spec

    def _get_default_image(self): ...
    def _get_watch_mounts(self): ...
    def _add_function(self, function: modal.functions.Function, is_web_endpoint: bool): ...
    def _init_container(self, client: modal.client.Client, running_app: modal.running_app.RunningApp): ...
    @property
    def registered_functions(self) -> typing.Dict[str, modal.functions.Function]: ...
    @property
    def registered_classes(self) -> typing.Dict[str, modal.functions.Function]: ...
    @property
    def registered_entrypoints(self) -> typing.Dict[str, LocalEntrypoint]: ...
    @property
    def indexed_objects(self) -> typing.Dict[str, modal.object.Object]: ...
    @property
    def registered_web_endpoints(self) -> typing.List[str]: ...
    def local_entrypoint(
        self, _warn_parentheses_missing: typing.Any = None, *, name: typing.Union[str, None] = None
    ) -> typing.Callable[[typing.Callable[..., typing.Any]], None]: ...
    def function(
        self,
        _warn_parentheses_missing: typing.Any = None,
        *,
        image: typing.Union[modal.image.Image, None] = None,
        schedule: typing.Union[modal.schedule.Schedule, None] = None,
        secrets: typing.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount.Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Union[int, None] = None,
        proxy: typing.Union[modal.proxy.Proxy, None] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Union[int, None] = None,
        allow_concurrent_inputs: typing.Union[int, None] = None,
        container_idle_timeout: typing.Union[int, None] = None,
        timeout: typing.Union[int, None] = None,
        keep_warm: typing.Union[int, None] = None,
        name: typing.Union[str, None] = None,
        is_generator: typing.Union[bool, None] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        checkpointing_enabled: typing.Union[bool, None] = None,
        block_network: bool = False,
        max_inputs: typing.Union[int, None] = None,
        interactive: bool = False,
        secret: typing.Union[modal.secret.Secret, None] = None,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        _experimental_boost: bool = False,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> typing.Callable[..., modal.functions.Function]: ...
    def cls(
        self,
        _warn_parentheses_missing: typing.Union[bool, None] = None,
        *,
        image: typing.Union[modal.image.Image, None] = None,
        secrets: typing.Sequence[modal.secret.Secret] = (),
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        serialized: bool = False,
        mounts: typing.Sequence[modal.mount.Mount] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
        ] = {},
        volumes: typing.Dict[
            typing.Union[str, pathlib.PurePosixPath],
            typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
        ] = {},
        allow_cross_region_volumes: bool = False,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        ephemeral_disk: typing.Union[int, None] = None,
        proxy: typing.Union[modal.proxy.Proxy, None] = None,
        retries: typing.Union[int, modal.retries.Retries, None] = None,
        concurrency_limit: typing.Union[int, None] = None,
        allow_concurrent_inputs: typing.Union[int, None] = None,
        container_idle_timeout: typing.Union[int, None] = None,
        timeout: typing.Union[int, None] = None,
        keep_warm: typing.Union[int, None] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        enable_memory_snapshot: bool = False,
        checkpointing_enabled: typing.Union[bool, None] = None,
        block_network: bool = False,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        max_inputs: typing.Union[int, None] = None,
        interactive: bool = False,
        secret: typing.Union[modal.secret.Secret, None] = None,
        _experimental_boost: bool = False,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> typing.Callable[[CLS_T], modal.cls.Cls]: ...

    class __spawn_sandbox_spec(typing_extensions.Protocol):
        def __call__(
            self,
            *entrypoint_args: str,
            image: typing.Union[modal.image.Image, None] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, pathlib.PurePosixPath], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Union[int, None] = None,
            workdir: typing.Union[str, None] = None,
            gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Union[str, None] = None,
            region: typing.Union[str, typing.Sequence[str], None] = None,
            cpu: typing.Union[float, None] = None,
            memory: typing.Union[int, typing.Tuple[int, int], None] = None,
            block_network: bool = False,
            volumes: typing.Dict[
                typing.Union[str, pathlib.PurePosixPath],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            _allow_background_volume_commits: typing.Union[bool, None] = None,
            pty_info: typing.Union[modal_proto.api_pb2.PTYInfo, None] = None,
            _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        ) -> modal.sandbox.Sandbox: ...
        async def aio(self, *args, **kwargs) -> modal.sandbox.Sandbox: ...

    spawn_sandbox: __spawn_sandbox_spec

    def include(self, other_app: App): ...

class _Stub(_App):
    @staticmethod
    def __new__(
        cls,
        name: typing.Union[str, None] = None,
        *,
        image: typing.Union[modal.image._Image, None] = None,
        mounts: typing.Sequence[modal.mount._Mount] = [],
        secrets: typing.Sequence[modal.secret._Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume._Volume] = {},
    ): ...

class Stub(App):
    def __init__(
        self,
        name: typing.Union[str, None] = None,
        *,
        image: typing.Union[modal.image.Image, None] = None,
        mounts: typing.Sequence[modal.mount.Mount] = [],
        secrets: typing.Sequence[modal.secret.Secret] = [],
        volumes: typing.Dict[typing.Union[str, pathlib.PurePosixPath], modal.volume.Volume] = {},
    ) -> None: ...

_default_image: modal.image._Image

import google.protobuf.message
import modal.app
import modal.client
import modal.cloud_bucket_mount
import modal.gpu
import modal.image
import modal.mount
import modal.network_file_system
import modal.object
import modal.scheduler_placement
import modal.secret
import modal.volume
import modal_proto.api_pb2
import os
import typing
import typing_extensions

class _LogsReader:
    def __init__(self, file_descriptor: int, sandbox_id: str, client: modal.client._Client) -> None: ...
    async def read(self) -> str: ...
    def _get_logs(self) -> typing.AsyncIterator[typing.Union[modal_proto.api_pb2.TaskLogs, None]]: ...
    def __aiter__(self): ...
    async def __anext__(self): ...

class _StreamWriter:
    def __init__(self, sandbox_id: str, client: modal.client._Client): ...
    def get_next_index(self): ...
    def write(self, data: typing.Union[bytes, bytearray, memoryview]): ...
    def write_eof(self): ...
    async def drain(self): ...

class LogsReader:
    def __init__(self, file_descriptor: int, sandbox_id: str, client: modal.client.Client) -> None: ...

    class __read_spec(typing_extensions.Protocol):
        def __call__(self) -> str: ...
        async def aio(self, *args, **kwargs) -> str: ...

    read: __read_spec

    class ___get_logs_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Iterator[typing.Union[modal_proto.api_pb2.TaskLogs, None]]: ...
        def aio(self) -> typing.AsyncIterator[typing.Union[modal_proto.api_pb2.TaskLogs, None]]: ...

    _get_logs: ___get_logs_spec

    def __iter__(self): ...
    def __aiter__(self): ...
    def __next__(self): ...
    async def __anext__(self, *args, **kwargs): ...

class StreamWriter:
    def __init__(self, sandbox_id: str, client: modal.client.Client): ...
    def get_next_index(self): ...
    def write(self, data: typing.Union[bytes, bytearray, memoryview]): ...
    def write_eof(self): ...

    class __drain_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    drain: __drain_spec

class _Sandbox(modal.object._Object):
    _result: typing.Union[modal_proto.api_pb2.GenericResult, None]
    _stdout: _LogsReader
    _stderr: _LogsReader
    _stdin: _StreamWriter

    @staticmethod
    def _new(
        entrypoint_args: typing.Sequence[str],
        image: modal.image._Image,
        mounts: typing.Sequence[modal.mount._Mount],
        secrets: typing.Sequence[modal.secret._Secret],
        timeout: typing.Union[int, None] = None,
        workdir: typing.Union[str, None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem
        ] = {},
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Union[modal_proto.api_pb2.PTYInfo, None] = None,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> _Sandbox: ...
    @staticmethod
    async def create(
        *entrypoint_args: str,
        app: typing.Union[modal.app._App, None] = None,
        environment_name: typing.Union[str, None] = None,
        image: typing.Union[modal.image._Image, None] = None,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        secrets: typing.Sequence[modal.secret._Secret] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem
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
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Union[modal_proto.api_pb2.PTYInfo, None] = None,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        client: typing.Union[modal.client._Client, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> _Sandbox: ...
    def _hydrate_metadata(self, handle_metadata: typing.Union[google.protobuf.message.Message, None]): ...
    @staticmethod
    async def from_id(sandbox_id: str, client: typing.Union[modal.client._Client, None] = None) -> _Sandbox: ...
    async def wait(self, raise_on_termination: bool = True): ...
    async def terminate(self): ...
    async def poll(self) -> typing.Union[int, None]: ...
    @property
    def stdout(self) -> _LogsReader: ...
    @property
    def stderr(self) -> _LogsReader: ...
    @property
    def stdin(self) -> _StreamWriter: ...
    @property
    def returncode(self) -> typing.Union[int, None]: ...

class Sandbox(modal.object.Object):
    _result: typing.Union[modal_proto.api_pb2.GenericResult, None]
    _stdout: LogsReader
    _stderr: LogsReader
    _stdin: StreamWriter

    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def _new(
        entrypoint_args: typing.Sequence[str],
        image: modal.image.Image,
        mounts: typing.Sequence[modal.mount.Mount],
        secrets: typing.Sequence[modal.secret.Secret],
        timeout: typing.Union[int, None] = None,
        workdir: typing.Union[str, None] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Union[str, None] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Union[float, None] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
        ] = {},
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike], typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount]
        ] = {},
        pty_info: typing.Union[modal_proto.api_pb2.PTYInfo, None] = None,
        _allow_background_volume_commits: typing.Union[bool, None] = None,
        _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> Sandbox: ...

    class __create_spec(typing_extensions.Protocol):
        def __call__(
            self,
            *entrypoint_args: str,
            app: typing.Union[modal.app.App, None] = None,
            environment_name: typing.Union[str, None] = None,
            image: typing.Union[modal.image.Image, None] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
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
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Union[modal_proto.api_pb2.PTYInfo, None] = None,
            _allow_background_volume_commits: typing.Union[bool, None] = None,
            _experimental_scheduler_placement: typing.Union[modal.scheduler_placement.SchedulerPlacement, None] = None,
            client: typing.Union[modal.client.Client, None] = None,
            _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
        ) -> Sandbox: ...
        async def aio(self, *args, **kwargs) -> Sandbox: ...

    create: __create_spec

    def _hydrate_metadata(self, handle_metadata: typing.Union[google.protobuf.message.Message, None]): ...

    class __from_id_spec(typing_extensions.Protocol):
        def __call__(self, sandbox_id: str, client: typing.Union[modal.client.Client, None] = None) -> Sandbox: ...
        async def aio(self, *args, **kwargs) -> Sandbox: ...

    from_id: __from_id_spec

    class __wait_spec(typing_extensions.Protocol):
        def __call__(self, raise_on_termination: bool = True): ...
        async def aio(self, *args, **kwargs): ...

    wait: __wait_spec

    class __terminate_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    terminate: __terminate_spec

    class __poll_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Union[int, None]: ...
        async def aio(self, *args, **kwargs) -> typing.Union[int, None]: ...

    poll: __poll_spec

    @property
    def stdout(self) -> LogsReader: ...
    @property
    def stderr(self) -> LogsReader: ...
    @property
    def stdin(self) -> StreamWriter: ...
    @property
    def returncode(self) -> typing.Union[int, None]: ...

_default_image: modal.image._Image

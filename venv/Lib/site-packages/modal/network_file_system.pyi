import modal.client
import modal.object
import modal.volume
import modal_proto.api_pb2
import pathlib
import synchronicity.combined_types
import typing
import typing_extensions

def network_file_system_mount_protos(
    validated_network_file_systems: typing.List[typing.Tuple[str, _NetworkFileSystem]], allow_cross_region_volumes: bool
) -> typing.List[modal_proto.api_pb2.SharedVolumeMount]: ...

class _NetworkFileSystem(modal.object._Object):
    @staticmethod
    def new(cloud: typing.Union[str, None] = None): ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Union[str, None] = None, create_if_missing: bool = False
    ) -> _NetworkFileSystem: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[_NetworkFileSystem],
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        _heartbeat_sleep: float = 300,
    ) -> typing.AsyncContextManager[_NetworkFileSystem]: ...
    @staticmethod
    def persisted(
        label: str, namespace=1, environment_name: typing.Union[str, None] = None, cloud: typing.Union[str, None] = None
    ): ...
    def persist(
        self,
        label: str,
        namespace=1,
        environment_name: typing.Union[str, None] = None,
        cloud: typing.Union[str, None] = None,
    ): ...
    @staticmethod
    async def lookup(
        label: str,
        namespace=1,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        create_if_missing: bool = False,
    ) -> _NetworkFileSystem: ...
    @staticmethod
    async def create_deployed(
        deployment_name: str,
        namespace=1,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
    ) -> str: ...
    async def write_file(self, remote_path: str, fp: typing.BinaryIO) -> int: ...
    def read_file(self, path: str) -> typing.AsyncIterator[bytes]: ...
    def iterdir(self, path: str) -> typing.AsyncIterator[modal.volume.FileEntry]: ...
    async def add_local_file(
        self,
        local_path: typing.Union[pathlib.Path, str],
        remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None,
    ): ...
    async def add_local_dir(
        self,
        local_path: typing.Union[pathlib.Path, str],
        remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None,
    ): ...
    async def listdir(self, path: str) -> typing.List[modal.volume.FileEntry]: ...
    async def remove_file(self, path: str, recursive=False): ...

class NetworkFileSystem(modal.object.Object):
    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def new(cloud: typing.Union[str, None] = None): ...
    @staticmethod
    def from_name(
        label: str, namespace=1, environment_name: typing.Union[str, None] = None, create_if_missing: bool = False
    ) -> NetworkFileSystem: ...
    @classmethod
    def ephemeral(
        cls: typing.Type[NetworkFileSystem],
        client: typing.Union[modal.client.Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        _heartbeat_sleep: float = 300,
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[NetworkFileSystem]: ...
    @staticmethod
    def persisted(
        label: str, namespace=1, environment_name: typing.Union[str, None] = None, cloud: typing.Union[str, None] = None
    ): ...
    def persist(
        self,
        label: str,
        namespace=1,
        environment_name: typing.Union[str, None] = None,
        cloud: typing.Union[str, None] = None,
    ): ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            namespace=1,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
            create_if_missing: bool = False,
        ) -> NetworkFileSystem: ...
        async def aio(self, *args, **kwargs) -> NetworkFileSystem: ...

    lookup: __lookup_spec

    class __create_deployed_spec(typing_extensions.Protocol):
        def __call__(
            self,
            deployment_name: str,
            namespace=1,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
        ) -> str: ...
        async def aio(self, *args, **kwargs) -> str: ...

    create_deployed: __create_deployed_spec

    class __write_file_spec(typing_extensions.Protocol):
        def __call__(self, remote_path: str, fp: typing.BinaryIO) -> int: ...
        async def aio(self, *args, **kwargs) -> int: ...

    write_file: __write_file_spec

    class __read_file_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.Iterator[bytes]: ...
        def aio(self, path: str) -> typing.AsyncIterator[bytes]: ...

    read_file: __read_file_spec

    class __iterdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.Iterator[modal.volume.FileEntry]: ...
        def aio(self, path: str) -> typing.AsyncIterator[modal.volume.FileEntry]: ...

    iterdir: __iterdir_spec

    class __add_local_file_spec(typing_extensions.Protocol):
        def __call__(
            self,
            local_path: typing.Union[pathlib.Path, str],
            remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None,
        ): ...
        async def aio(self, *args, **kwargs): ...

    add_local_file: __add_local_file_spec

    class __add_local_dir_spec(typing_extensions.Protocol):
        def __call__(
            self,
            local_path: typing.Union[pathlib.Path, str],
            remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None,
        ): ...
        async def aio(self, *args, **kwargs): ...

    add_local_dir: __add_local_dir_spec

    class __listdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.List[modal.volume.FileEntry]: ...
        async def aio(self, *args, **kwargs) -> typing.List[modal.volume.FileEntry]: ...

    listdir: __listdir_spec

    class __remove_file_spec(typing_extensions.Protocol):
        def __call__(self, path: str, recursive=False): ...
        async def aio(self, *args, **kwargs): ...

    remove_file: __remove_file_spec

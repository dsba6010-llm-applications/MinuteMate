import modal.client
import modal.object
import typing
import typing_extensions

class _Secret(modal.object._Object):
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, typing.Union[str, None]] = {}): ...
    @staticmethod
    def from_local_environ(env_keys: typing.List[str]): ...
    @staticmethod
    def from_dotenv(path=None, *, filename=".env"): ...
    @staticmethod
    def from_name(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> _Secret: ...
    @staticmethod
    async def lookup(
        label: str,
        namespace=1,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
    ) -> _Secret: ...
    @staticmethod
    async def create_deployed(
        deployment_name: str,
        env_dict: typing.Dict[str, str],
        namespace=1,
        client: typing.Union[modal.client._Client, None] = None,
        environment_name: typing.Union[str, None] = None,
        overwrite: bool = False,
    ) -> str: ...

class Secret(modal.object.Object):
    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def from_dict(env_dict: typing.Dict[str, typing.Union[str, None]] = {}): ...
    @staticmethod
    def from_local_environ(env_keys: typing.List[str]): ...
    @staticmethod
    def from_dotenv(path=None, *, filename=".env"): ...
    @staticmethod
    def from_name(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> Secret: ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            label: str,
            namespace=1,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
        ) -> Secret: ...
        async def aio(self, *args, **kwargs) -> Secret: ...

    lookup: __lookup_spec

    class __create_deployed_spec(typing_extensions.Protocol):
        def __call__(
            self,
            deployment_name: str,
            env_dict: typing.Dict[str, str],
            namespace=1,
            client: typing.Union[modal.client.Client, None] = None,
            environment_name: typing.Union[str, None] = None,
            overwrite: bool = False,
        ) -> str: ...
        async def aio(self, *args, **kwargs) -> str: ...

    create_deployed: __create_deployed_spec

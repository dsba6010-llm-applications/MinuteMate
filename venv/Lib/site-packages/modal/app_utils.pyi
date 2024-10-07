import modal.client
import modal_proto.api_pb2
import typing
import typing_extensions

async def _list_apps(
    env: typing.Union[str, None] = None, client: typing.Union[modal.client._Client, None] = None
) -> typing.List[modal_proto.api_pb2.AppStats]: ...

class __list_apps_spec(typing_extensions.Protocol):
    def __call__(
        self, env: typing.Union[str, None] = None, client: typing.Union[modal.client.Client, None] = None
    ) -> typing.List[modal_proto.api_pb2.AppStats]: ...
    async def aio(self, *args, **kwargs) -> typing.List[modal_proto.api_pb2.AppStats]: ...

list_apps: __list_apps_spec

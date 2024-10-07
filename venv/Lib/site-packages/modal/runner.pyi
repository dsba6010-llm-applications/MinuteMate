import _io
import modal._output
import modal.client
import modal.object
import modal.running_app
import multiprocessing.synchronize
import synchronicity.combined_types
import typing
import typing_extensions

_App = typing.TypeVar("_App")

async def _heartbeat(client: modal.client._Client, app_id: str) -> None: ...
async def _init_local_app_existing(
    client: modal.client._Client, existing_app_id: str
) -> modal.running_app.RunningApp: ...
async def _init_local_app_new(
    client: modal.client._Client,
    description: str,
    app_state: int,
    environment_name: str = "",
    interactive: bool = False,
) -> modal.running_app.RunningApp: ...
async def _init_local_app_from_name(
    client: modal.client._Client, name: str, namespace: typing.Any, environment_name: str = ""
) -> modal.running_app.RunningApp: ...
async def _create_all_objects(
    client: modal.client._Client,
    running_app: modal.running_app.RunningApp,
    indexed_objects: typing.Dict[str, modal.object._Object],
    new_app_state: int,
    environment_name: str,
    output_mgr: typing.Union[modal._output.OutputManager, None] = None,
) -> None: ...
async def _disconnect(
    client: modal.client._Client, app_id: str, reason: int, exc_str: typing.Union[str, None] = None
) -> None: ...
def _run_app(
    app: _App,
    client: typing.Union[modal.client._Client, None] = None,
    stdout: typing.Union[_io.TextIOWrapper, None] = None,
    show_progress: bool = True,
    detach: bool = False,
    output_mgr: typing.Union[modal._output.OutputManager, None] = None,
    environment_name: typing.Union[str, None] = None,
    shell: bool = False,
    interactive: bool = False,
) -> typing.AsyncContextManager[_App]: ...
async def _serve_update(
    app: _App, existing_app_id: str, is_ready: multiprocessing.synchronize.Event, environment_name: str
) -> None: ...

class DeployResult:
    app_id: str

    def __init__(self, app_id: str) -> None: ...
    def __repr__(self): ...
    def __eq__(self, other): ...
    def __setattr__(self, name, value): ...
    def __delattr__(self, name): ...
    def __hash__(self): ...

async def _deploy_app(
    app: _App,
    name: typing.Union[str, None] = None,
    namespace: typing.Any = 1,
    client: typing.Union[modal.client._Client, None] = None,
    stdout: typing.Union[_io.TextIOWrapper, None] = None,
    show_progress: bool = True,
    environment_name: typing.Union[str, None] = None,
    tag: typing.Union[str, None] = None,
) -> DeployResult: ...
async def _interactive_shell(
    _app: _App, cmds: typing.List[str], environment_name: str = "", **kwargs: typing.Any
) -> None: ...
def _run_stub(
    app: _App,
    client: typing.Union[modal.client._Client, None] = None,
    stdout: typing.Union[_io.TextIOWrapper, None] = None,
    show_progress: bool = True,
    detach: bool = False,
    output_mgr: typing.Union[modal._output.OutputManager, None] = None,
    environment_name: typing.Union[str, None] = None,
    shell: bool = False,
    interactive: bool = False,
) -> typing.AsyncGenerator[_App, None]: ...
def _deploy_stub(
    app: _App,
    name: typing.Union[str, None] = None,
    namespace: typing.Any = 1,
    client: typing.Union[modal.client._Client, None] = None,
    stdout: typing.Union[_io.TextIOWrapper, None] = None,
    show_progress: bool = True,
    environment_name: typing.Union[str, None] = None,
    tag: typing.Union[str, None] = None,
) -> typing.Coroutine[typing.Any, typing.Any, DeployResult]: ...

class __run_app_spec(typing_extensions.Protocol):
    def __call__(
        self,
        app: _App,
        client: typing.Union[modal.client.Client, None] = None,
        stdout: typing.Union[_io.TextIOWrapper, None] = None,
        show_progress: bool = True,
        detach: bool = False,
        output_mgr: typing.Union[modal._output.OutputManager, None] = None,
        environment_name: typing.Union[str, None] = None,
        shell: bool = False,
        interactive: bool = False,
    ) -> synchronicity.combined_types.AsyncAndBlockingContextManager[_App]: ...
    def aio(
        self,
        app: _App,
        client: typing.Union[modal.client.Client, None] = None,
        stdout: typing.Union[_io.TextIOWrapper, None] = None,
        show_progress: bool = True,
        detach: bool = False,
        output_mgr: typing.Union[modal._output.OutputManager, None] = None,
        environment_name: typing.Union[str, None] = None,
        shell: bool = False,
        interactive: bool = False,
    ) -> typing.AsyncContextManager[_App]: ...

run_app: __run_app_spec

class __serve_update_spec(typing_extensions.Protocol):
    def __call__(
        self, app: _App, existing_app_id: str, is_ready: multiprocessing.synchronize.Event, environment_name: str
    ) -> None: ...
    async def aio(self, *args, **kwargs) -> None: ...

serve_update: __serve_update_spec

class __deploy_app_spec(typing_extensions.Protocol):
    def __call__(
        self,
        app: _App,
        name: typing.Union[str, None] = None,
        namespace: typing.Any = 1,
        client: typing.Union[modal.client.Client, None] = None,
        stdout: typing.Union[_io.TextIOWrapper, None] = None,
        show_progress: bool = True,
        environment_name: typing.Union[str, None] = None,
        tag: typing.Union[str, None] = None,
    ) -> DeployResult: ...
    async def aio(self, *args, **kwargs) -> DeployResult: ...

deploy_app: __deploy_app_spec

class __interactive_shell_spec(typing_extensions.Protocol):
    def __call__(
        self, _app: _App, cmds: typing.List[str], environment_name: str = "", **kwargs: typing.Any
    ) -> None: ...
    async def aio(self, *args, **kwargs: typing.Any) -> None: ...

interactive_shell: __interactive_shell_spec

class __run_stub_spec(typing_extensions.Protocol):
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Generator[_App, None, None]: ...
    def aio(self, *args: typing.Any, **kwargs: typing.Any) -> typing.AsyncGenerator[_App, None]: ...

run_stub: __run_stub_spec

class __deploy_stub_spec(typing_extensions.Protocol):
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> DeployResult: ...
    def aio(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> typing.Coroutine[typing.Any, typing.Any, DeployResult]: ...

deploy_stub: __deploy_stub_spec

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, ContentSwitcher, Tabs, Tab, Label
from textual.widgets._header import HeaderClock
from textual.containers import (
    VerticalScroll,
    Horizontal,
    Vertical,
    Container as Group,
)
from textual.reactive import reactive
from kubernetes import client

from .logs import LogsButton
from .custom_widgets import CustomButton, ResponsiveGrid, ReactiveString
from .pods import PodsList


class AppGUI(App):
    CSS_PATH = "style.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, kclient: client, **kargs):
        self.kclient = kclient
        super().__init__(**kargs)

    def compose(self) -> ComposeResult:
        with Horizontal(id="header"):
            yield HeaderClock()
            yield Tabs(
                Tab("Containers", id="container-list"),
                Tab("Logs", id="container-logs"),
                id="nav",
            )
        yield Footer()
        with ContentSwitcher():
            yield ContainersList(self.kclient, id="container-list")
            yield VerticalScroll(id="container-logs")
            yield PodsList(self.kclient, id="image-list")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        self.query_one(ContentSwitcher).current = event.tab.id


class ContainersList(ResponsiveGrid):
    container_count = reactive(0)

    def __init__(self, kclient: client, **kargs):
        self.containers = []
        self.kclient = kclient
        super().__init__(**kargs)

    def on_mount(self) -> None:
        self.get_containers()
        self.set_interval(2, self.count_timer)

    def count_timer(self) -> None:
        self.get_containers()

    async def watch_container_count(self, count: int) -> None:
        await self.grid.remove_children()
        for c in self.containers:
            cw = ContainerWidget(c, self.kclient)  # type: ignore
            self.grid.mount(cw)

    @work(exclusive=True)
    def get_containers(self) -> None:
        self.containers = self.kclient.containers.list(all=True)
        self.container_count = len(self.containers)

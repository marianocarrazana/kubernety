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
from kubernetes.client.api.core_v1_api import CoreV1Api

from .pods import PodsList


class AppGUI(App):
    CSS_PATH = "style.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, kclient:CoreV1Api, **kargs):
        self.kclient = kclient
        super().__init__(**kargs)

    def compose(self) -> ComposeResult:
        with Horizontal(id="header"):
            yield HeaderClock()
            yield Tabs(
                Tab("Pods", id="pods-list"),
                # Tab("Logs", id="container-logs"),
                id="nav",
            )
        yield Footer()
        with ContentSwitcher():
            yield PodsList(self.kclient, id="pods-list")
            # yield VerticalScroll(id="container-logs")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        self.query_one(ContentSwitcher).current = event.tab.id


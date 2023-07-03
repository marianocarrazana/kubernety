from textual import work
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.reactive import reactive
from textual.containers import Vertical
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client.models import V1Pod

from .custom_widgets import ResponsiveGrid


class PodsList(ResponsiveGrid):
    pods_count = reactive(0)

    def __init__(self, kclient:CoreV1Api, **kargs):
        self.pods = []
        self.kclient = kclient
        super().__init__(**kargs)

    def on_mount(self) -> None:
        self.get_images()
        self.set_interval(2, self.count_timer)

    def count_timer(self) -> None:
        self.get_images()

    async def watch_pods_count(self, count: int) -> None:
        await self.grid.remove_children()
        for pod in self.pods:
            cw = PodWidget(pod, self.kclient) 
            self.grid.mount(cw)

    @work(exclusive=True)
    def get_images(self) -> None:
        self.pods = self.kclient.list_pod_for_all_namespaces(watch=False).items
        self.pods_count = len(self.pods)


class PodWidget(Static):
    def __init__(self, pod:V1Pod, client:CoreV1Api, **kargs):
        self.pod = pod
        self.client = client
        super().__init__(**kargs)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("[b]" + self.pod.metadata.name),
            Label(self.pod.metadata.namespace),
            Label(self.pod.status.pod_ip),
        )

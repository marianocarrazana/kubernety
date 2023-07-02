from textual import work
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.reactive import reactive
from textual.containers import Vertical

from .custom_widgets import ResponsiveGrid


class PodsList(ResponsiveGrid):
    images_count = reactive(0)

    def __init__(self, kclient, **kargs):
        self.images = []
        self.kclient = kclient
        super().__init__(**kargs)

    def on_mount(self) -> None:
        self.get_images()
        self.set_interval(2, self.count_timer)

    def count_timer(self) -> None:
        self.get_images()

    async def watch_images_count(self, count: int) -> None:
        await self.grid.remove_children()
        for c in self.images:
            cw = PodWidget(c, self.kclient)  # type: ignore
            self.grid.mount(cw)

    @work(exclusive=True)
    def get_images(self) -> None:
        self.images = self.kclient.images.list(all=False)
        self.images_count = len(self.images)


class PodWidget(Static):
    def __init__(self, image: Image, client, **kargs):
        self.image = image
        self.client = client
        self.attrs = image.attrs or {}
        self.isize = self.attrs.get("Size", 0) / 1000 / 1000
        if self.image.tags:
            self.tag = self.image.tags[0]
        elif self.image.id:
            self.tag = self.image.id.replace("sha256:", "")
        else:
            self.tag = ""
        super().__init__(**kargs)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("[b]" + self.tag),
            Label(self.image.short_id.replace("sha256:", "")),
            Label(f"Size: {self.isize:.2f}MB"),
        )
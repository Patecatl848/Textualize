from rich.console import RenderableType
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder

placeholders_count = 12


class VerticalContainer(Widget):
    CSS = """
    VerticalContainer {
        layout: vertical;
        overflow: hidden auto;
        background: darkblue;
    }

    VerticalContainer Placeholder {
        margin: 1 0;
        height: 5;
        border: solid lime;
        align: center top;
    }
    """


class Introduction(Widget):
    CSS = """
    Introduction {
        background: indigo;
        color: white;
        height: 3;
        padding: 1 0;
    }
    """

    def render(self, styles) -> RenderableType:
        return Text(
            "Press keys 0 to 9 to scroll to the Placeholder with that ID.",
            justify="center",
        )


class MyTestApp(App):
    def compose(self) -> ComposeResult:
        placeholders = [
            Placeholder(id=f"placeholder_{i}", name=f"Placeholder #{i}")
            for i in range(placeholders_count)
        ]

        yield VerticalContainer(Introduction(), *placeholders, id="root")

    def on_mount(self):
        self.bind("q", "quit")
        self.bind("t", "tree")

        scroll_to_placeholders_keys_to_bind = ",".join(
            [str(i) for i in range(placeholders_count)]
        )
        self.bind(
            scroll_to_placeholders_keys_to_bind, "scroll_to_placeholder('$event.key')"
        )

    def action_tree(self):
        self.log(self.tree)

    async def action_scroll_to_placeholder(self, key: str):
        target_placeholder = self.query(f"#placeholder_{key}").first()
        target_placeholder_container = self.query("#root").first()
        target_placeholder_container.scroll_to_widget(target_placeholder, animate=True)


app = MyTestApp()

if __name__ == "__main__":
    app.run()

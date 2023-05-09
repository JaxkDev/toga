from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete for this widget.
class MultilineTextInput(Widget):
    def create(self):
        self._action("create MultilineTextInput")

    def set_value(self, value):
        self._set_value("value", value)

    def get_value(self):
        return self._get_value("value")

    def get_placeholder(self):
        return self._get_value("placeholder")

    def set_placeholder(self, value):
        self._set_value("placeholder", value)

    def get_readonly(self):
        return self._get_value("readonly")

    def set_readonly(self, value):
        self._set_value("readonly", value)

    def scroll_to_bottom(self):
        self._action("scroll to bottom")

    def scroll_to_top(self):
        self._action("scroll to top")

    def simulate_change(self):
        self.interface.on_change(None)

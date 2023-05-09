from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import EventLog, assert_action_performed, attribute_value


@pytest.fixture
def widget():
    return toga.MultilineTextInput()


def test_widget_created(widget):
    "A multiline text input"
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create MultilineTextInput")

    assert not widget.readonly
    assert widget.placeholder == ""
    assert widget.value == ""
    assert widget._on_change._raw is None


def test_create_with_values():
    "A multiline text input can be created with initial values"
    on_change = Mock()
    widget = toga.MultilineTextInput(
        value="Some text",
        placeholder="A placeholder",
        readonly=True,
        on_change=on_change,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create MultilineTextInput")

    assert widget.readonly
    assert widget.placeholder == "A placeholder"
    assert widget.value == "Some text"
    assert widget._on_change._raw == on_change


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", ""),
        (None, ""),
        (12345, "12345"),
        ("Contains\nnewline", "Contains\nnewline"),
    ],
)
def test_value(widget, value, expected):
    """The value of the input can be set."""
    # Clear the event log
    EventLog.reset()

    widget.value = value
    assert widget.value == expected

    # test backend has the right value
    assert attribute_value(widget, "value") == expected

    # A refresh was performed
    assert_action_performed(widget, "refresh")


def test_clear(widget):
    """The value of the input can be cleared."""
    # Clear the event log
    EventLog.reset()

    # Set an initial value on the widget
    widget.value = "Hello world"
    assert widget.value == "Hello world"

    # A refresh was performed
    assert_action_performed(widget, "refresh")

    # Clear the event log
    EventLog.reset()

    # Clear the widget text.
    widget.clear()
    assert widget.value == ""

    # A refresh was performed
    assert_action_performed(widget, "refresh")


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, False),
        ("", False),
        ("true", True),
        ("false", True),  # Evaluated as a string, this value is true.
        (0, False),
        (1234, True),
    ],
)
def test_readonly(widget, value, expected):
    "The readonly status of the widget can be changed."
    # Widget is initially not readonly by default.
    assert not widget.readonly

    # Set the readonly status
    widget.readonly = value
    assert widget.readonly == expected

    # Set the widget readonly
    widget.readonly = True
    assert widget.readonly

    # Set the readonly status again
    widget.readonly = value
    assert widget.readonly == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, False),
        ("", False),
        ("true", True),
        ("false", True),  # Evaluated as a string, this value is true.
        (0, False),
        (1234, True),
    ],
)
def test_enabled(widget, value, expected):
    "The enabled status of the widget can be changed, but is a proxy for readonly"
    # Widget is initially enabled by default.
    assert widget.enabled
    assert not widget.readonly

    # Set the enabled status
    widget.enabled = value
    assert widget.enabled == expected
    assert widget.readonly != expected

    # Disable the widget
    widget.enabled = False
    assert not widget.enabled
    assert widget.readonly

    # Set the enabled status again
    widget.enabled = value
    assert widget.enabled == expected
    assert widget.readonly != expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", ""),
        (None, ""),
        (12345, "12345"),
        ("Contains\nnewline", "Contains\nnewline"),
    ],
)
def test_placeholder(widget, value, expected):
    """The value of the placeholder can be set."""
    # Clear the event log
    EventLog.reset()

    widget.placeholder = value
    assert widget.placeholder == expected

    # test backend has the right value
    assert attribute_value(widget, "placeholder") == expected

    # A refresh was performed
    assert_action_performed(widget, "refresh")


def test_scroll(widget):
    """The widget can be scrolled programatically."""
    # Clear the event log
    EventLog.reset()

    widget.scroll_to_top()

    # A refresh was performed
    assert_action_performed(widget, "scroll to top")

    # Clear the event log
    EventLog.reset()

    widget.scroll_to_bottom()

    # The widget has been scrolled
    assert_action_performed(widget, "scroll to bottom")


def test_on_change(widget):
    """The on_change handler can be invoked."""
    # No handler initially
    assert widget._on_change._raw is None

    # Define and set a new callback
    handler = Mock()

    widget.on_change = handler

    assert widget.on_change._raw == handler

    # Invoke the callback
    widget._impl.simulate_change()

    # Callback was invoked
    handler.assert_called_once_with(widget)

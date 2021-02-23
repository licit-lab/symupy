"""
    Unit tests for symupy.api.stream
"""

# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.runtime.logic.publisher import Publisher
from symupy.runtime.logic.subscriber import Subscriber

# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================


@pytest.fixture
def default_channel():
    return ("default",)


@pytest.fixture
def channels():
    return ("channel 1", "channel 2")


def test_default_constructor(default_channel):
    p = Publisher()
    assert p.channels == default_channel


def test_default_attach_observer(default_channel):
    p = Publisher()
    s = Subscriber(p)
    assert p.channels == default_channel
    assert p._channels[default_channel[0]][s] == s.update


def test_constructor_channels(channels):
    p = Publisher(channels)
    assert p.channels == channels


def test_attach_observer(channels):
    p = Publisher(channels)
    s = Subscriber(p, channels[0])
    assert p.channels == channels
    assert p._channels[channels[0]][s] == s.update


def test_attach_detach_observer(channels):
    p = Publisher(channels)
    s = Subscriber(p, channels[0])
    assert p._channels[channels[0]][s] == s.update


def test_context_publisher(channels):
    with Publisher(channels) as p:
        s1 = Subscriber(p, channels[0])
        s2 = Subscriber(p, channels[0])
        p.dispatch(channels[0])
        assert s1._call == 1
        assert s2._call == 1


def test_context_observer(channels):
    with Publisher(channels) as p:
        with Subscriber(p, channels[0]), Subscriber(p, channels[1]):
            p.dispatch(channels[0])


def test_context_dispatch(channels):
    pass

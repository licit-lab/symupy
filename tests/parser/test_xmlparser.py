"""
    Unit tests for symupy.reader.xmlparser
"""
# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import os
import platform
import pytest

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================


# ============================================================================
# TESTS AND DEFINITIONS
# ============================================================================

from symupy.parser.xmlparser import XMLParser


@pytest.fixture
def bottleneck_001():
    file_name = "bottleneck_001.xml"
    file_path = ("tests", "mocks", "bottlenecks", file_name)
    return os.path.join(os.getcwd(), *file_path)


def test_xmlparse(bottleneck_001):
    parser = XMLParser(bottleneck_001)
    root = parser.get_elem("ROOT_SYMUBRUIT")
    assert len(root.getchildrens()) == 4


def test_sourceline(bottleneck_001):
    parser = XMLParser(bottleneck_001)
    elem = parser.xpath('ROOT_SYMUBRUIT/SCENARIOS/SCENARIO')
    assert elem.sourceline == 60

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

from symupy.plugins.reader.symuflow import SymuFlowNetworkReader


@pytest.fixture
def bottleneck_001():
    file_name = "bottleneck_001.xml"
    file_path = ("tests", "mocks", "bottlenecks", file_name)
    return os.path.join(os.getcwd(), *file_path)


def test_getlinks(bottleneck_001):
    reader = SymuFlowNetworkReader(bottleneck_001)
    links = reader.get_links()
    assert len(links) == 1


def test_getnetwork(bottleneck_001):
    reader = SymuFlowNetworkReader(bottleneck_001)
    network = reader.get_network()
    assert len(network.links) == 1


def test_getlinkattributes(bottleneck_001):
    reader = SymuFlowNetworkReader(bottleneck_001)
    network = reader.get_network()
    lkinfo = network.get_links_attributes("id")
    assert lkinfo.get("Zone_001") == "Zone_001"
    lkinfo = network.get_links_attributes("downstream_node")
    assert lkinfo.get("Zone_001") == "Ext_Out"
    lkinfo = network.get_links_attributes("upstream_node")
    assert lkinfo.get("Zone_001") == "Ext_In"
    lkinfo = network.get_links_attributes("nb_lanes")
    assert lkinfo.get("Zone_001") == 1
    lkinfo = network.get_links_attributes("internal_points")
    assert lkinfo.get("Zone_001") == []

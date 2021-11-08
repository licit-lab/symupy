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

from symupy.parser.xmlparser import XMLParser, XMLTrajectory


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
    elem = parser.xpath("ROOT_SYMUBRUIT/SCENARIOS/SCENARIO")
    assert elem.sourceline == 60


@pytest.fixture
def multiple_traces():
    STREAM = b'<INST nbVeh="92" val="301.00"><CREATIONS/><SORTIES/><TRAJS><TRAJ abs="999.63" acc="0.00" dst="999.63" id="148" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="992.28" acc="0.00" dst="992.28" id="149" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="984.93" acc="0.00" dst="984.93" id="150" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="977.57" acc="0.00" dst="977.57" id="151" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="970.22" acc="0.00" dst="970.22" id="152" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="962.87" acc="0.00" dst="962.87" id="153" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="955.51" acc="0.00" dst="955.51" id="154" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="948.16" acc="0.00" dst="948.16" id="155" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="940.81" acc="0.00" dst="940.81" id="156" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="933.46" acc="0.00" dst="933.46" id="157" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="926.10" acc="0.00" dst="926.10" id="158" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="918.75" acc="0.00" dst="918.75" id="159" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="911.40" acc="0.00" dst="911.40" id="160" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="904.04" acc="0.00" dst="904.04" id="161" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="896.69" acc="0.00" dst="896.69" id="162" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="889.34" acc="0.00" dst="889.34" id="163" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="881.99" acc="0.00" dst="881.99" id="164" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="874.63" acc="0.00" dst="874.63" id="165" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="867.28" acc="0.00" dst="867.28" id="166" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="859.93" acc="0.00" dst="859.93" id="167" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="852.57" acc="0.00" dst="852.57" id="168" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="845.22" acc="0.00" dst="845.22" id="169" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="837.87" acc="0.00" dst="837.87" id="170" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="830.51" acc="0.00" dst="830.51" id="171" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="823.16" acc="0.00" dst="823.16" id="172" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="815.81" acc="0.00" dst="815.81" id="173" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="808.46" acc="0.00" dst="808.46" id="174" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="801.10" acc="0.00" dst="801.10" id="175" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="793.75" acc="0.00" dst="793.75" id="176" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="786.40" acc="0.00" dst="786.40" id="177" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="779.04" acc="0.00" dst="779.04" id="178" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="771.69" acc="0.00" dst="771.69" id="179" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="764.34" acc="0.00" dst="764.34" id="180" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="756.98" acc="0.00" dst="756.98" id="181" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="749.63" acc="0.00" dst="749.63" id="182" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="742.28" acc="0.00" dst="742.28" id="183" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="734.93" acc="0.00" dst="734.93" id="184" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="727.57" acc="0.00" dst="727.57" id="185" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="720.22" acc="0.00" dst="720.22" id="186" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="712.87" acc="0.00" dst="712.87" id="187" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="705.51" acc="0.00" dst="705.51" id="188" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="698.16" acc="0.00" dst="698.16" id="189" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="690.81" acc="0.00" dst="690.81" id="190" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="683.46" acc="0.00" dst="683.46" id="191" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="676.10" acc="0.00" dst="676.10" id="192" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="668.75" acc="0.00" dst="668.75" id="193" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="661.40" acc="0.00" dst="661.40" id="194" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="654.04" acc="0.00" dst="654.04" id="195" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="646.69" acc="0.00" dst="646.69" id="196" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="639.34" acc="0.00" dst="639.34" id="197" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="631.98" acc="0.00" dst="631.98" id="198" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="624.63" acc="0.00" dst="624.63" id="199" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="617.28" acc="0.00" dst="617.28" id="200" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="609.93" acc="0.00" dst="609.93" id="201" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="602.57" acc="0.00" dst="602.57" id="202" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="595.22" acc="0.00" dst="595.22" id="203" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="587.87" acc="0.00" dst="587.87" id="204" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="580.51" acc="0.00" dst="580.51" id="205" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="573.16" acc="0.00" dst="573.16" id="206" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="565.81" acc="-0.00" dst="565.81" id="207" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="558.45" acc="0.00" dst="558.45" id="208" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="551.10" acc="0.00" dst="551.10" id="209" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="543.75" acc="0.00" dst="543.75" id="210" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="536.40" acc="-0.00" dst="536.40" id="211" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="529.04" acc="0.00" dst="529.04" id="212" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="521.69" acc="0.00" dst="521.69" id="213" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="514.34" acc="0.00" dst="514.34" id="214" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="506.98" acc="-0.00" dst="506.98" id="215" ord="0.00" tron="L_0" type="VL" vit="1.47" voie="1" z="0.00"/><TRAJ abs="499.63" acc="0.00" dst="499.63" id="216" ord="0.00" tron="L_0" type="VL" vit="1.48" voie="1" z="0.00"/><TRAJ abs="492.27" acc="0.00" dst="492.27" id="217" ord="0.00" tron="L_0" type="VL" vit="1.48" voie="1" z="0.00"/><TRAJ abs="484.91" acc="0.00" dst="484.91" id="218" ord="0.00" tron="L_0" type="VL" vit="1.48" voie="1" z="0.00"/><TRAJ abs="477.56" acc="-0.08" dst="477.56" id="219" ord="0.00" tron="L_0" type="VL" vit="1.48" voie="1" z="0.00"/><TRAJ abs="470.20" acc="0.00" dst="470.20" id="220" ord="0.00" tron="L_0" type="VL" vit="1.56" voie="1" z="0.00"/><TRAJ abs="462.76" acc="0.00" dst="462.76" id="221" ord="0.00" tron="L_0" type="VL" vit="1.56" voie="1" z="0.00"/><TRAJ abs="455.32" acc="0.00" dst="455.32" id="222" ord="0.00" tron="L_0" type="VL" vit="1.56" voie="1" z="0.00"/><TRAJ abs="447.88" acc="-1.39" dst="447.88" id="223" ord="0.00" tron="L_0" type="VL" vit="1.56" voie="1" z="0.00"/><TRAJ abs="440.44" acc="-1.06" dst="440.44" id="224" ord="0.00" tron="L_0" type="VL" vit="2.94" voie="1" z="0.00"/><TRAJ abs="431.62" acc="-11.11" dst="431.62" id="225" ord="0.00" tron="L_0" type="VL" vit="4.00" voie="1" z="0.00"/><TRAJ abs="421.73" acc="-9.52" dst="421.73" id="226" ord="0.00" tron="L_0" type="VL" vit="15.48" voie="1" z="0.00"/><TRAJ abs="400.00" acc="0.00" dst="400.00" id="227" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="368.75" acc="0.00" dst="368.75" id="228" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="337.50" acc="0.00" dst="337.50" id="229" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="306.25" acc="0.00" dst="306.25" id="230" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="275.00" acc="0.00" dst="275.00" id="231" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="243.75" acc="0.00" dst="243.75" id="232" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="212.50" acc="0.00" dst="212.50" id="233" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="181.25" acc="0.00" dst="181.25" id="234" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="150.00" acc="0.00" dst="150.00" id="235" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="118.75" acc="0.00" dst="118.75" id="236" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="87.50" acc="0.00" dst="87.50" id="237" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="56.25" acc="0.00" dst="56.25" id="238" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="25.00" acc="0.00" dst="25.00" id="239" ord="0.00" tron="L_0" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="O" nb_veh_en_attente="0"/></ENTREES><REGULATIONS/></INST>'

    return STREAM


@pytest.fixture
def multiple_traces_tuple():
    return (
        (999.63, 0.0, 999.63, False, 148, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (992.28, 0.0, 992.28, False, 149, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (984.93, 0.0, 984.93, False, 150, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (977.57, 0.0, 977.57, False, 151, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (970.22, 0.0, 970.22, False, 152, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (962.87, 0.0, 962.87, False, 153, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (955.51, 0.0, 955.51, False, 154, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (948.16, 0.0, 948.16, False, 155, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (940.81, 0.0, 940.81, False, 156, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (933.46, 0.0, 933.46, False, 157, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (926.1, 0.0, 926.1, False, 158, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (918.75, 0.0, 918.75, False, 159, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (911.4, 0.0, 911.4, False, 160, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (904.04, 0.0, 904.04, False, 161, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (896.69, 0.0, 896.69, False, 162, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (889.34, 0.0, 889.34, False, 163, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (881.99, 0.0, 881.99, False, 164, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (874.63, 0.0, 874.63, False, 165, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (867.28, 0.0, 867.28, False, 166, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (859.93, 0.0, 859.93, False, 167, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (852.57, 0.0, 852.57, False, 168, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (845.22, 0.0, 845.22, False, 169, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (837.87, 0.0, 837.87, False, 170, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (830.51, 0.0, 830.51, False, 171, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (823.16, 0.0, 823.16, False, 172, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (815.81, 0.0, 815.81, False, 173, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (808.46, 0.0, 808.46, False, 174, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (801.1, 0.0, 801.1, False, 175, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (793.75, 0.0, 793.75, False, 176, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (786.4, 0.0, 786.4, False, 177, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (779.04, 0.0, 779.04, False, 178, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (771.69, 0.0, 771.69, False, 179, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (764.34, 0.0, 764.34, False, 180, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (756.98, 0.0, 756.98, False, 181, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (749.63, 0.0, 749.63, False, 182, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (742.28, 0.0, 742.28, False, 183, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (734.93, 0.0, 734.93, False, 184, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (727.57, 0.0, 727.57, False, 185, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (720.22, 0.0, 720.22, False, 186, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (712.87, 0.0, 712.87, False, 187, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (705.51, 0.0, 705.51, False, 188, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (698.16, 0.0, 698.16, False, 189, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (690.81, 0.0, 690.81, False, 190, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (683.46, 0.0, 683.46, False, 191, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (676.1, 0.0, 676.1, False, 192, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (668.75, 0.0, 668.75, False, 193, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (661.4, 0.0, 661.4, False, 194, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (654.04, 0.0, 654.04, False, 195, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (646.69, 0.0, 646.69, False, 196, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (639.34, 0.0, 639.34, False, 197, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (631.98, 0.0, 631.98, False, 198, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (624.63, 0.0, 624.63, False, 199, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (617.28, 0.0, 617.28, False, 200, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (609.93, 0.0, 609.93, False, 201, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (602.57, 0.0, 602.57, False, 202, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (595.22, 0.0, 595.22, False, 203, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (587.87, 0.0, 587.87, False, 204, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (580.51, 0.0, 580.51, False, 205, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (573.16, 0.0, 573.16, False, 206, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (565.81, -0.0, 565.81, False, 207, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (558.45, 0.0, 558.45, False, 208, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (551.1, 0.0, 551.1, False, 209, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (543.75, 0.0, 543.75, False, 210, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (536.4, -0.0, 536.4, False, 211, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (529.04, 0.0, 529.04, False, 212, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (521.69, 0.0, 521.69, False, 213, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (514.34, 0.0, 514.34, False, 214, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (506.98, -0.0, 506.98, False, 215, 0.0, "L_0", "VL", 1.47, 1, 0.0),
        (499.63, 0.0, 499.63, False, 216, 0.0, "L_0", "VL", 1.48, 1, 0.0),
        (492.27, 0.0, 492.27, False, 217, 0.0, "L_0", "VL", 1.48, 1, 0.0),
        (484.91, 0.0, 484.91, False, 218, 0.0, "L_0", "VL", 1.48, 1, 0.0),
        (477.56, -0.08, 477.56, False, 219, 0.0, "L_0", "VL", 1.48, 1, 0.0),
        (470.2, 0.0, 470.2, False, 220, 0.0, "L_0", "VL", 1.56, 1, 0.0),
        (462.76, 0.0, 462.76, False, 221, 0.0, "L_0", "VL", 1.56, 1, 0.0),
        (455.32, 0.0, 455.32, False, 222, 0.0, "L_0", "VL", 1.56, 1, 0.0),
        (447.88, -1.39, 447.88, False, 223, 0.0, "L_0", "VL", 1.56, 1, 0.0),
        (440.44, -1.06, 440.44, False, 224, 0.0, "L_0", "VL", 2.94, 1, 0.0),
        (431.62, -11.11, 431.62, False, 225, 0.0, "L_0", "VL", 4.0, 1, 0.0),
        (421.73, -9.52, 421.73, False, 226, 0.0, "L_0", "VL", 15.48, 1, 0.0),
        (400.0, 0.0, 400.0, False, 227, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (368.75, 0.0, 368.75, False, 228, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (337.5, 0.0, 337.5, False, 229, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (306.25, 0.0, 306.25, False, 230, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (275.0, 0.0, 275.0, False, 231, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (243.75, 0.0, 243.75, False, 232, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (212.5, 0.0, 212.5, False, 233, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (181.25, 0.0, 181.25, False, 234, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (150.0, 0.0, 150.0, False, 235, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (118.75, 0.0, 118.75, False, 236, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (87.5, 0.0, 87.5, False, 237, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (56.25, 0.0, 56.25, False, 238, 0.0, "L_0", "VL", 25.0, 1, 0.0),
        (25.0, 0.0, 25.0, False, 239, 0.0, "L_0", "VL", 25.0, 1, 0.0),
    )


@pytest.fixture
def multiple_traces_hybrid():
    STREAM = b'<INST nbVeh="1" val="3.00"><CREATIONS><CREATION entree="Ext_In" id="2" sortie="Ext_Out" type="VL"/></CREATIONS><SORTIES/><TRAJS><TRAJ abs="50.00" acc="0.00" dst="50.00" etat_pilotage="force (ecoulement respecte)" id="0" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/><TRAJ abs="19.12" acc="0.00" dst="19.12" id="1" ord="0.00" tron="Zone_001" type="VL" vit="25.00" voie="1" z="0.00"/></TRAJS><STREAMS/><LINKS/><SGTS/><FEUX/><ENTREES><ENTREE id="Ext_In" nb_veh_en_attente="1"/></ENTREES><REGULATIONS/></INST>'
    return STREAM


@pytest.fixture
def multiple_traces_hybrid_tuple():
    return (
        (50.0, 0.0, 50.0, True, 0, 0.0, "Zone_001", "VL", 25.0, 1, 0.0),
        (19.12, 0.0, 19.12, False, 1, 0.0, "Zone_001", "VL", 25.0, 1, 0.0),
    )


def test_xml_trajectory_parse_regular(multiple_traces, multiple_traces_tuple):
    z = XMLTrajectory(multiple_traces)
    ids = [x[4] for x in multiple_traces_tuple]
    assert z.traj == multiple_traces_tuple
    assert z.abs == dict(zip(ids, [x[0] for x in multiple_traces_tuple]))
    assert z.acceleration == dict(zip(ids, [x[1] for x in multiple_traces_tuple]))
    assert z.dst == dict(zip(ids, [x[2] for x in multiple_traces_tuple]))
    assert z.driven == dict(zip(ids, [x[3] for x in multiple_traces_tuple]))
    assert z.id == tuple(ids)
    assert z.ord == dict(zip(ids, [x[5] for x in multiple_traces_tuple]))
    assert z.link == dict(zip(ids, [x[6] for x in multiple_traces_tuple]))
    assert z.type == dict(zip(ids, [x[7] for x in multiple_traces_tuple]))
    assert z.vit == dict(zip(ids, [x[8] for x in multiple_traces_tuple]))
    assert z.lane == dict(zip(ids, [x[9] for x in multiple_traces_tuple]))
    assert z.z == dict(zip(ids, [x[10] for x in multiple_traces_tuple]))


def test_xml_trajectory_parse_hybrid(
    multiple_traces_hybrid, multiple_traces_hybrid_tuple
):
    z = XMLTrajectory(multiple_traces_hybrid)
    ids = [x[4] for x in multiple_traces_hybrid_tuple]
    assert z.traj == multiple_traces_hybrid_tuple
    assert z.abs == dict(zip(ids, [x[0] for x in multiple_traces_hybrid_tuple]))
    assert z.acceleration == dict(zip(ids, [x[1] for x in multiple_traces_hybrid_tuple]))
    assert z.dst == dict(zip(ids, [x[2] for x in multiple_traces_hybrid_tuple]))
    assert z.driven == dict(zip(ids, [x[3] for x in multiple_traces_hybrid_tuple]))
    assert z.id == tuple(ids)
    assert z.ord == dict(zip(ids, [x[5] for x in multiple_traces_hybrid_tuple]))
    assert z.link == dict(zip(ids, [x[6] for x in multiple_traces_hybrid_tuple]))
    assert z.type == dict(zip(ids, [x[7] for x in multiple_traces_hybrid_tuple]))
    assert z.vit == dict(zip(ids, [x[8] for x in multiple_traces_hybrid_tuple]))
    assert z.lane == dict(zip(ids, [x[9] for x in multiple_traces_hybrid_tuple]))
    assert z.z == dict(zip(ids, [x[10] for x in multiple_traces_hybrid_tuple]))

"""
XML Parser
==========
A generic parser for XML files.
"""

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import re
from functools import cache, cached_property
from typing import Pattern
from symupy.utils.constants import FIELD_FORMAT, FIELD_DATA

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class XMLElement:
    pattern_tag = re.compile("(?<=<)(\w+)(?=>|\s|\/)")
    pattern_comment = re.compile("^<!(.*)>$")
    pattern_args = re.compile('\s([a-zA-Z0-9_:]+)="(.*?)"')
    pattern_childrens = re.compile("\/>$")

    def __init__(self, line, pos, filename, linenum):
        self._filename = filename
        self._pos = pos
        self.tag = XMLElement.pattern_tag.findall(line)[0]
        self.attr = {key: val for key, val in XMLElement.pattern_args.findall(line)}
        self.sourceline = linenum

        if XMLElement.pattern_childrens.findall(line):
            self._has_childrens = False
        else:
            self._has_childrens = True

    def iterchildrens(self):
        linenum = self.sourceline
        with open(self._filename) as f:
            f.seek(self._pos)
            f.readline()

            if self._has_childrens:
                linenum += 1
                line = f.readline().strip()
                while not any(
                    bool(x)
                    for x in [
                        re.findall(self._end_tag(self.tag), line),
                        re.findall(self._startend_tag(self.tag), line),
                    ]
                ):
                    # Checking if line is a comment or blank
                    if not XMLElement.pattern_comment.findall(line) and line != "":
                        new_tag = XMLElement.pattern_tag.findall(line)[0]
                        end_tag = re.compile(f"<\/{new_tag}>")
                        if re.findall(self._startend_tag(new_tag), line):
                            pos = f.tell() - (len(line) + 2)
                            yield XMLElement(line, pos, self._filename, linenum)
                        elif re.findall(self._start_tag(new_tag), line):
                            pos = f.tell() - (len(line) + 2)
                            keep_line = line
                            keepnum = linenum
                            while True:
                                linenum += 1
                                line = f.readline().strip()
                                if end_tag.findall(line):
                                    break
                            yield XMLElement(keep_line, pos, self._filename, keepnum)
                        else:
                            break
                    linenum += 1
                    line = f.readline().strip()
            else:
                yield from ()

    def getchildrens(self):
        return list(self.iterchildrens())

    def find_children_tag(self, tag):
        for child in self.iterchildrens():
            if child.tag == tag:
                return child

    def find_children_attr(self, attr, val):
        for child in self.iterchildrens():
            if attr in child.attr.keys():
                if child.attr[attr] == val:
                    return child

    def _start_tag(self, tag):
        return f"<{tag}.*>"

    def _end_tag(self, tag):
        return f"<\/{tag}>"

    def _startend_tag(self, tag):
        return f"^<{tag}.*\/>"

    def __repr__(self):
        return f"XMLElement({self.tag}, {self.attr.__repr__()})"

    def __hash__(self):
        return hash((self._filename, self.sourceline))

    def __eq__(self, another):
        return (
            self.sourceline == another.sourceline
            and self._filename == another._filename
        )


class XMLParser(object):
    def __init__(self, filename):
        self._filename = filename

    def get_elem(self, elem):
        linenum = 1
        with open(self._filename, "r") as f:
            line = f.readline()
            while line:
                if re.findall(f"(?<=<){elem}(?=>|\s|\/)", line):
                    pos = f.tell() - len(line)
                    return XMLElement(line.strip(), pos, self._filename, linenum)
                linenum += 1
                line = f.readline()

    def xpath(self, path):
        tags = path.split("/")
        elem = self.get_elem(tags[0])
        for t in tags[1:]:
            if t[0] == "@":
                return elem.attr[t[1:]]
            elif elem is None:
                return
            else:
                elem = elem.find_children_tag(t)
        return elem

    def get_root(self):
        linenum = 1
        with open(self._filename, "r") as f:
            line = f.readline()
            # Check first elem in XML but ignore header and comment
            while not re.findall("^<[^\?|!](.*)>$", line):
                linenum += 1
                line = f.readline()
            pos = f.tell() - len(line)
            return XMLElement(line.strip(), pos, self._filename, linenum)


PATTERN = {
    "abs": re.compile(r'abs="(.*?)"'),
    "acc": re.compile(r'acc="(.*?)"'),
    "dst": re.compile(r'dst="(.*?)"'),
    "etat_pilotage": re.compile(r'dst="([\d\.]*?)"( etat_pilotage=".*?")? id="(.*?)"'),
    "id": re.compile(r'id="(\d+)"'),
    "ord": re.compile(r'ord="(.*?)"'),
    "tron": re.compile(r'tron="(.*?)"'),
    "type": re.compile(r'tron="(.*?)" type="(.*?)" vit="(.*?)"'),
    "vit": re.compile(r'vit="(.*?)"'),
    "voie": re.compile(r'voie="(.*?)"'),
    "z": re.compile(r'z="(.*?)"'),
    "traj": re.compile(
        r'abs="(.*?)" acc="(.*?)" dst="([\d\.]*?)"( etat_pilotage=".*?")? id="(.*?)" ord="(.*?)" tron="(.*?)" type="(.*?)" vit="(.*?)" voie="(.*?)" z="(.*?)"'
    ),
    "inst": re.compile(r'val="(.*?)"'),
    "nbveh": re.compile(r'nbVeh="(.*?)"'),
    "extract_traj_balise": re.compile('<TRAJS>(.*?)<\/TRAJS>')
}

CAV_TYPE = tuple(value for key, value in FIELD_FORMAT.items())


class XMLTrajectory:
    """Model object for a trajectory, it can be created from a xml and contains trajectories for a set of vehicles."""

    aliases = {
        "abscissa": "abs",
        "acceleration": "acc",
        "distance": "dst",
        "elevation": "z",
        "lane": "voie",
        "link": "tron",
        "ordinate": "ord",
        "speed": "vit",
        "vehid": "id",
        "vehtype": "type",
    }

    def __init__(self, xml: bytes):
        self._xml = xml.decode("UTF8")
        self._trajs = ''
        if len(self._xml)>0:
            pattern = PATTERN['extract_traj_balise'].findall(self._xml)
            if len(pattern)>0:
                self._trajs = pattern[0]

    def __getattr__(self, name):
        if name == "aliases":
            raise AttributeError  # http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
        name = self.aliases.get(name, name)
        return object.__getattribute__(self, name)

    @cached_property
    def abs(self) -> tuple:
        """`abs` cached values for all vehicles in network

        Returns:
            tuple: cached `abs` values
        """

        abs = tuple(
            map(
                lambda x: FIELD_FORMAT["abs"](x.replace(',', '.')),
                PATTERN.get("abs").findall(self._trajs),
            )
        )

        return dict(zip(self.id, abs))


    @cached_property
    def acc(self):
        """`acceleration` cached values for all vehicles in network

        Returns:
            tuple: cached `acc` values
        """
        acc =  tuple(map(FIELD_FORMAT["acc"], PATTERN.get("acc").findall(self._trajs)))

        return dict(zip(self.id, acc))

    @cached_property
    def dst(self):
        """`distance` cached values for all vehicles in network

        Returns:
            tuple: cached `dst` values
        """
        dst = tuple(map(FIELD_FORMAT["dst"], PATTERN.get("dst").findall(self._trajs)))

        return  dict(zip(self.id, dst))

    @cached_property
    def driven(self):
        """alias for `etat_pilotage`"""
        return self.etat_pilotage

    @cached_property
    def etat_pilotage(self):
        """`etat_pilotage` cached values for all vehicles in network

        Returns:
            tuple: cached `etat_pilotage` values
        """
        drv = PATTERN.get("etat_pilotage").findall(self._trajs)
        if drv:
            drv = tuple(map(FIELD_FORMAT["etat_pilotage"], [x[1] for x in drv]))
            return dict(zip(self.id, drv))

    @cached_property
    def id(self):
        """Vehicle `id` cached values for all vehicles in network

        Returns:
            tuple: cached `id` values
        """
        return tuple(
            map(
                FIELD_FORMAT["id"],
                [x for x in PATTERN.get("id").findall(self._trajs)],
            )
        )

    @cached_property
    def ord(self):
        """`ordinate` cached values for all vehicles in network

        Returns:
            tuple: cached `ord` values
        """
        ord = tuple(map(lambda x: FIELD_FORMAT["ord"](x.replace(',', '.')), PATTERN.get("ord").findall(self._trajs)))
        return dict(zip(self.id, ord))

    @cached_property
    def tron(self):
        """`link` cached values for all vehicles in network

        Returns:
            tuple: cached `tron` values
        """
        tron = tuple(PATTERN.get("tron").findall(self._trajs))
        return dict(zip(self.id, tron))

    @cached_property
    def type(self):
        """Vehicle `type` cached values for all vehicles in network

        Returns:
            tuple: cached `type` values
        """
        types = tuple(x[1] for x in PATTERN.get("type").findall(self._trajs))
        return dict(zip(self.id, types))

    @cached_property
    def vit(self):
        """`speed` cached values for all vehicles in network

        Returns:
            tuple: cached `vit` values
        """
        vit = [FIELD_FORMAT["vit"](vit.replace(',', '.')) for vit in PATTERN.get("vit").findall(self._trajs)]
        return dict(zip(self.id, vit))

    @cached_property
    def voie(self):
        """`lane` cached values for all vehicles in network

        Returns:
            tuple: cached `voie` values
        """
        voie = tuple(map(FIELD_FORMAT["voie"], PATTERN.get("voie").findall(self._trajs)))
        return dict(zip(self.id, voie))

    @cached_property
    def z(self):
        """`elevation` cached values for all vehicles in network

        Returns:
            tuple: cached `z` values
        """
        z = tuple(map(float, PATTERN.get("z").findall(self._trajs)))
        return dict(zip(self.id, z))

    @cached_property
    def traj(self):
        """Trajectory cached values for all vehicles in network

        Returns:
            tuple: cached `traj` values
        """
        return tuple(
            XMLTrajectory._typeconvert(x)
            for x in PATTERN.get("traj").findall(self._trajs)
        )

    @cached_property
    def inst(self):
        """`val` simulation time instant for current trajectory

        Returns:
            float: simulation time
        """
        return float(PATTERN.get("inst").findall(self._xml)[0])

    @cached_property
    def nbveh(self):
        """`nbveh` simulation time instant for current trajectory

        Returns:
            int: number of vehicles
        """
        return int(PATTERN.get("nbveh").findall(self._xml)[0])

    @cached_property
    def todict(self):
        """Converts to dictionary any of the data in the """
        # Relies on order
        return tuple(dict(zip(FIELD_DATA.values(), x)) for x in self.traj)

    @classmethod
    def _typeconvert(cls, data: tuple):
        return tuple(a(b) for a, b in zip(CAV_TYPE, data))


if __name__ == "__main__":
    import symupy
    import os

    file = (
        os.path.dirname(symupy.__file__)
        + "/../tests/mocks/bottlenecks/bottleneck_001.xml"
    )
    parser = XMLParser(file)
    root = parser.get_root()

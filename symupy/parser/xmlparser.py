"""
XML Parser
==========
A generic parser for XML files.
"""

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

import re

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class Element:
    def __init__(self, line, pos, filename):
        self._filename = filename
        self._pos = pos
        self.tag = re.findall("(?<=<)(\w+)(?=>|\s|\/)", line)[0]
        self.attr = {
            key: val for key, val in re.findall('\s(\w+)="(.*?)"', line)
        }

        if re.findall("\/>$", line):
            self._has_childrens = False
        else:
            self._has_childrens = True

    def iterchildrens(self):
        with open(self._filename) as f:
            f.seek(self._pos)
            f.readline()

            if self._has_childrens:
                line = f.readline().strip()
                while not any(
                    bool(x)
                    for x in [
                        re.findall(self._end_tag(self.tag), line),
                        re.findall(self._startend_tag(self.tag), line),
                    ]
                ):
                    # Checking if line is a comment or blank
                    if not re.findall("^<!(.*)>$", line) and line != "":
                        new_tag = re.findall("(?<=<)(\w+)(?=>|\s|\/)", line)[0]
                        if re.findall(self._startend_tag(new_tag), line):
                            pos = f.tell() - (len(line) + 2)
                            yield Element(line, pos, self._filename)
                        elif re.findall(self._start_tag(new_tag), line):
                            pos = f.tell() - (len(line) + 2)
                            keep_line = line
                            while True:
                                if re.findall(
                                    self._end_tag(new_tag), f.readline().strip()
                                ):
                                    break
                            yield Element(keep_line, pos, self._filename)
                        else:
                            break
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
        return f"Element({self.tag}, {self.attr.__repr__()})"


class XMLParser(object):
    def __init__(self, filename):
        self._filename = filename

    def get_elem(self, elem):
        with open(self._filename, "r") as f:
            line = f.readline()
            while line:
                if re.findall(f"(?<=<){elem}(?=>|\s|\/)", line):
                    pos = f.tell() - len(line)
                    return Element(line.strip(), pos, self._filename)
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


if __name__ == "__main__":
    import symupy
    import os

    file = (
        os.path.dirname(symupy.__file__)
        + "/../tests/mocks/bottlenecks/bottleneck_001.xml"
    )
    parser = XMLParser(file)
    network = parser.get_network()

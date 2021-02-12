import numpy as np
import os

from collections import OrderedDict

from symupy.components.networks import Network
from symupy.reader.xmlparser import XMLParser

from functools import cached_property

class NetworkReader(object):
    def __init__(self, file, remove_comments=True):
        assert file.split('.')[-1] == 'xml'
        self._file = file
        self._parser = XMLParser(self._file)
        self._id = self._parser.xpath('ROOT_SYMUBRUIT/RESEAUX/RESEAU/@id')

    @cached_property
    def _links(self):
        return self._parser.xpath('ROOT_SYMUBRUIT/RESEAUX/RESEAU/TRONCONS')

    @cached_property
    def _sensors(self):
        return self._parser.xpath('ROOT_SYMUBRUIT/TRAFICS/TRAFIC/PARAMETRAGE_CAPTEURS/CAPTEURS')

    @cached_property
    def _termination_zones(self):
        return self._parser.xpath('ROOT_SYMUBRUIT/TRAFICS/TRAFIC/ZONES_DE_TERMINAISON')

    @cached_property
    def _public_transport(self):
        return self._parser.xpath('ROOT_SYMUBRUIT/RESEAUX/RESEAU/PARAMETRAGE_VEHICULES_GUIDES/LIGNES_TRANSPORT_GUIDEES')

    def iter_links(self):
        return self._links.iterchildrens()

    def get_links(self):
        iterator = self.iter_links()
        return {tr.attr['id']:tr.attr for tr in iterator}

    def get_network(self):
        troncons = self.iter_links()
        net = Network(self._id)
        for tr in troncons:
            net.add_link(tr.attr['id'], tr.attr['id_eltamont'], tr.attr['id_eltaval'],
                         np.fromstring(tr.attr['extremite_amont'], sep=' '),
                         np.fromstring(tr.attr['extremite_aval'], sep=' '))
            internal_points = tr.find_children_tag('POINTS_INTERNES')
            if internal_points is not None:
                elt = internal_points.getchildrens()
                net.links[tr.attr['id']]['internal_points'] = np.array([np.fromstring(e.attr['coordonnees'], sep=' ') for e in elt if 'coordonnees' in e.attr.keys()])

        for id in self.info_sensors():
            net.add_sensor(id, list(self.iter_sensor(id)))

        for id in self.info_termination_zones():
            net.add_termination_zone(id, list(self.iter_termination_zones(id)))
        return net

    def nb_troncons(self):
        troncons = self._links
        size = len(troncons.getchildrens())
        return size

    def info_sensors(self):
        if self._sensors is not None:
            return {cpt.attr['id']: cpt.tag for cpt in self._sensors.iterchildrens()}
        else:
            return dict()

    def iter_sensor(self, id):
        if self._sensors is not None:
            cpt = self._sensors.find_children_attr('id', id)
            if 'troncon' in cpt.attr.keys():
                yield cpt.attr['troncon']
                return
            else:
                troncons = cpt.find_children_tag('TRONCONS').iterchildrens()
                for tr in troncons:
                    yield tr.attr['id']
        else:
            yield from ()

    def info_termination_zones(self):
        if self._termination_zones is not None:
            return [zn.attr['id'] for zn in self._termination_zones.iterchildrens()]
        else:
            return list()

    def iter_termination_zones(self, id):
        if self._termination_zones is not None:
            zn = self._termination_zones.find_children_attr('id', id)
            troncons = zn.find_children_tag('TRONCONS').iterchildrens()
            for tr in troncons:
                yield tr.attr['id']
        else:
            yield from ()

    def info_public_transport(self):
        if self._public_transport is not None:
            return [pt.attr['id'] for pt in self._public_transport]
        else:
            return list()

    def iter_public_transport(self, id):
        if self._public_transport is not None:
            pt = self._public_transport.find_children_attr('id', id)
            troncons = pt.find_children_tag('TRONCONS').iterchildrens()
            for tr in troncons:
                yield tr.attr['id']
        else:
            yield from ()


if __name__ == "__main__":
    import symupy
    import os
    file = os.path.dirname(symupy.__file__)+'/../tests/mocks/bottlenecks/bottleneck_001.xml'
    file = '/Users/florian/Work/visunet/data/Lyon63V/L63V.xml'
    reader = NetworkReader(file)
    network = reader.get_network()

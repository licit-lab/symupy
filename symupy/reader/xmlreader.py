from lxml import etree, objectify
import numpy as np
import os

from collections import OrderedDict

from symupy.components.networks import Network

class NetworkReader(object):
    def __init__(self, file, remove_comments=True):
        assert file.split('.')[-1] == 'xml'
        self._file = file
        parser = etree.XMLParser(remove_comments=remove_comments)
        self._tree = objectify.parse(self._file, parser=parser)
        self._capteurs = self._tree.xpath("//ROOT_SYMUBRUIT/TRAFICS/TRAFIC/PARAMETRAGE_CAPTEURS/CAPTEURS/*")
        self._termination_zones = self._tree.xpath("//ROOT_SYMUBRUIT/TRAFICS/TRAFIC/ZONES_DE_TERMINAISON/*")
        self._public_transport = self._tree.xpath('//ROOT_SYMUBRUIT/RESEAUX/RESEAU/PARAMETRAGE_VEHICULES_GUIDES/LIGNES_TRANSPORT_GUIDEES/*')
        self._id = self._tree.xpath('//ROOT_SYMUBRUIT/RESEAUX/RESEAU/@id')[0]
        self.file_size = os.path.getsize(file)

    def iter_links(self):
        elems = self._tree.xpath('//ROOT_SYMUBRUIT/RESEAUX/RESEAU/TRONCONS')[0].iterchildren()
        for i in elems:
            yield i.attrib

    def get_links(self):
        iterator = self.iter_links()
        return {tr.pop('id'):tr for tr in iterator}

    def get_network(self):
        troncons = self._tree.xpath('//ROOT_SYMUBRUIT/RESEAUX/RESEAU/TRONCONS')[0].iterchildren()
        net = Network(self._id)
        for tr in troncons:
            net.add_link(tr.attrib['id'], tr.attrib['id_eltamont'], tr.attrib['id_eltaval'])
            net.nodes[tr.attrib['id_eltamont']]['pos'] = np.fromstring(tr.attrib['extremite_amont'], sep=' ')
            net.nodes[tr.attrib['id_eltaval']]['pos'] = np.fromstring(tr.attrib['extremite_aval'], sep=' ')
            if tr.getchildren():
                elt = tr.getchildren()[0].getchildren()
                net.links[tr.attrib['id']]['internal_points'] = np.array([np.fromstring(e.attrib['coordonnees'], sep=' ') for e in elt if 'coordonnees' in e.keys()])

        for id in self.info_sensors():
            net.add_sensor(id, list(self.iter_sensor(id)))

        for id in self.info_termination_zones():
            net.add_termination_zone(id, list(self.iter_termination_zones(id)))
        return net

    def nb_troncons(self):
        troncons = self._tree.xpath('//ROOT_SYMUBRUIT/RESEAUX/RESEAU/TRONCONS/*')
        size = len(troncons)
        return size

    def info_sensors(self):
        return {cpt.attrib['id']: cpt.tag for cpt in self._capteurs}

    def iter_sensor(self, id):
        for cpt in self._capteurs:
            if cpt.attrib['id'] == id:
                troncons = cpt.xpath("./TRONCONS/*")
                for tr in troncons:
                    yield tr.attrib['id']

    def info_termination_zones(self):
        return [zn.attrib['id'] for zn in self._termination_zones]

    def iter_termination_zones(self, id):
        for zn in self._termination_zones:
            if zn.attrib['id'] == id:
                troncons = zn.xpath("./TRONCONS/*")
                for tr in troncons:
                    yield tr.attrib['id']

    def info_public_transport(self):
        return [pt.attrib['id'] for pt in self._public_transport]

    def iter_public_transport(self, id):
        for pt in self._public_transport:
            if pt.attrib['id'] == id:
                troncons = pt.xpath("./TRONCONS/*")
                for tr in troncons:
                    yield tr.attrib['id']

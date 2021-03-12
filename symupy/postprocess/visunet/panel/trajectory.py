import linecache

import matplotlib.pyplot as plt
import numpy as np
from lxml import etree
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QFileDialog, QFormLayout,
                             QGroupBox, QLabel, QLineEdit, QListWidget,
                             QMessageBox, QPushButton, QRadioButton,
                             QVBoxLayout, QWidget, QSlider, QHBoxLayout,
                             QDesktopWidget, QComboBox)
from PyQt5.Qt import QRect

from symupy.postprocess.visunet.qtutils import waitcursor, Slider, LabelComboBox
from symupy.parser.csvparser import (get_iteration_PPaths, get_iteration_distribution,
                               get_iteration_final_PPaths)
from symupy.parser.xmlparser import XMLParser
import re


class TrajectoryWidget(QGroupBox):
    def __init__(self, data, name='Trajectories', parent=None):
        super().__init__(name, parent)

        self.data = data

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.button_load_traj = QPushButton('Load Trajectory')
        self.button_load_traj.clicked.connect(self.load_traj)
        self.layout.addWidget(self.button_load_traj)

        self.label_file_traj = QLabel('File:')
        self.label_file_traj.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.layout.addWidget(self.label_file_traj)

        self.veh_list = QListWidget()
        self.veh_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.layout.addWidget(self.veh_list)

        self.info = QPushButton('Info')
        self.layout.addWidget(self.info)
        self.info.clicked.connect(self.info_popup)

        self.render_traj = QPushButton('Render')
        self.layout.addWidget(self.render_traj)
        self.render_traj.clicked.connect(self.plot_traj)

        self.traj_profil = None
        self.vehs = dict()
        self.loqder = None

    def show_range_traj(self):
        if not self.load_all.isChecked():
            self.load_range.setVisible(True)
        else:
            self.load_range.setVisible(False)

    def update_label_traj(self):
        file = self.data.file_traj.split('/')[-1]
        self.label_file_traj.setText('File: '+file)

    def load_traj(self):
        self.loader = Loader(self.vehs, self.veh_list, self.data, self.label_file_traj, parent=None)
        geom = QRect(0, 0, 200, 400)
        centerPoint = QDesktopWidget().availableGeometry().center()
        geom.moveCenter(centerPoint)
        self.loader.setGeometry(geom)

        self.loader.show()

    def plot_traj(self):
        try:
            for i in self.data.traj_plot:
                i.remove()
                del i
            self.data.traj_plot=list()
            selection = [item for item in self.veh_list.selectedItems()]
            vehs = {item.text(): self.vehs[item.text()][0] for item in self.veh_list.selectedItems()}
            for id, tj in vehs.items():
                tj = filter(lambda a: a[0] == 'T', tj)
                arr = np.row_stack([self.data.troncons_coords[tr] for tr in tj])
                self.data.traj_plot.append(self.data.figure.gca().plot(arr[:,0], arr[:,1], '-', label=id).pop(0))
                self.data.traj_plot.append(self.data.figure.gca().plot(arr[0,0], arr[0,1], 'k+').pop(0))
                self.data.traj_plot.append(self.data.figure.gca().annotate("O",(arr[0,0], arr[0,1])))
                self.data.traj_plot.append(self.data.figure.gca().plot(arr[-1,0], arr[-1,1], 'k+').pop(0))
                self.data.traj_plot.append(self.data.figure.gca().annotate("D",(arr[-1,0], arr[-1,1])))
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            if self.data.legend_network is not None and self.data.public_transport:
                self.data.figure.gca().add_artist(self.data.legend_network)
            plt.axis('tight')
            self.data.figure.gca().set_aspect('equal')
            self.data.canvas.draw()
        except (ValueError, KeyError) as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(e))
            msg.setInformativeText('VEHS')
            msg.setInformativeText(f'{id}: {[it for it in tj]}')
            msg.setWindowTitle("Error")
            msg.exec_()


    def info_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")

        items = self.veh_list.selectedItems()
        last_item = self.vehs[items[-1].text()]
        nb = last_item[1]
        troncons = last_item[0]
        troncons = filter(lambda a: a[0] == 'T', troncons)

        line = linecache.getline(self.data.file_traj, nb+1)
        cols = line.split(';')

        info = ''

        if 'default_PPaths' in self.data.file_traj:
            info += 'Departure Time: '+ cols[4] + '\n' +\
                    'Arrival Time: '+ cols[5] + '\n'

        elif 'final_PPaths' in self.data.file_traj:
            info += 'Departure Time: '+ cols[4] + '\n' +\
                    'Arrival Time: '+ cols[5] + '\n'

        elif 'distribution' in self.data.file_traj:
            info += 'Travel Time: '+ cols[7] + '\n'

        elif 'xml' in self.data.file_traj:
            line = linecache.getline(self.data.file_traj, nb-1)
            dist = re.search(r'dstParcourue="(.*)" entree=', line).group(1)
            info += 'Distance : ' + dist + '\n'
            print(nb)

        try:
            info += 'Troncons : ' + str(last_item[0])
        except:
            pass

        if items:
            msg.setText(items[-1].text())
            msg.setInformativeText(info)
            msg.exec_()


class Loader(QWidget):
    def __init__(self, traj, list_widget, data, label_file_par, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Loader')
        self.list_widget = list_widget
        self.label_file_par = label_file_par
        self.data = data
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.file_button = QPushButton('File')
        self.file_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.file_button)

        self.label=QLabel('File:')
        self.layout.addWidget(self.label)

        self.period = LabelComboBox(name='Period')
        self.period.setVisible(False)
        self.layout.addWidget(self.period)

        self.choice = QComboBox()
        self.choice.setVisible(False)
        self.choice.addItem("iteration")
        self.choice.addItem("trajectory")

        self.slider = Slider()
        self.slider.setVisible(False)
        self.slider_2 = Slider()
        self.slider_2.setVisible(False)
        self.layout.addWidget(self.choice)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.slider_2)

        self.load_button = None

        self.traj_profil = None

        self.traj = traj

    def load_traj_csv(self):
        self.list_widget.clear()
        self.traj.clear()

        if self.traj_profil == "default_PPaths":
            it = self.slider.value()
            if str(self.choice.currentText()) == 'iteration':
                period = int(self.period.value())
                range_vehs = self.iteration[period][it]
                with open(self.data.file_traj) as file:
                    for count, line in enumerate(file):
                        if count>= range_vehs[0] and count<=range_vehs[1]:
                            self.traj[f"VEH{line.split(';')[3]}"] = [line.split(';')[7].split("\\")[1:-1][::2], count]
            else:
                with open(self.data.file_traj) as file:
                    for count, line in enumerate(file):
                        if re.findall(f"[0-9];[0-9];[0-9];{it};", line):
                            self.traj[f"IT{line.split(';')[1]}"] = [line.split(';')[7].split("\\")[1:-1][::2], count]

        if self.traj_profil == "distribution":
            outer = self.slider.value()
            inner = self.slider_2.value()
            period = self.period.value()
            if str(self.choice.currentText()) == 'iteration':
                range_vehs = self.iteration[int(period)][outer][inner]
                id_veh = 0
                with open(self.data.file_traj) as file:
                    for count, line in enumerate(file):
                        if count>= range_vehs[0] and count<=range_vehs[1]:
                            self.traj[f"VEH{id_veh}"] = [line.split(';')[8].split("\\")[2:-2][::2], count]
                            id_veh += 1
            else:
                iterat = list()
                [[iterat.append(lt) for lt in d.values()] for d in self.iteration[int(period)].values()]

                count_iter = 0
                nb_iter = len(iterat)
                print(iterat)

                with open(self.data.file_traj) as file:
                    for count, line in enumerate(file):
                        if iterat[count_iter][0] <= count <= iterat[count_iter][1]:
                            col = line.split(';')
                            self.traj[f"IT_OUT{col[1]}_IN{col[2]}"] = [col[8].split("\\")[2:-2][::2], count]
                            if count_iter < nb_iter-1:
                                count_iter += 1
                            else:
                                break

        elif self.traj_profil == "final_PPaths":
            period = self.period.value()
            range_vehs = self.iteration[int(period)]
            with open(self.data.file_traj) as file:
                for count, line in enumerate(file):
                    if count>= range_vehs[0] and count<=range_vehs[1]:
                        self.traj[f"VEH{line.split(';')[3]}"] = [line.split(';')[7].split("\\")[1:-1][::2], count]

        keys = list(self.traj.keys())
        keys = sorted(keys, key=lambda x: int(x[3:]))
        [self.list_widget.addItem(key) for key in keys]
        self.close()

    def load_traj_xml(self):
        self.traj.clear()
        self.list_widget.clear()
        vehs = extract_vehs_outfile(self.data.file_traj)
        vehs = XMLParser(self.data.file_traj).xpath("OUT/SIMULATION/VEHS").iterchildrens()
        #
        [self.traj.__setitem__(f"VEH{item.attr['id']}", [item.attr['itineraire'].split(' '), 0]) for item in vehs]
        [self.list_widget.addItem(i) for i in self.traj]
        self.close()

    def load_file(self):
        options = QFileDialog.Options(QFileDialog.DontUseNativeDialog)
        self.data.file_traj, _ = QFileDialog.getOpenFileName(self,"Load Trajectories", "","Trajectories file (*.xml *.csv)", options=options)
        self.label.setText(f"File: {self.data.file_traj.split('/')[-1]}")
        self.label_file_par.setText(f"File: {self.data.file_traj.split('/')[-1]}")

        for profil in ['default_PPaths','final_PPaths', 'distribution', 'xml']:
            if profil in self.data.file_traj:
                self.traj_profil = profil
                break
        print('profil:', self.traj_profil)

        self.update_gui_profil()

    def add_load(self):
        if self.load_button is None:
            self.load_button = QPushButton('Load')
            self.layout.addWidget(self.load_button)

            ext = self.data.file_traj.split('.')[-1]
            if ext == 'csv':
                self.load_button.clicked.connect(self.load_traj_csv)
            elif ext == 'xml':
                self.load_button.clicked.connect(self.load_traj_xml)

    def update_gui_profil(self):
        if self.traj_profil == 'default_PPaths':
            self.iteration = get_iteration_PPaths(self.data.file_traj)
            self.update_period_widget()
            self.period.setVisible(True)
            self.choice.setVisible(True)
            self.choice.currentIndexChanged.connect(self.change_iter_traj_ppaths)
            self.period.currentIndexChanged.connect(self.connect_period_slider)
            self.connect_period_slider()
            self.change_iter_traj_ppaths()
            self.slider.setName('')
            self.slider.setVisible(True)
            self.add_load()
        elif self.traj_profil == 'distribution':
            self.iteration = get_iteration_distribution(self.data.file_traj)
            self.update_period_widget()
            self.choice.setVisible(True)
            self.choice.currentIndexChanged.connect(self.change_iter_traj_distrib)
            self.period.setVisible(True)
            self.period.currentIndexChanged.connect(self.connect_period_slider)
            self.connect_period_slider()
            self.change_iter_traj_distrib()
            self.slider.setVisible(True)
            self.add_load()
        elif self.traj_profil == 'final_PPaths':
            self.iteration = get_iteration_final_PPaths(self.data.file_traj)
            self.update_period_widget()
            self.period.setVisible(True)
            self.add_load()
        elif self.traj_profil == 'xml':
            self.load_traj_xml()
        else:
            self.period.setVisible(False)
            self.slider.setName('')
            self.choice.setVisible(False)
            self.slider.setVisible(False)

    def change_iter_traj_ppaths(self):
        period = self.period.value()
        print(period, self.iteration)
        if str(self.choice.currentText()) == 'trajectory':
            it = self.slider.value()
            range_vehs = self.iteration[int(period)][it]
            self.slider.setName('')
            self.slider.setRange(1, range_vehs[1]-range_vehs[0]+1)
        else:
            self.slider.setRange(0, len(self.iteration[int(period)])-1)

    def change_iter_traj_distrib(self):
        if str(self.choice.currentText()) == 'trajectory':
            self.slider_2.setVisible(False)
            # TODO: Find clever way etxracting leaf of nested dict
            period = self.period.value()
            outer = self.slider.value()
            inner = self.slider_2.value()
            range_vehs = self.iteration[int(period)][outer][inner]

            self.slider.setName('')
            self.slider.setRange(1, range_vehs[1]-range_vehs[0]+1)
        else:
            self.slider.setName('outer')
            self.slider.valueChanged.connect(self.connect_slider_distrib)
            self.connect_slider_distrib()
            self.slider_2.setName('inner')
            self.slider_2.setVisible(True)
            self.slider.setRange(0, len(self.iteration)-1)

    def update_period_widget(self):
        self.period.setItems(self.iteration.keys())

    def connect_slider_distrib(self):
        it = self.slider.value()
        count=len(self.iteration.keys())-1
        self.slider_2.setRange(0, count)

    def connect_period_slider(self):
        period = self.period.value()
        print('connect', period)
        self.slider.setRange(0, len(self.iteration[int(period)])-1)

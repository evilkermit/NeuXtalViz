import os
import sys
import traceback

os.environ['QT_API'] = 'pyqt5'

from qtpy.QtWidgets import (QApplication,
                            QMainWindow,
                            QWidget,
                            QAction,
                            QStackedWidget,
                            QVBoxLayout,
                            QMessageBox)

from qtpy.QtGui import QIcon

from NeuXtalViz._version import __version__

import pyvista
pyvista.set_plot_theme('document')

import qdarktheme
qdarktheme.enable_hi_dpi()

from mvvm_lib.pyqt_binding import PyQtBinding

#import qdarkstyle
#from qdarkstyle.light.palette import LightPalette

from NeuXtalViz.qt.crystal_structure_tools import CrystalStructureView
from NeuXtalViz.models.crystal_structure_tools import CrystalStructureModel
from NeuXtalViz.presenters.crystal_structure_tools import CrystalStructure

from NeuXtalViz.qt.ub_tools import UBView
from NeuXtalViz.models.ub_tools import UBModel
from NeuXtalViz.presenters.ub_tools import UB

from NeuXtalViz.qt.sample_tools import SampleView
from NeuXtalViz.models.sample_tools import SampleModel
from NeuXtalViz.presenters.sample_tools import Sample

from NeuXtalViz.qt.modulation_tools import ModulationView
from NeuXtalViz.models.modulation_tools import ModulationModel
from NeuXtalViz.presenters.modulation_tools import Modulation

from NeuXtalViz.view_models.volume_slicer import VolumeSlicerViewModel
from NeuXtalViz.qt.volume_slicer import VolumeSlicerView

from NeuXtalViz.qt.experiment_planner import ExperimentView
from NeuXtalViz.models.experiment_planner import ExperimentModel
from NeuXtalViz.presenters.experiment_planner import Experiment

class NeuXtalViz(QMainWindow):

    __instance = None

    def __new__(cls):
        if NeuXtalViz.__instance is None:
            NeuXtalViz.__instance = QMainWindow.__new__(cls)
        return NeuXtalViz.__instance

    def __init__(self, parent=None):
        super().__init__(parent)

        binding = PyQtBinding()

        icon = os.path.join(os.path.dirname(__file__), 'icons/NeuXtalViz.png')
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('NeuXtalViz {}'.format(__version__))
        # self.resize(1200, 900)

        main_window = QWidget(self)
        self.setCentralWidget(main_window)

        layout = QVBoxLayout(main_window)

        app_stack = QStackedWidget()

        app_menu = self.menuBar().addMenu('Applications')

        cs_action = QAction('Crystal Structure', self)
        cs_action.triggered.connect(lambda: app_stack.setCurrentIndex(0))
        app_menu.addAction(cs_action)

        s_action = QAction('Sample', self)
        s_action.triggered.connect(lambda: app_stack.setCurrentIndex(1))
        app_menu.addAction(s_action)

        m_action = QAction('Modulation', self)
        m_action.triggered.connect(lambda: app_stack.setCurrentIndex(2))
        app_menu.addAction(m_action)

        vs_action = QAction('Volume Slicer', self)
        vs_action.triggered.connect(lambda: app_stack.setCurrentIndex(3))
        app_menu.addAction(vs_action)

        cs_view = CrystalStructureView(self)
        cs_model = CrystalStructureModel()
        self.cs = CrystalStructure(cs_view, cs_model)
        app_stack.addWidget(cs_view)

        s_view = SampleView(self)
        s_model = SampleModel()
        self.s = Sample(s_view, s_model)
        app_stack.addWidget(s_view)

        m_view = ModulationView(self)
        m_model = ModulationModel()
        self.m = Modulation(m_view, m_model)
        app_stack.addWidget(m_view)

        vs_view = VolumeSlicerView(view_model=VolumeSlicerViewModel(binding), parent=self)
        app_stack.addWidget(vs_view)

        layout.addWidget(app_stack)

        ub_action = QAction('UB', self)
        ub_action.triggered.connect(lambda: app_stack.setCurrentIndex(4))
        app_menu.addAction(ub_action)

        ub_view = UBView(self)
        ub_model = UBModel()
        self.ub = UB(ub_view, ub_model)
        app_stack.addWidget(ub_view)

        ep_action = QAction('Planner', self)
        ep_action.triggered.connect(lambda: app_stack.setCurrentIndex(5))
        app_menu.addAction(ep_action)

        ep_view = ExperimentView(self)
        ep_model = ExperimentModel()
        self.ep = Experiment(ep_view, ep_model)
        app_stack.addWidget(ep_view)

        layout.addWidget(app_stack)

        # self.showMaximized()

def handle_exception(exc_type, exc_value, exc_traceback):
    error_message = ''.join(traceback.format_exception(exc_type,
                                                       exc_value,
                                                       exc_traceback))

    msg_box = QMessageBox()
    msg_box.setWindowTitle('Application Error')
    msg_box.setText('An unexpected error occurred. Please see details below:')
    msg_box.setDetailedText(error_message)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.exec_()

def gui():
    sys.excepthook = handle_exception
    app = QApplication(sys.argv)
    qdarktheme.setup_theme('light')
    # app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))
    window = NeuXtalViz()
    window.show()
    sys.exit(app.exec_())
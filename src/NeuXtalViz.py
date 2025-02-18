import os
import sys
import traceback
import subprocess

os.environ["QT_API"] = "pyqt5"

from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QAction,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QFileDialog,
)

from qtpy.QtGui import QIcon

from NeuXtalViz._version import __version__

import pyvista

pyvista.set_plot_theme("document")

import qdarktheme

qdarktheme.enable_hi_dpi()

# import qdarkstyle
# from qdarkstyle.light.palette import LightPalette

from NeuXtalViz.views.base_view import NeuXtalVizWidget
from NeuXtalViz.models.base_model import NeuXtalVizModel
from NeuXtalViz.presenters.base_presenter import NeuXtalVizPresenter

from NeuXtalViz.views.crystal_structure_tools import CrystalStructureView
from NeuXtalViz.models.crystal_structure_tools import CrystalStructureModel
from NeuXtalViz.presenters.crystal_structure_tools import CrystalStructure

from NeuXtalViz.views.ub_tools import UBView
from NeuXtalViz.models.ub_tools import UBModel
from NeuXtalViz.presenters.ub_tools import UB

from NeuXtalViz.views.sample_tools import SampleView
from NeuXtalViz.models.sample_tools import SampleModel
from NeuXtalViz.presenters.sample_tools import Sample

from NeuXtalViz.views.modulation_tools import ModulationView
from NeuXtalViz.models.modulation_tools import ModulationModel
from NeuXtalViz.presenters.modulation_tools import Modulation

from NeuXtalViz.views.volume_slicer import VolumeSlicerView
from NeuXtalViz.models.volume_slicer import VolumeSlicerModel
from NeuXtalViz.presenters.volume_slicer import VolumeSlicer

from NeuXtalViz.views.experiment_planner import ExperimentView
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

        self._topaz_path = "/SNS/TOPAZ"

        icon = os.path.join(os.path.dirname(__file__), "icons/NeuXtalViz.png")
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle("NeuXtalViz {}".format(__version__))
        # self.resize(1200, 900)

        main_window = QWidget(self)
        self.setCentralWidget(main_window)

        layout = QHBoxLayout(main_window)

        main_view = NeuXtalVizWidget(self)
        main_model = NeuXtalVizModel()
        main_presenter = NeuXtalVizPresenter(main_view, main_model)

        app_stack = QStackedWidget()
        app_stack.setLayout(QVBoxLayout())
        app_menu = self.menuBar().addMenu("Applications")

        cs_action = QAction("Crystal Structure", self)
        cs_action.triggered.connect(lambda: app_stack.setCurrentIndex(0))
        app_menu.addAction(cs_action)

        cs_view = CrystalStructureView(main_view)
        cs_model = CrystalStructureModel(main_model)
        self.cs = CrystalStructure(main_presenter, cs_view, cs_model)
        app_stack.addWidget(cs_view)

        s_action = QAction("Sample", self)
        s_action.triggered.connect(lambda: app_stack.setCurrentIndex(1))
        app_menu.addAction(s_action)

        s_view = SampleView(main_view)
        s_model = SampleModel(main_model)
        self.s = Sample(main_presenter, s_view, s_model)
        app_stack.addWidget(s_view)

        m_action = QAction("Modulation", self)
        m_action.triggered.connect(lambda: app_stack.setCurrentIndex(2))
        app_menu.addAction(m_action)

        m_view = ModulationView(main_view)
        m_model = ModulationModel(main_model)
        self.m = Modulation(main_presenter, m_view, m_model)
        app_stack.addWidget(m_view)

        vs_action = QAction("Volume Slicer", self)
        vs_action.triggered.connect(lambda: app_stack.setCurrentIndex(3))
        app_menu.addAction(vs_action)

        vs_view = VolumeSlicerView(main_view)
        vs_model = VolumeSlicerModel(main_model)
        self.vs = VolumeSlicer(main_presenter, vs_view, vs_model)
        app_stack.addWidget(vs_view)

        ub_action = QAction("UB", self)
        ub_action.triggered.connect(lambda: app_stack.setCurrentIndex(4))
        app_menu.addAction(ub_action)

        ub_view = UBView(main_view)
        ub_model = UBModel(main_model)
        self.ub = UB(main_presenter, ub_view, ub_model)
        app_stack.addWidget(ub_view)

        ep_action = QAction("Planner", self)
        ep_action.triggered.connect(lambda: app_stack.setCurrentIndex(5))
        app_menu.addAction(ep_action)

        ep_view = ExperimentView(main_view)
        ep_model = ExperimentModel(main_model)
        self.ep = Experiment(main_presenter, ep_view, ep_model)
        app_stack.addWidget(ep_view)

        layout.addLayout(main_view.layout, stretch=1)
        layout.addWidget(app_stack, stretch=1)

        app_menu = self.menuBar().addMenu("External")

        topaz_action = QAction("TOPAZ", self)
        topaz_action.triggered.connect(self.topaz_reduction_GUI)
        app_menu.addAction(topaz_action)

        # self.showMaximized()

    def topaz_reduction_GUI(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", self._topaz_path
        )

        if directory:
            self._topaz_path = directory
            main_py_path = os.path.join(directory, "main.py")
            if os.path.isfile(main_py_path):
                try:
                    subprocess.Popen(["mantidpython", main_py_path])
                except subprocess.CalledProcessError as e:
                    QMessageBox.critical(
                        self, "Error", f"Failed to execute main.py:\n{e}"
                    )
            else:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "The selected directory does not contain main.py.",
                )


def handle_exception(exc_type, exc_value, exc_traceback):
    error_message = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )

    msg_box = QMessageBox()
    msg_box.setWindowTitle("Application Error")
    msg_box.setText("An unexpected error occurred. Please see details below:")
    msg_box.setDetailedText(error_message)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.exec_()


def gui():
    sys.excepthook = handle_exception
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    # app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))
    window = NeuXtalViz()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    gui()

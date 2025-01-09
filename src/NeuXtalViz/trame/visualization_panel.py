"""Card for rendering and manipulating 3D visualizations."""

from typing import Any

import pyvista as pv
from pyvista.trame.ui import get_viewer
from trame.widgets import vuetify3 as vuetify

from NeuXtalViz.trame.viz_controls import VizControls


class VisualizationPanel:
    """Card for rendering and manipulating 3D visualizations."""

    def __init__(self, vm) -> None:
        self.vm = vm

        self.vm.clear_scene_bind.connect(self.clear_scene)
        self.vm.reset_view_bind.connect(self.reset_view)
        self.vm.reset_scene_bind.connect(self.reset_scene)

        self.camera_position = None
        self.plotter = self.create_plotter()
        self.create_ui()

    def clear_scene(self, _: Any = None) -> None:
        self.plotter.clear_plane_widgets()
        self.plotter.clear_actors()

        if self.camera_position is not None:
            self.save_camera()

    def create_plotter(self) -> pv.Plotter:
        plotter = pv.Plotter(off_screen=True)
        plotter.background_color = "#f0f0f0"

        return plotter

    def create_ui(self) -> None:
        with vuetify.VContainer(classes="pa-0 mr-2", fluid=True):
            VizControls(self.vm, self.plotter)

            with vuetify.VSheet(style="height: 70vh;"):
                view = get_viewer(self.plotter)
                view.ui(add_menu=False, mode="server")

    def reset_scene(self, _: Any = None):
        if self.camera_position is not None:
            self.plotter.camera_position = self.camera_position
        else:
            self.reset_view()

    def reset_view(self, negative=False):
        """
        Reset the view.
        """

        self.plotter.reset_camera()
        self.plotter.view_isometric(negative)
        self.camera_position = self.plotter.camera_position

    def save_camera(self) -> None:
        self.camera_position = self.plotter.camera_position

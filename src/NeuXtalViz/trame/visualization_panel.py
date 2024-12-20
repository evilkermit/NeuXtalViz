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
        # TODO
        # self.vm.clear_scene_bind.connect(self.clear_scene)
        # self.vm.render_bind.connect(self.render)
        # self.vm.reset_camera_bind.connect(self.reset_camera)

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

    def render(self, _: Any = None) -> None:
        self.render_axes()
        self.plotter.render()

    def render_axes(self) -> None:
        transform = self.vm.get_transform()
        reciprocal_lattice = self.vm.get_reciprocal_lattice()

        if transform is None:
            return

        user_matrix = pv._vtk.vtkMatrix4x4()
        for i in range(3):
            for j in range(3):
                user_matrix.SetElement(i, j, transform[i, j])

        if reciprocal_lattice:
            actor = self.plotter.add_axes(xlabel="a*", ylabel="b*", zlabel="c*")  # type: ignore
        else:
            actor = self.plotter.add_axes(xlabel="a", ylabel="b", zlabel="c")  # type: ignore

        actor.SetUserMatrix(user_matrix)

    def reset_camera(self, force: bool) -> None:
        if force or self.camera_position is None:
            self.plotter.reset_camera()  # type: ignore
            self.plotter.view_isometric()  # type: ignore
            self.save_camera()
        else:
            self.plotter.camera_position = self.camera_position

    def save_camera(self) -> None:
        self.camera_position = self.plotter.camera_position

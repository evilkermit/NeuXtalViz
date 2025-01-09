"""Controls above the visualization pane."""

from typing import Optional

import numpy as np
import pyvista as pv
from nova.trame.view.components import InputField
from nova.trame.view.layouts import GridLayout, HBoxLayout
from trame.widgets import vuetify3 as vuetify


class VizControls:
    """Controls above the visualization pane."""

    def __init__(self, vm, plotter: pv.Plotter) -> None:
        self.vm = vm

        self.plotter = plotter

        self.create_ui()

    def create_ui(self) -> None:
        with GridLayout(classes="mb-1", columns=8):
            vuetify.VBtn("Save Screenshot", column_span=2, disabled=True, click=self.save_screenshot)
            vuetify.VBtn("+Qx", click=self.view_yz)
            vuetify.VBtn("+Qy", click=self.view_zx)
            vuetify.VBtn("+Qz", click=self.view_xy)
            vuetify.VBtn("a*", click=self.view_bc_star)
            vuetify.VBtn("b*", click=self.view_ca_star)
            vuetify.VBtn("c*", click=self.view_ab_star)

            vuetify.VBtn("Reset View", column_span=2, click=self.vm.reset_view)
            vuetify.VBtn("-Qx", click=self.view_zy)
            vuetify.VBtn("-Qy", click=self.view_xz)
            vuetify.VBtn("-Qz", click=self.view_yx)
            vuetify.VBtn("a", click=self.view_bc)
            vuetify.VBtn("b", click=self.view_ca)
            vuetify.VBtn("c", click=self.view_ab)

        with HBoxLayout(classes="mb-1", valign="center"):
            InputField(
                v_model="axis_type",
                label="Axis Type",
                items=("['[hkl]', '[uvw]']"),
                type="select",
                # update_modelValue=(self.vm.set_axis_type, "[$event]"),
            )
            InputField(
                v_model="axis_0",
                classes="mx-1",
                variant="outlined",
                # update_modelValue=(self.vm.set_axis, "[0, $event]"),
            )
            InputField(
                v_model="axis_1",
                classes="mx-1",
                variant="outlined",
                # update_modelValue=(self.vm.set_axis, "[1, $event]"),
            )
            InputField(
                v_model="axis_2",
                classes="mx-1",
                variant="outlined",
                # update_modelValue=(self.vm.set_axis, "[2, $event]"),
            )
            vuetify.VBtn("View Axis", click=self.view_manual)
            InputField(
                v_model="reciprocal_lattice",
                label="Reciprocal Lattice",
                type="checkbox",
                # update_modelValue=self.toggle_reciprocal_lattice,
            )
            InputField(
                v_model="parallel_projection",
                label="Parallel Projection",
                type="checkbox",
                # update_modelValue=self.toggle_parallel_projection,
            )

    def save_screenshot(self) -> None:
        pass  # TODO

    def toggle_parallel_projection(self) -> None:
        value = self.vm.toggle_parallel_projection()

        if value:
            self.plotter.enable_parallel_projection()  # type: ignore
        else:
            self.plotter.disable_parallel_projection()  # type: ignore

        self.vm.render()

    def toggle_reciprocal_lattice(self) -> None:
        self.vm.toggle_reciprocal_lattice()
        self.vm.render()

    def view_ab(self) -> None:
        view, up = self.vm.get_ab_axes()
        self.view_vector(view, up)

    def view_ab_star(self) -> None:
        view, up = self.vm.get_ab_star_axes()
        self.view_vector(view, up)

    def view_bc(self) -> None:
        view, up = self.vm.get_bc_axes()
        self.view_vector(view, up)

    def view_bc_star(self) -> None:
        view, up = self.vm.get_bc_star_axes()
        self.view_vector(view, up)

    def view_ca(self) -> None:
        view, up = self.vm.get_ca_axes()
        self.view_vector(view, up)

    def view_ca_star(self) -> None:
        view, up = self.vm.get_ca_star_axes()
        self.view_vector(view, up)

    def view_manual(self) -> None:
        view = self.vm.get_manual_axis()
        self.view_vector(view)

    def view_vector(self, view: Optional[np.ndarray], up: Optional[np.ndarray] = None) -> None:
        if view is None:
            return

        if up is not None:
            up = np.cross(view, up)
            self.plotter.view_vector(view, up)  # type: ignore
        else:
            self.plotter.view_vector(view)  # type: ignore

    def view_xy(self) -> None:
        self.plotter.view_xy()  # type: ignore

    def view_xz(self) -> None:
        self.plotter.view_xz()  # type: ignore

    def view_yx(self) -> None:
        self.plotter.view_yx()  # type: ignore

    def view_yz(self) -> None:
        self.plotter.view_yz()  # type: ignore

    def view_zx(self) -> None:
        self.plotter.view_zx()  # type: ignore

    def view_zy(self) -> None:
        self.plotter.view_zy()  # type: ignore

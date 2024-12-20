"""Controls for the volume slicer view."""

from typing import Any, Optional

import numpy as np
import pyvista as pv
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure
from matplotlib.transforms import Affine2D
from nova.trame.view.components import InputField
from nova.trame.view.layouts import GridLayout, HBoxLayout, VBoxLayout
from trame.app.file_upload import ClientFile
from trame.widgets import matplotlib
from trame.widgets import vuetify3 as vuetify

CLIMS = [
    {"title": "Min/Max", "value": "minmax"},
    {"title": "μ±3×σ", "value": "normal"},
    {"title": "Q₃/Q₁±1.5×IQR", "value": "boxplot"},
]
COLOR_MAPS = [
    {"title": "Sequential", "value": "viridis"},
    {"title": "Binary", "value": "binary"},
    {"title": "Diverging", "value": "bwr"},
    {"title": "Rainbow", "value": "turbo"},
]


class VolumeSlicerView:
    """Controls for the volume slicer view."""

    def __init__(self, view_model, plotter: pv.Plotter) -> None:
        self.vm = view_model
        self.vm.update_view()

        self.colorbar: Optional[Colorbar] = None
        self.figure_1d = Figure()
        self.figure_1d_ax = self.figure_1d.subplots(1, 1)
        self.figure_1d_window: Optional[matplotlib.Figure] = None
        self.figure_2d = Figure()
        self.figure_2d_ax = self.figure_2d.subplots(1, 1)
        self.figure_2d_window: Optional[matplotlib.Figure] = None
        self.plotter = plotter
        self.xlim: Optional[np.ndarray] = None
        self.ylim: Optional[np.ndarray] = None

        self.create_ui()

    def create_ui(self) -> None:
        with VBoxLayout():
            with GridLayout(columns=3, valign="center"):
                InputField(
                    v_model="config.clim",
                    label="Limits",
                    items=(CLIMS,),
                    type="select"
                )
                InputField(
                    v_model="config.cmap",
                    label="Color Scale",
                    items=(COLOR_MAPS,),
                    type="select",
                )
                vuetify.VBtn("Load NXS", click="trame.refs.nxs_file_input.click();")
                InputField(
                    ref="nxs_file_input",
                    v_model="vs_nxs_file",
                    classes="d-none",
                    label="Load NXS",
                    type="file",
                    update_modelValue=(self.load_nxs, "[vs_nxs_file]"),
                )

            # 2D view
            self.figure_2d_window = matplotlib.Figure(figure=self.figure_2d)
            with HBoxLayout():
                InputField(
                    v_model="config.slice_axis",
                    label="Slice Plane",
                    items=("['Axis 1/2', 'Axis 1/3', 'Axis 2/3']",),
                    type="select",
                )
                InputField(
                    v_model="config.slice_value",
                    type="slider",
                )
                InputField(
                    v_model="config.slice_value",
                    label="Slice",
                )
                InputField(
                    v_model="config.slice_thickness",
                    classes="mx-1",
                    label="Thickness",
                )
                InputField(
                    v_model="config.scale_2d",
                    items=("['Linear', 'Log']",),
                    label="Scale",
                    type="select",
                )

            # 1D view
            self.figure_1d_window = matplotlib.Figure(figure=self.figure_1d)
            with HBoxLayout(halign="center"):
                InputField(
                    v_model="config.cut_axis",
                    label="Cut Line",
                    items=("['Axis 1', 'Axis 2']",),
                    type="select",
                )
                InputField(
                    v_model="config.cut_value",
                    type="slider"
                )
                InputField(
                    v_model="config.cut_value", label="Cut"
                )
                InputField(
                    v_model="config.cut_thickness",
                    classes="mx-1",
                    label="Thickness",
                )
                InputField(
                    v_model="config.scale_1d",
                    items=("['Linear', 'Log']",),
                    label="Scale",
                    type="select",
                )

    def load_nxs(self, nxs_file: str) -> None:
        if nxs_file:
            file_obj = ClientFile(nxs_file)
            # self.vm.load_nxs(file_obj.content)

    def add_cut(self, _: Any = None) -> None:
        cut_dict = self.vm.get_cut_info()

        x = cut_dict["x"]
        y = cut_dict["y"]
        e = cut_dict["e"]

        val = cut_dict["value"]

        label = cut_dict["label"]
        title = cut_dict["title"]

        scale = self.vm.get_cut_scale()

        line_cut = self.vm.get_cut_line()

        lines = self.figure_2d_ax.get_lines()
        for line in lines:
            line.remove()

        xlim = self.xlim
        ylim = self.ylim

        thick = self.vm.get_cut_thickness()

        delta = 0 if thick is None else thick / 2

        if line_cut == "Axis 2":
            l0 = [val - delta, val - delta], ylim
            l1 = [val + delta, val + delta], ylim
        else:
            l0 = xlim, [val - delta, val - delta]  # type: ignore
            l1 = xlim, [val + delta, val + delta]  # type: ignore

        self.figure_2d_ax.plot(*l0, "w--", linewidth=1, transform=self.transform)  # type: ignore
        self.figure_2d_ax.plot(*l1, "w--", linewidth=1, transform=self.transform)  # type: ignore

        self.figure_1d_ax.clear()

        self.figure_1d_ax.errorbar(x, y, e)
        self.figure_1d_ax.set_xlabel(label)
        self.figure_1d_ax.set_yscale(scale.lower())
        self.figure_1d_ax.set_title(title)
        self.figure_1d_ax.minorticks_on()

        self.figure_1d_ax.xaxis.get_major_locator().set_params(integer=True)  # type: ignore

        if self.figure_2d_window:
            self.figure_2d_window.update(figure=self.figure_2d)
        if self.figure_1d_window:
            self.figure_1d_window.update(figure=self.figure_1d)

    def add_histo(self, _: Any = None) -> None:
        cmap = self.vm.get_color_map()
        histo_dict = self.vm.get_histo_info()
        normal = self.vm.get_normal()
        origin = self.vm.get_origin()

        if histo_dict == {}:
            return

        signal = histo_dict["signal"]
        labels = histo_dict["labels"]
        min_lim = histo_dict["min_lim"]
        max_lim = histo_dict["max_lim"]
        spacing = histo_dict["spacing"]
        projection = histo_dict["projection"]
        transform = histo_dict["transform"]
        scales = histo_dict["scales"]

        grid = pv.ImageData()
        grid.dimensions = tuple(np.array(signal.shape) + 1)
        grid.origin = min_lim
        grid.spacing = spacing

        min_bnd = min_lim * scales
        max_bnd = max_lim * scales

        bounds = np.array([[min_bnd[i], max_bnd[i]] for i in [0, 1, 2]])
        limits = np.array([[min_lim[i], max_lim[i]] for i in [0, 1, 2]])

        a = pv._vtk.vtkMatrix3x3()
        b = pv._vtk.vtkMatrix4x4()
        for i in range(3):
            for j in range(3):
                a.SetElement(i, j, transform[i, j])
                b.SetElement(i, j, projection[i, j])

        grid.cell_data["scalars"] = signal.flatten(order="F")

        if normal is not None:
            normal /= np.linalg.norm(normal)
        origin = np.dot(projection, origin)
        clim = [np.nanmin(signal), np.nanmax(signal)]

        self.clip = self.plotter.add_volume_clip_plane(
            grid,
            clim=clim,
            cmap=cmap,
            log_scale=False,
            normal=normal,
            normal_rotation=True,
            opacity="linear",
            origin=origin,
            origin_translation=True,
            render=False,
            show_scalar_bar=False,
            user_matrix=b,
        )

        prop = self.clip.GetOutlineProperty()
        prop.SetOpacity(0)

        actor = self.plotter.show_grid(
            xtitle=labels[0], ytitle=labels[1], ztitle=labels[2], font_size=8, minor_ticks=True
        )  # type: ignore

        actor.SetAxisBaseForX(*transform[:, 0])
        actor.SetAxisBaseForY(*transform[:, 1])
        actor.SetAxisBaseForZ(*transform[:, 2])

        actor.bounds = bounds.ravel()
        actor.SetXAxisRange(limits[0])
        actor.SetYAxisRange(limits[1])
        actor.SetZAxisRange(limits[2])

        axis0_args = *limits[0], actor.n_xlabels, actor.x_label_format
        axis1_args = *limits[1], actor.n_ylabels, actor.y_label_format
        axis2_args = *limits[2], actor.n_zlabels, actor.z_label_format

        axis0_label = pv.plotting.cube_axes_actor.make_axis_labels(*axis0_args)
        axis1_label = pv.plotting.cube_axes_actor.make_axis_labels(*axis1_args)
        axis2_label = pv.plotting.cube_axes_actor.make_axis_labels(*axis2_args)

        actor.SetAxisLabels(0, axis0_label)
        actor.SetAxisLabels(1, axis1_label)
        actor.SetAxisLabels(2, axis2_label)

    def add_slice(self, _: Any = None) -> None:
        cmap = self.vm.get_color_map()

        slice_dict = self.vm.get_slice_info()

        x = slice_dict["x"]
        y = slice_dict["y"]

        labels = slice_dict["labels"]
        title = slice_dict["title"]
        signal = slice_dict["signal"]

        scale = self.vm.get_slice_scale()

        vmin = np.nanmin(signal)
        vmax = np.nanmax(signal)

        if np.isclose(vmax, vmin) or not np.isfinite([vmin, vmax]).all():
            vmin, vmax = (0.1, 1) if scale == "log" else (0, 1)

        transform = slice_dict["transform"]
        aspect = slice_dict["aspect"]

        transform_inv = np.linalg.inv(transform)

        def __format_axis_coord(x: float, y: float) -> str:
            x, y, _ = np.dot(transform_inv, [x, y, 1])
            return "x={:.3f}, y={:.3f}".format(x, y)

        self.figure_2d_ax.format_coord = __format_axis_coord  # type: ignore

        transform = Affine2D(transform) + self.figure_2d_ax.transData
        self.transform = transform

        self.xlim = np.array([x.min(), x.max()])
        self.ylim = np.array([y.min(), y.max()])

        if self.colorbar is not None:
            self.colorbar.remove()

        self.figure_2d_ax.clear()

        im = self.figure_2d_ax.pcolormesh(
            x,
            y,
            signal,
            norm=scale.lower(),
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            shading="flat",
            rasterized=True,
            transform=transform,
        )

        self.figure_2d_ax.set_aspect(aspect)
        self.figure_2d_ax.set_xlabel(labels[0])
        self.figure_2d_ax.set_ylabel(labels[1])
        self.figure_2d_ax.set_title(title)
        self.figure_2d_ax.minorticks_on()

        self.figure_2d_ax.xaxis.get_major_locator().set_params(integer=True)  # type: ignore
        self.figure_2d_ax.yaxis.get_major_locator().set_params(integer=True)  # type: ignore

        self.colorbar = self.figure_2d.colorbar(im, ax=self.figure_2d_ax)
        self.colorbar.minorticks_on()

        if self.figure_2d_window:
            self.figure_2d_window.update(figure=self.figure_2d)

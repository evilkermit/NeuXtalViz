from functools import partial

from qtpy.QtWidgets import (QWidget,
                            QHBoxLayout,
                            QVBoxLayout,
                            QPushButton,
                            QLabel,
                            QTabWidget,
                            QComboBox,
                            QLineEdit,
                            QSlider,
                            QFileDialog)

from qtpy.QtGui import QDoubleValidator
from qtpy.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

import numpy as np
import pyvista as pv

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.transforms import Affine2D

from NeuXtalViz.views.utilities import update_combobox, update_lineedit

cmaps = {
    'Sequential': 'viridis',
    'Binary': 'binary',
    'Diverging': 'bwr',
    'Rainbow': 'turbo'
}

opacities = {
    'Linear': 'linear',
    'Geometric': 'geom',
    'Sigmoid': 'sigmoid'
}

class VolumeSlicerView(QWidget):

    slice_ready = pyqtSignal()
    cut_ready = pyqtSignal()

    def __init__(self, view_model, parent=None):
        super().__init__(parent)

        self.view_model = view_model

        self.tab_widget = QTabWidget(self)
        self.slicer_tab()

        self.view_model.clim_bind.connect(partial(update_combobox, self.clim_combo))
        self.view_model.cmap_bind.connect(partial(update_combobox, self.cbar_combo))
        self.view_model.cut_axis_bind.connect(partial(update_combobox, self.cut_combo))
        self.view_model.cut_thickness_bind.connect(partial(update_lineedit, self.cut_thickness_line))
        self.view_model.cut_value_bind.connect(partial(update_lineedit, self.cut_line))
        self.view_model.opacity_bind.connect(partial(update_combobox, self.opacity_combo))
        self.view_model.opacity_range_bind.connect(partial(update_combobox, self.range_combo))
        self.view_model.scale_3d_bind.connect(partial(update_combobox, self.vol_scale_combo))
        self.view_model.scale_2d_bind.connect(partial(update_combobox, self.slice_scale_combo))
        self.view_model.scale_1d_bind.connect(partial(update_combobox, self.cut_scale_combo))
        self.view_model.slice_axis_bind.connect(partial(update_combobox, self.slice_combo))
        self.view_model.slice_thickness_bind.connect(partial(update_lineedit, self.slice_thickness_line))
        self.view_model.slice_value_bind.connect(partial(update_lineedit, self.slice_line))

        self.view_model.update_view()

    def slicer_tab(self):

        slice_tab = QWidget()
        self.tab_widget.addTab(slice_tab, 'Slicer')

        notation = QDoubleValidator.StandardNotation

        validator = QDoubleValidator(-100, 100, 5, notation=notation)

        plots_layout = QVBoxLayout()
        slice_params_layout = QHBoxLayout()
        cut_params_layout = QHBoxLayout()
        draw_layout = QHBoxLayout()

        self.vol_scale_combo = QComboBox(self)
        self.opacity_combo = QComboBox(self)
        self.range_combo = QComboBox(self)
        self.clim_combo = QComboBox(self)
        self.cbar_combo = QComboBox(self)

        self.load_NXS_button = QPushButton('Load NXS', self)

        draw_layout.addWidget(self.vol_scale_combo)
        draw_layout.addWidget(self.opacity_combo)
        draw_layout.addWidget(self.range_combo)
        draw_layout.addWidget(self.clim_combo)
        draw_layout.addWidget(self.cbar_combo)
        draw_layout.addWidget(self.load_NXS_button)

        self.slice_combo = QComboBox(self)
        self.cut_combo = QComboBox(self)

        slice_label = QLabel('Slice:', self)
        cut_label = QLabel('Cut:', self)

        self.slice_line = QLineEdit()
        self.slice_line.setValidator(validator)

        self.cut_line = QLineEdit()
        self.cut_line.setValidator(validator)

        validator = QDoubleValidator(0.0001, 100, 5, notation=notation)

        slice_thickness_label = QLabel('Thickness:', self)
        cut_thickness_label = QLabel('Thickness:', self)

        self.slice_thickness_line = QLineEdit()
        self.cut_thickness_line = QLineEdit()

        self.slice_thickness_line.setValidator(validator)
        self.cut_thickness_line.setValidator(validator)

        self.slice_scale_combo = QComboBox(self)
        self.cut_scale_combo = QComboBox(self)

        slider_layout = QVBoxLayout()
        bar_layout = QHBoxLayout()

        self.min_slider = QSlider(Qt.Vertical)
        self.max_slider = QSlider(Qt.Vertical)

        self.min_slider.setRange(0, 100)
        self.max_slider.setRange(0, 100)

        self.min_slider.setValue(0)
        self.max_slider.setValue(100)

        self.min_slider.setTracking(False)
        self.max_slider.setTracking(False)

        bar_layout.addWidget(self.min_slider)
        bar_layout.addWidget(self.max_slider)

        self.save_slice_button = QPushButton('Save Slice', self)
        self.save_cut_button = QPushButton('Save Cut', self)

        slider_layout.addLayout(bar_layout)

        slice_params_layout.addWidget(self.slice_combo)
        slice_params_layout.addWidget(slice_label)
        slice_params_layout.addWidget(self.slice_line)
        slice_params_layout.addWidget(slice_thickness_label)
        slice_params_layout.addWidget(self.slice_thickness_line)
        slice_params_layout.addWidget(self.save_slice_button)
        slice_params_layout.addWidget(self.slice_scale_combo)

        cut_params_layout.addWidget(self.cut_combo)
        cut_params_layout.addWidget(cut_label)
        cut_params_layout.addWidget(self.cut_line)
        cut_params_layout.addWidget(cut_thickness_label)
        cut_params_layout.addWidget(self.cut_thickness_line)
        cut_params_layout.addWidget(self.save_cut_button)
        cut_params_layout.addWidget(self.cut_scale_combo)

        plots_layout.addLayout(draw_layout)

        self.canvas_slice = FigureCanvas(Figure(constrained_layout=True))
        self.canvas_cut = FigureCanvas(Figure(constrained_layout=True,
                                              figsize=(6.4,3.2)))

        image_layout = QHBoxLayout()
        line_layout = QHBoxLayout()

        fig_2d_layout = QVBoxLayout()
        fig_1d_layout = QVBoxLayout()

        fig_2d_layout.addWidget(NavigationToolbar2QT(self.canvas_slice, self))
        fig_2d_layout.addWidget(self.canvas_slice)

        fig_1d_layout.addWidget(NavigationToolbar2QT(self.canvas_cut, self))
        fig_1d_layout.addWidget(self.canvas_cut)

        image_layout.addLayout(fig_2d_layout)
        image_layout.addLayout(slider_layout)

        line_layout.addLayout(fig_1d_layout)

        plots_layout.addLayout(image_layout)
        plots_layout.addLayout(slice_params_layout)
        plots_layout.addLayout(line_layout)
        plots_layout.addLayout(cut_params_layout)

        self.fig_slice = self.canvas_slice.figure
        self.fig_cut = self.canvas_cut.figure

        self.ax_slice = self.fig_slice.subplots(1, 1)
        self.ax_cut = self.fig_cut.subplots(1, 1)

        self.cb = None

        slice_tab.setLayout(plots_layout)

    def save_file_dialog(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)

        filename, _ = file_dialog.getSaveFileName(self,
                                                  'Save csv file',
                                                  '',
                                                  'CSV files (*.csv)',
                                                  options=options)

        return filename

    def update_colorbar_min(self):

        min_val = self.min_slider.value()
        max_val = self.max_slider.value()

        if min_val >= max_val:
            self.min_slider.blockSignals(True)
            self.min_slider.setValue(max_val-1)
            self.min_slider.blockSignals(False)

        self.update_slice_color()

    def update_colorbar_max(self):

        min_val = self.min_slider.value()
        max_val = self.max_slider.value()

        if min_val >= max_val:
            self.max_slider.blockSignals(True)
            self.max_slider.setValue(min_val+1)
            self.max_slider.blockSignals(False)

        self.update_slice_color()

    def update_slice_color(self):

        if self.cb is not None:

            min_slider, max_slider = self.get_color_bar_values()

            vmin = self.vmin+(self.vmax-self.vmin)*min_slider/100
            vmax = self.vmin+(self.vmax-self.vmin)*max_slider/100

            self.im.set_clim(vmin=vmin, vmax=vmax)
            self.cb.update_normal(self.im)
            self.cb.minorticks_on()

            self.canvas_slice.draw_idle()
            self.canvas_slice.flush_events()

    def load_NXS_file_dialog(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)

        filename, _ = file_dialog.getOpenFileName(self,
                                                  'Load NXS file',
                                                  '',
                                                  'NXS files (*.nxs)',
                                                  options=options)

        return filename

    def add_histo(self, histo_dict, normal, norm, value):

        opacity = opacities[self.get_opacity()][self.get_range()]

        log_scale = True if self.get_vol_scale() == 'Log' else False

        cmap = cmaps[self.get_colormap()]

        self.clear_scene()

        self.norm = np.array(norm).copy()
        origin = norm
        origin[origin.index(1)] = value

        signal = histo_dict['signal']
        labels = histo_dict['labels']

        min_lim = histo_dict['min_lim']
        max_lim = histo_dict['max_lim']
        spacing = histo_dict['spacing']

        P = histo_dict['projection']
        T = histo_dict['transform']
        S = histo_dict['scales']

        grid = pv.ImageData()

        grid.dimensions = np.array(signal.shape)+1

        grid.origin = min_lim
        grid.spacing = spacing

        min_bnd = min_lim*S
        max_bnd = max_lim*S

        bounds = np.array([[min_bnd[i], max_bnd[i]] for i in [0,1,2]])
        limits = np.array([[min_lim[i], max_lim[i]] for i in [0,1,2]])

        a = pv._vtk.vtkMatrix3x3()
        b = pv._vtk.vtkMatrix4x4()
        for i in range(3):
            for j in range(3):
                a.SetElement(i,j,T[i,j])
                b.SetElement(i,j,P[i,j])

        grid.cell_data['scalars'] = signal.flatten(order='F')

        normal /= np.linalg.norm(normal)

        origin = np.dot(P, origin)

        clim = [np.nanmin(signal), np.nanmax(signal)]

        self.clip = self.plotter.add_volume_clip_plane(grid,
                                                       opacity=opacity,
                                                       log_scale=log_scale,
                                                       clim=clim,
                                                       normal=normal,
                                                       origin=origin,
                                                       origin_translation=False,
                                                       show_scalar_bar=False,
                                                       normal_rotation=False,
                                                       cmap=cmap,
                                                       user_matrix=b)

        prop = self.clip.GetOutlineProperty()
        prop.SetOpacity(0)

        prop = self.clip.GetEdgesProperty()
        prop.SetOpacity(0)

        actor = self.plotter.show_grid(xtitle=labels[0],
                                       ytitle=labels[1],
                                       ztitle=labels[2],
                                       font_size=8,
                                       minor_ticks=True)

        actor.SetAxisBaseForX(*T[:,0])
        actor.SetAxisBaseForY(*T[:,1])
        actor.SetAxisBaseForZ(*T[:,2])

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

        self.reset_scene()

        self.clip.AddObserver('InteractionEvent', self.interaction_callback)

        self.P_inv = np.linalg.inv(P)

    def interaction_callback(self, caller, event):

        orig = caller.GetOrigin()
        #norm = caller.GetNormal()

        #norm /= np.linalg.norm(norm)
        #norm = self.norm

        ind = np.array(self.norm).tolist().index(1)

        value = np.dot(self.P_inv, orig)[ind]

        self.slice_line.blockSignals(True)
        self.set_slice_value(value)
        self.slice_line.blockSignals(False)

        self.slice_ready.emit()

    def __format_axis_coord(self, x, y):

        x, y, _ = np.dot(self.T_inv, [x, y, 1])
        return 'x={:.3f}, y={:.3f}'.format(x, y)

    def add_slice(self, slice_dict):

        self.max_slider.blockSignals(True)
        self.max_slider.setValue(100)
        self.max_slider.blockSignals(False)

        self.min_slider.blockSignals(True)
        self.min_slider.setValue(0)
        self.min_slider.blockSignals(False)

        cmap = cmaps[self.get_colormap()]

        x = slice_dict['x']
        y = slice_dict['y']

        labels = slice_dict['labels']
        title = slice_dict['title']
        signal = slice_dict['signal']

        scale = self.get_slice_scale()

        vmin = np.nanmin(signal)
        vmax = np.nanmax(signal)

        if np.isclose(vmax, vmin) or not np.isfinite([vmin, vmax]).all():
            vmin, vmax = (0.1, 1) if scale == 'log' else (0, 1)

        T = slice_dict['transform']
        aspect = slice_dict['aspect']

        self.T_inv = np.linalg.inv(T)

        self.ax_slice.format_coord = self.__format_axis_coord

        transform = Affine2D(T)+self.ax_slice.transData
        self.transform = transform

        self.xlim = np.array([x.min(), x.max()])
        self.ylim = np.array([y.min(), y.max()])

        if self.cb is not None:
            self.cb.remove()

        self.ax_slice.clear()

        im = self.ax_slice.pcolormesh(x,
                                      y,
                                      signal,
                                      norm=scale,
                                      cmap=cmap,
                                      vmin=vmin,
                                      vmax=vmax,
                                      shading='flat',
                                      rasterized=True,
                                      transform=transform)

        self.im = im
        self.vmin, self.vmax = self.im.norm.vmin, self.im.norm.vmax

        self.ax_slice.set_aspect(aspect)
        self.ax_slice.set_xlabel(labels[0])
        self.ax_slice.set_ylabel(labels[1])
        self.ax_slice.set_title(title)
        self.ax_slice.minorticks_on()

        self.ax_slice.xaxis.get_major_locator().set_params(integer=True)
        self.ax_slice.yaxis.get_major_locator().set_params(integer=True)

        self.cb = self.fig_slice.colorbar(self.im, ax=self.ax_slice)
        self.cb.minorticks_on()

        self.canvas_slice.draw_idle()
        self.canvas_slice.flush_events()

    def add_cut(self, cut_dict):

        x = cut_dict['x']
        y = cut_dict['y']
        e = cut_dict['e']

        val = cut_dict['value']

        label = cut_dict['label']
        title = cut_dict['title']

        scale = self.get_cut_scale()

        line_cut = self.get_cut()

        lines = self.ax_slice.get_lines()
        for line in lines:
            line.remove()

        xlim = self.xlim
        ylim = self.ylim

        thick = self.get_cut_thickness()

        delta = 0 if thick is None else thick/2

        if line_cut == 'Axis 2':
            l0 = [val-delta, val-delta], ylim
            l1 = [val+delta, val+delta], ylim
            direction = 'vertical'
        else:
            l0 = xlim, [val-delta, val-delta]
            l1 = xlim, [val+delta, val+delta]
            direction = 'horizontal'

        self.ax_slice.plot(*l0, 'w--', linewidth=1, transform=self.transform)
        self.ax_slice.plot(*l1, 'w--', linewidth=1, transform=self.transform)

        self.ax_cut.clear()

        self.ax_cut.errorbar(x, y, e)
        self.ax_cut.set_xlabel(label)
        self.ax_cut.set_yscale(scale)
        self.ax_cut.set_title(title)
        self.ax_cut.minorticks_on()

        self.ax_cut.xaxis.get_major_locator().set_params(integer=True)

        self.canvas_cut.draw_idle()
        self.canvas_cut.flush_events()

        self.canvas_slice.draw_idle()
        self.canvas_slice.flush_events()

        self.linecut = {'is_dragging': False,
                        'line_cut': (xlim, ylim, delta, direction)}

        self.fig_slice.canvas.mpl_connect('button_press_event',
                                          self.on_press)

        self.fig_slice.canvas.mpl_connect('button_release_event',
                                          self.on_release)

        self.fig_slice.canvas.mpl_connect('motion_notify_event',
                                          self.on_motion)

    def on_press(self, event):

        if event.inaxes == self.ax_slice and \
            self.fig_slice.canvas.toolbar.mode == '':

            self.linecut['is_dragging'] = True

    def on_release(self, event):

        self.linecut['is_dragging'] = False

        self.cut_ready.emit()

    def on_motion(self, event):

        if self.linecut['is_dragging'] and event.inaxes == self.ax_slice:

            lines = self.ax_slice.get_lines()
            for line in lines:
                line.remove()

            xlim, ylim, delta, direction = self.linecut['line_cut']

            x, y, _ = np.dot(self.T_inv, [event.xdata, event.ydata, 1])

            self.cut_line.blockSignals(True)

            if direction == 'vertical':
                l0 = [x-delta, x-delta], ylim
                l1 = [x+delta, x+delta], ylim
                self.set_cut_value(x)
            else:
                l0 = xlim, [y-delta, y-delta]
                l1 = xlim, [y+delta, y+delta]
                self.set_cut_value(y)

            self.cut_line.blockSignals(False)

            self.ax_slice.plot(*l0,
                               'w--',
                               linewidth=1,
                               transform=self.transform)

            self.ax_slice.plot(*l1,
                               'w--',
                               linewidth=1,
                               transform=self.transform)

            self.canvas_slice.draw_idle()
            self.canvas_slice.flush_events()

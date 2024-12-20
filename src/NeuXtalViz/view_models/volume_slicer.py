from mvvm_lib.interface import BindingInterface

from NeuXtalViz.models.volume_slicer import VolumeSlicerModel


class VolumeSlicerViewModel:
    def __init__(self, binding: BindingInterface) -> None:
        self.model = VolumeSlicerModel()

        self.config = self.model.config.volume_slicer
        self.config_bind = binding.new_bind(self.config)

        self.add_cut_bind = binding.new_bind()
        self.add_slice_bind = binding.new_bind()
        self.cut_data_bind = binding.new_bind()
        self.redraw_data_bind = binding.new_bind()
        self.slice_data_bind = binding.new_bind()
        self.set_oriented_lattice_parameters_bind = binding.new_bind()

    def update_view(self) -> None:
        self.config_bind.update_in_view(self.config)

    def update_slice(self):

        if self.model.is_histo_loaded():

            self.slice_data_bind.update_in_view(None)

    def update_cut(self):

        if self.model.is_histo_loaded():

            self.cut_data_bind.update_in_view(None)

    def load_NXS(self, filename, progress):

        if filename:

            progress('Processing...', 1)

            progress('Loading NeXus file...', 10)

            self.model.load_md_histo_workspace(filename)

            progress('Loading NeXus file...', 50)

            progress('Loading NeXus file...', 80)

            progress('NeXus file loaded!', 100)

        else:

            progress('Invalid parameters.', 0)

    def load_NXS_complete(self, result):

        self.update_oriented_lattice()

    def update_oriented_lattice(self):
        ol = self.model.get_oriented_lattice_parameters()
        if ol is not None:
            self.set_oriented_lattice_parameters_bind.update_in_view(ol)

    def get_normal(self):

        slice_plane = self.config.slice_axis

        if slice_plane == 'Axis 1/2':
            norm = [0,0,1]
        elif slice_plane == 'Axis 1/3':
            norm = [0,1,0]
        else:
            norm = [1,0,0]

        return norm

    def get_axis(self):

        axis = [1 if not norm else 0 for norm in self.get_normal()]
        ind = [i for i, ax in enumerate(axis) if ax == 1]

        line_cut = self.config.cut_axis

        if line_cut == 'Axis 1':
            axis[ind[0]] = 0
        else:
            axis[ind[1]] = 0

        return axis

    def get_clim_method(self):

        ctype = self.config.clim

        if ctype == 'μ±3×σ':
            method = 'normal'
        elif ctype == 'Q₃/Q₁±1.5×IQR':
            method = 'boxplot'
        else:
            method = None

        return method

    def set_cut_value(self, value):

        self.config.cut_value = value

    def set_slice_value(self, value):

        self.config.slice_value = value

    def redraw_data(self, progress):

        if self.model.is_histo_loaded():

            progress('Processing...', 1)

            progress('Updating volume...', 20)

            norm = self.get_normal()

            histo = self.model.get_histo_info(norm)

            data = histo['signal']

            data = self.model.calculate_clim(data, self.get_clim_method())

            progress('Updating volume...', 50)

            histo['signal'] = data

            value = self.config.slice_value

            normal = -self.model.get_normal('[uvw]', norm)

            # origin = self.model.get_normal('[hkl]', orig)

            if value is not None:

                progress('Volume drawn!', 100)

                return histo, normal, norm, value, self.model.get_transform()

            else:

                progress('Invalid parameters.', 0)

    def redraw_data_complete(self, result):

        if result is not None:

            self.redraw_data_bind.update_in_view((self.config, result))

    def slice_data(self, progress):

        if self.model.is_histo_loaded():

            norm = self.get_normal()

            thick = self.config.slice_thickness
            value = self.config.slice_value

            if thick is not None:

                progress('Processing...', 1)

                progress('Updating slice...', 50)

                slice_histo = self.model.get_slice_info(norm, value, thick)

                data = slice_histo['signal']

                data = self.model.calculate_clim(data, self.get_clim_method())

                slice_histo['signal'] = data

                progress('Data sliced!', 100)

                return slice_histo

    def slice_data_complete(self, result):

        if result is not None:

            self.add_slice_bind.update_in_view((self.config, result))

    def cut_data(self, progress):

        if self.model.is_sliced():

            value = self.config.cut_value
            thick = self.config.cut_thickness

            axis = self.get_axis()

            if value is not None and thick is not None:

                progress('Processing...', 1)

                progress('Updating cut...', 50)

                progress('Data cut!', 100)

                cut_histo = self.model.get_cut_info(axis, value, thick)

                return cut_histo

    def cut_data_complete(self, result):

        if result is not None:

            self.add_cut_bind.update_in_view((self.config, result))

    def save_slice(self, filename):

        if self.model.is_sliced():

            self.model.save_slice(filename)

    def save_cut(self, filename):

        if self.model.is_cut():

            self.model.save_cut(filename)

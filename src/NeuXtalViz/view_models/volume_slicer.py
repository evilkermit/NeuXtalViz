from typing import Any, Optional

from mvvm_lib.interface import BindingInterface

from NeuXtalViz.models.volume_slicer import VolumeSlicerModel


class VolumeSlicerViewModel:
    def __init__(self, binding: BindingInterface) -> None:
        self.model = VolumeSlicerModel()

        self.clim_bind = binding.new_bind()
        self.cmap_bind = binding.new_bind()
        self.cut_axis_bind = binding.new_bind()
        self.cut_thickness_bind = binding.new_bind()
        self.cut_value_bind = binding.new_bind()
        self.opacity_bind = binding.new_bind()
        self.opacity_range_bind = binding.new_bind()
        self.render_bind = binding.new_bind()
        self.scale_3d_bind = binding.new_bind()
        self.scale_2d_bind = binding.new_bind()
        self.scale_1d_bind = binding.new_bind()
        self.slice_axis_bind = binding.new_bind()
        self.slice_thickness_bind = binding.new_bind()
        self.slice_value_bind = binding.new_bind()
        self.transform_bind = binding.new_bind()

    def get_clim_method(self) -> Optional[str]:
        if self.model.config.volume_slicer.clim == 'μ±3×σ':
            method = 'normal'
        elif self.model.config.volume_slicer.clim == 'Q₃/Q₁±1.5×IQR':
            method = 'boxplot'
        else:
            method = None

        return method

    def get_normal(self):
        if self.model.config.volume_slicer.slice_axis == 'Axis 1/2':
            norm = [0,0,1]
        elif self.model.config.volume_slicer.slice_axis == 'Axis 1/3':
            norm = [0,1,0]
        else:
            norm = [1,0,0]

        return norm

    def load_NXS(self, filename: str, progress: callable):
        if filename:
            progress('Processing...', 1)
            progress('Loading NeXus file...', 10)

            self.model.load_md_histo_workspace(filename)

            progress('Loading NeXus file...', 50)
            progress('Loading NeXus file...', 80)
            progress('NeXus file loaded!', 100)
        else:
            progress('Invalid parameters.', 0)

    def load_NXS_complete(self, _) -> None:
        self.update_oriented_lattice()

    def redraw_data(self, progress) -> Optional[Any]:
        if self.model.is_histo_loaded():
            progress('Processing...', 1)
            progress('Updating volume...', 20)

            norm = self.get_normal()
            normal = -self.model.get_normal('[uvw]', norm)

            histo = self.model.get_histo_info(norm)

            data = histo['signal']
            data = self.model.calculate_clim(data, self.get_clim_method())

            progress('Updating volume...', 50)

            histo['signal'] = data

            value = self.model.config.volume_slicer.slice_value
            if value is not None:
                progress('Volume drawn!', 100)

                return histo, normal, norm, value, self.model.get_transform()
            else:
                progress('Invalid parameters.', 0)

    def redraw_data_complete(self, result) -> None:
        if result is not None:
            histo, normal, norm, value, trans = result

            self.render_bind.update_in_view((histo, normal, norm, value))
            # TODO: move to base view model
            self.transform_bind.update_in_view(trans)

    def update_oriented_lattice(self) -> None:
        # TODO
        pass

    def update_view(self) -> None:
        self.clim_bind.update_in_view(self.model.config.volume_slicer.clim)
        self.cmap_bind.update_in_view(self.model.config.volume_slicer.cmap)
        self.cut_axis_bind.update_in_view(self.model.config.volume_slicer.cut_axis)
        self.cut_thickness_bind.update_in_view(self.model.config.volume_slicer.cut_thickness)
        self.cut_value_bind.update_in_view(self.model.config.volume_slicer.cut_value)
        self.opacity_bind.update_in_view(self.model.config.volume_slicer.opacity)
        self.opacity_range_bind.update_in_view(self.model.config.volume_slicer.opacity_range)
        self.scale_3d_bind.update_in_view(self.model.config.volume_slicer.scale_3d)
        self.scale_2d_bind.update_in_view(self.model.config.volume_slicer.scale_2d)
        self.scale_1d_bind.update_in_view(self.model.config.volume_slicer.scale_1d)
        self.slice_axis_bind.update_in_view(self.model.config.volume_slicer.slice_axis)
        self.slice_thickness_bind.update_in_view(self.model.config.volume_slicer.slice_thickness)
        self.slice_value_bind.update_in_view(self.model.config.volume_slicer.slice_value)

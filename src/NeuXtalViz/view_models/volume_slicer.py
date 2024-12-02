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
        self.scale_3d_bind = binding.new_bind()
        self.scale_2d_bind = binding.new_bind()
        self.scale_1d_bind = binding.new_bind()
        self.slice_axis_bind = binding.new_bind()
        self.slice_thickness_bind = binding.new_bind()
        self.slice_value_bind = binding.new_bind()

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

from nova.mvvm.interface import BindingInterface


class VisualizationPanelViewModel:
    def __init__(self, binding: BindingInterface) -> None:
        self.clear_scene_bind = binding.new_bind()
        self.reset_view_bind = binding.new_bind()
        self.reset_scene_bind = binding.new_bind()

    def clear_scene(self) -> None:
        self.clear_scene_bind.update_in_view(None)

    def reset_view(self) -> None:
        self.reset_view_bind.update_in_view(None)

    def reset_scene(self) -> None:
        self.reset_scene_bind.update_in_view(None)

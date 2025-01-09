"""Creates models and view models."""

from typing import Any

from nova.mvvm.interface import BindingInterface

from NeuXtalViz.view_models.visualization_panel import VisualizationPanelViewModel
from NeuXtalViz.view_models.volume_slicer import VolumeSlicerViewModel


def create_viewmodels(binding: BindingInterface) -> dict[str, Any]:
    vm: dict[str, Any] = {}
    vm["viz_panel"] = VisualizationPanelViewModel(binding)
    vm["volume_slicer"] = VolumeSlicerViewModel(binding, vm["viz_panel"])

    return vm

"""Creates models and view models."""

from typing import Any

from nova.mvvm.interface import BindingInterface

from NeuXtalViz.view_models.volume_slicer import VolumeSlicerViewModel


def create_viewmodels(binding: BindingInterface) -> dict[str, Any]:
    vm: dict[str, Any] = {}
    vm["main"] = {}
    vm["volume_slicer"] = VolumeSlicerViewModel(binding)

    return vm

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ClimEnum(str, Enum):
    minmax = 'Min/Max'
    mean = 'μ±3×σ'
    iqr = 'Q₃/Q₁±1.5×IQR'


class ColorMapEnum(str, Enum):
    sequential = 'Sequential'
    binary = 'Binary'
    diverging = 'Diverging'
    rainbow = 'Rainbow'


class CutAxisEnum(str, Enum):
    axis_1 = 'Axis 1'
    axis_2 = 'Axis 2'


class OpacityEnum(str, Enum):
    linear = 'Linear'
    geometric = 'Geometric'
    sigmoid = 'Sigmoid'


class ScaleEnum(str, Enum):
    linear = 'Linear'
    log = 'Log'


class SliceAxisEnum(str, Enum):
    axis_1_2 = 'Axis 1/2'
    axis_1_3 = 'Axis 1/3'
    axis_2_3 = 'Axis 2/3'


class CameraConfig(BaseModel):
    axes: list[Optional[float]] = [None, None, None]
    parallel_projection: bool = False
    reciprocal_lattice: bool = True
    type: str = '[hkl]'


class VolumeSlicer(BaseModel):
    # volume rendering options
    clim: ClimEnum = ClimEnum.iqr
    cmap: ColorMapEnum = ColorMapEnum.sequential
    opacity: OpacityEnum = OpacityEnum.linear
    opacity_reverse: bool = False
    scale_3d: ScaleEnum = ScaleEnum.linear

    # slice options
    slice_axis: SliceAxisEnum = SliceAxisEnum.axis_1_2
    slice_thickness: float = 0.1
    slice_value: float = 0.0
    scale_2d: ScaleEnum = ScaleEnum.linear

    # cut options
    cut_axis: CutAxisEnum = CutAxisEnum.axis_1
    cut_thickness: float = 0.1
    cut_value: float = 0.0
    scale_1d: ScaleEnum = ScaleEnum.linear


class Config(BaseModel):
    camera: CameraConfig = CameraConfig()
    volume_slicer: VolumeSlicer = VolumeSlicer()


class SharedConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

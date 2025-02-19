from nova.mvvm.pyqt5_binding import PyQt5Binding
from pydantic import BaseModel, Field

from NeuXtalViz.presenters.base_view_model import NeuXtalVizViewModel


class ModulationControls(BaseModel):
    eps: float = Field(default=0.025)
    min: int = Field(default=15)


class Modulation(NeuXtalVizViewModel):
    def __init__(self, view, model):
        self.mod_controls = ModulationControls()

        binding = PyQt5Binding()

        self.add_peaks_bind = binding.new_bind()
        self.update_table_bind = binding.new_bind()

        super(Modulation, self).__init__(view, model)

    def set_cluster_param(self, key, value):
        setattr(self.mod_controls, key, value)

    def cluster_complete(self, result):
        if result is not None:
            self.update_processing("Adding peaks.", 30)
            self.add_peaks_bind.update_in_view(result)
            self.update_table_bind.update_in_view(result)
            self.update_processing("Peaks added!", 0)

    def cluster_process(self, progress):
        params = [self.mod_controls.eps, self.mod_controls.min]

        if params is not None:
            progress("Invalid parameters.", 0)

            peak_info = self.model.get_peak_info()
            if peak_info is not None:
                progress("Clustering peaks.", 25)

                success = self.model.cluster_peaks(peak_info, *params)

                if success:
                    progress("Peaks clustered!", 100)

                    return peak_info

                else:
                    progress("Invalid cluster.", 0)

        else:
            progress("Invalid parameters.", 0)

    def load_UB(self, filename):
        self.update_processing("Loading peaks.", 30)

        self.model.load_UB(filename)

        self.update_oriented_lattice()

        self.transform_bind.update_in_view(self.model.get_transform())

        self.update_processing("UB loaded!", 0)

    def load_peaks(self, filename):
        self.update_processing("Loading peaks.", 30)

        self.model.load_peaks(filename)

        self.update_processing("Peaks loaded!", 0)

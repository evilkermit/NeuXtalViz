import numpy as np

from NeuXtalViz.presenters.base_presenter import NeuXtalVizPresenter

class UB(NeuXtalVizPresenter):

    def __init__(self, view, model):

        super(UB, self).__init__(view, model)

        self.view.connect_load_Q(self.load_Q)
        self.view.connect_save_Q(self.save_Q)
        self.view.connect_load_peaks(self.load_peaks)
        self.view.connect_save_peaks(self.save_peaks)
        self.view.connect_load_UB(self.load_UB)
        self.view.connect_save_UB(self.save_UB)
        self.view.connect_switch_instrument(self.switch_instrument)
        self.view.connect_wavelength(self.update_wavelength)

        self.view.connect_browse_calibration(self.load_detector_calibration)
        self.view.connect_browse_tube(self.load_tube_calibration)

        self.view.connect_convert_Q(self.convert_Q)
        self.view.connect_find_peaks(self.find_peaks)
        self.view.connect_index_peaks(self.index_peaks)
        self.view.connect_predict_peaks(self.predict_peaks)
        self.view.connect_integrate_peaks(self.integrate_peaks)
        self.view.connect_filter_peaks(self.filter_peaks)
        self.view.connect_find_conventional(self.find_conventional)
        self.view.connect_lattice_transform(self.lattice_transform)
        self.view.connect_symmetry_transform(self.symmetry_transform)
        self.view.connect_transform_UB(self.transform_UB)
        self.view.connect_optimize_UB(self.refine_UB)
        self.view.connect_find_niggli(self.find_niggli)
        self.view.connect_calculate_peaks(self.calculate_peaks)
        self.view.connect_cell_row_highligter(self.highlight_cell)
        self.view.connect_peak_row_highligter(self.highlight_peak)
        self.view.connect_select_cell(self.select_cell)

        self.switch_instrument()
        self.lattice_transform()

    def convert_Q(self):

        instrument = self.view.get_instrument()
        wavelength = self.view.get_wavelength()
        tube_cal = self.view.get_tube_calibration()
        det_cal = self.view.get_detector_calibration()

        IPTS = self.view.get_IPTS()
        runs = self.view.get_runs()
        exp = self.view.get_experiment()
        lorentz = self.view.get_lorentz()
        time_stop = self.view.get_time_stop()

        validate = [IPTS, runs, time_stop, wavelength]

        if instrument == 'DEMAND':
            validate.append(exp)

        if all(elem is not None for elem in validate):

            self.update_processing()

            self.update_processing('Data loading...', 10)

            self.model.load_data(instrument,
                                 IPTS,
                                 runs,
                                 exp,
                                 time_stop)

            self.update_processing('Data loaded...', 40)

            self.update_processing('Data calibrating...', 50)

            self.model.calibrate_data(instrument, det_cal, tube_cal)

            self.update_processing('Data calibrated...', 60)

            self.update_processing('Data converting...', 70)

            self.model.convert_data(instrument, wavelength, lorentz)

            self.update_processing('Data converted...', 99)

            self.visualize()

            self.update_complete('Data converted!')

        else:

            self.update_invalid()

    def visualize(self):

        Q_hist = self.model.get_Q_info()

        if Q_hist is not None:

            self.view.add_Q_viz(Q_hist)

            if self.model.has_UB():

                self.model.update_UB()

                self.update_oriented_lattice()

                self.view.set_transform(self.model.get_transform())

                self.update_lattice_info()

            if self.model.has_peaks():

                peaks = self.model.get_peak_info()

                self.view.update_peaks_table(peaks)

    def update_lattice_info(self):

        params = self.model.get_lattice_constants()

        if params is not None:

            self.view.set_lattice_constants(params)

        params = self.model.get_sample_directions()

        if params is not None:

            self.view.set_sample_directions(params)

    def find_peaks(self):

        if self.model.has_Q():

            dist = self.view.get_find_peaks_distance()
            params = self.view.get_find_peaks_parameters()
            edge = self.view.get_find_peaks_edge()

            if dist is not None and params is not None:

                self.model.find_peaks(dist, *params, edge)

                self.visualize()

                self.view.clear_niggli_info()

    def find_conventional(self):

        if self.model.has_peaks():

            params = self.view.get_lattice_constants()
            tol = self.view.get_calculate_UB_tol()

            if params is not None and tol is not None:

                self.model.determine_UB_with_lattice_parameters(*params, tol)

                self.visualize()

                self.view.clear_niggli_info()

    def find_niggli(self):

        if self.model.has_peaks():

            params = self.view.get_min_max_constants()
            tol = self.view.get_calculate_UB_tol()

            if params is not None and tol is not None:

                self.model.determine_UB_with_niggli_cell(*params, tol)

                self.visualize()

                self.show_cells()

    def show_cells(self):

        if self.model.has_peaks() and self.model.has_UB():

            scalar = self.view.get_max_scalar_error()

            if scalar is not None:

                cells = self.model.possible_conventional_cells(scalar)
                self.view.update_cell_table(cells)

    def select_cell(self):

        if self.model.has_peaks() and self.model.has_UB():

            form = self.view.get_form_number()
            tol = self.view.get_calculate_UB_tol()

            if form is not None and tol is not None:

                self.model.select_cell(form, tol)

                self.visualize()

                self.view.clear_niggli_info()

    def highlight_cell(self):

        form = self.view.get_form()
        self.view.set_cell_form(form)

    def highlight_peak(self):

        no = self.view.get_peak()
        if no is not None:
            peak = self.model.get_peak(no)
            self.view.set_peak_info(peak)
            # self.view.highlight_peak(no)

    def lattice_transform(self):

        cell = self.view.get_lattice_transform()

        Ts = self.model.generate_lattice_transforms(cell)

        self.view.update_symmetry_symbols(list(Ts.keys()))

        self.symmetry_transform()

    def symmetry_transform(self):

        cell = self.view.get_lattice_transform()

        Ts = self.model.generate_lattice_transforms(cell)

        symbol = self.view.get_symmetry_symbol()

        if symbol in Ts.keys():

            T = Ts[symbol]

            self.view.set_transform_matrix(T)

    def transform_UB(self):

        if self.model.has_peaks() and self.model.has_UB():

            params = self.view.get_transform_matrix()
            tol = self.view.get_transform_UB_tol()

            if params is not None and tol is not None:

                self.model.transform_lattice(params, tol)

                self.visualize()

                self.view.clear_niggli_info()

    def refine_UB(self):

        if self.model.has_peaks() and self.model.has_UB():

            params = self.view.get_lattice_constants()
            tol = self.view.get_refine_UB_tol()
            option = self.view.get_refine_UB_option()

            if option == 'Constrained' and params is not None:
                self.model.refine_U_only(*params)
                self.visualize()
            elif tol is not None:
                if option == 'Unconstrained':
                    self.model.refine_UB_without_constraints(tol)
                else:
                    self.model.refine_UB_with_constraints(option, tol)
                self.visualize()
                self.view.clear_niggli_info()

    def get_modulation_info(self):

        mod_info = self.view.get_max_order_cross_terms()
        if mod_info is not None:
            max_order, cross_terms = mod_info
        else:
            max_order, cross_terms = 0, False

        mod_vec = self.view.get_modulatation_offsets()
        if mod_vec is not None:
            mod_vec_1 = mod_vec[0:3]
            mod_vec_2 = mod_vec[3:6]
            mod_vec_3 = mod_vec[6:9]

        return mod_vec_1, mod_vec_2, mod_vec_3, max_order, cross_terms

    def index_peaks(self):

        mod_info = self.get_modulation_info()

        mod_vec_1, mod_vec_2, mod_vec_3, max_order, cross_terms = mod_info

        if self.model.has_peaks() and self.model.has_UB():

            params = self.view.get_index_peaks_parameters()
            sat = self.view.get_index_satellite_peaks()
            round_hkl = self.view.get_index_peaks_round()

            if params is not None:

                tol, sat_tol = params

                if sat == False:
                    max_order = 0

                self.model.index_peaks(tol,
                                       sat_tol,
                                       mod_vec_1,
                                       mod_vec_2,
                                       mod_vec_3,
                                       max_order,
                                       cross_terms,
                                       round_hkl=round_hkl)

                self.visualize()

    def predict_peaks(self):

        mod_info = self.get_modulation_info()

        mod_vec_1, mod_vec_2, mod_vec_3, max_order, cross_terms = mod_info

        centering = self.view.get_predict_peaks_centering()

        wavelength = self.view.get_wavelength()

        params = self.view.get_predict_peaks_parameters()

        # sat = self.view.get_predict_satellite_peaks()

        edge = self.view.get_predict_peaks_edge()

        if self.model.has_peaks() and self.model.has_UB():

            if wavelength is not None and params is not None:

                d_min, sat_d_min = params

                if sat_d_min < d_min:
                    sat_d_min = d_min

                lamda_min, lamda_max = wavelength

                if np.isclose(lamda_min, lamda_max):
                    lamda_min, lamda_max = 0.97*lamda_min, 1.03*lamda_max

                self.model.predict_peaks(centering,
                                         d_min,
                                         lamda_min,
                                         lamda_max,
                                         edge)

                self.visualize()

    def integrate_peaks(self):

        params = self.view.get_integrate_peaks_parameters()

        ellipsoid = self.view.get_ellipsoid()

        centroid = self.view.get_centroid()

        if self.model.has_peaks() and self.model.has_Q():

            if params is not None:

                method = 'ellipsoid' if ellipsoid else 'sphere'

                rad, inner_factor, outer_factor = params
                
                if inner_factor < 1:
                    inner_factor = 1
                if outer_factor < inner_factor:
                    outer_factor = inner_factor

                self.model.integrate_peaks(rad,
                                           inner_factor,
                                           outer_factor,
                                           method=method,
                                           centroid=centroid)

                self.visualize()

    def filter_peaks(self):

        name = self.view.get_filter_variable()
        operator = self.view.get_filter_comparison()
        value = self.view.get_filter_value()

        if self.model.has_peaks() and value is not None:

            self.model.filter_peaks(name, operator, value)

            self.visualize()

    def load_detector_calibration(self):

        filename = self.view.load_detector_cal_dialog()

        if filename:

            self.view.set_detector_calibration(filename)

    def load_tube_calibration(self):

        filename = self.view.load_tube_cal_dialog()

        if filename:

            self.view.set_tube_calibration(filename)

    def load_Q(self):

        filename = self.view.load_Q_file_dialog()

        if filename:

            self.model.load_Q(filename)

    def save_Q(self):

        filename = self.view.save_Q_file_dialog()

        if filename:

            self.model.save_Q(filename)

    def load_peaks(self):

        filename = self.view.load_peaks_file_dialog()

        if filename:

            self.model.load_peaks(filename)

    def save_peaks(self):

        filename = self.view.save_peaks_file_dialog()

        if filename:

            self.model.save_peaks(filename)

    def load_UB(self):

        filename = self.view.load_UB_file_dialog()

        if filename:

            self.model.load_UB(filename)

            self.view.set_transform(self.model.get_transform())

    def save_UB(self):

        filename = self.view.save_UB_file_dialog()

        if filename:

            self.model.save_UB(filename)

    def switch_instrument(self):

        instrument = self.view.get_instrument()

        wavelength = self.model.get_wavelength(instrument)
        self.view.set_wavelength(wavelength)

        filepath = self.model.get_raw_file_path(instrument)
        self.view.clear_run_info(filepath)

    def update_wavelength(self):

        wl_min, wl_max = self.view.get_wavelength()
        self.view.update_wavelength(wl_min)

    def calculate_peaks(self):

        hkl_1, hkl_2 = self.view.get_input_hkls()
        constants = self.view.get_lattice_constants()
        if constants is not None:
            d_phi = self.model.calculate_peaks(hkl_1, hkl_2, *constants)
            self.view.set_d_phi(*d_phi)
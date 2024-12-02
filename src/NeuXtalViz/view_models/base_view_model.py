from mvvm_lib.interface import BindingInterface


class NeuXtalVizViewModel:
    def __init__(self, binding: BindingInterface) -> None:
        self.status = ''
        self.step = 0

        self.status_bind = binding.new_bind()
        self.step_bind = binding.new_bind()

    def update_processing(self, status: str, step: int) -> None:
        self.status = status
        self.step = step

        self.update_view()

    def update_view(self) -> None:
        self.status_bind.update_in_view(self.status)
        self.step_bind.update_in_view(self.step)

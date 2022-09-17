from matplotlib import pyplot as plt
import seaborn as sns

from Model.model import Model


class Graphics:
    def __init__(self, steps_count: int, time_step: float, model: Model):
        self.steps_count = steps_count
        self.time_step = time_step
        self.model = model

    def draw(self):
        for current_step in range(self.steps_count):
            a = self.model.get(current_step * self.time_step)
            print(a)

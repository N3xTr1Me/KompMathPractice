import datetime
import random

from Model.model import Model
from Graphics.graphics import Graphics

dims = (10, 10)
time = 0.2
time_step = 0.001
steps_count = int(time / time_step)

model = Model(T=time, step=time_step, dimensions=dims, right_side=lambda x, y: random.randint(1, 10))
model.run_algorithm()

# graphics = Graphics(steps_count, time_step, model)
# graphics.draw()

print()

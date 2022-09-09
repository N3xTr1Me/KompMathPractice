import datetime
import random

from Model.model import Model


dims = (10, 10)
time = 10
time_step = 0.5

start_1 = datetime.datetime.now()
m = Model(T=time, step=time_step, dimensions=dims, right_side=lambda x, y: random.randint(1, 10))

start_2 = datetime.datetime.now()
m.run_algorithm()
print(datetime.datetime.now() - start_2)
print(datetime.datetime.now() - start_1)

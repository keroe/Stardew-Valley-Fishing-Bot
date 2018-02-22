import numpy as np

folder = 'userdata/'

for file in folder:
	data = list(np.load(file))
	frames = len(data)
class  LineForChart:
    def __init__(self):
        self.x = []
        self.y = []
        
import numpy as np
class DataBackup:
    def __init__(self):
        self.dict = {
            "dead": np.array([]),
            "constant": np.array([]),
            "exploded": np.array([]),
            "time_dead": np.arange(1, sim.time + 1, dtype=int),
            "time_constant": np.arange(1, sim.time + 1, dtype=int),
            "time_exploded": np.arange(1, sim.time + 1, dtype=int)
        }

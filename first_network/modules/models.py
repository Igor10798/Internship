class  LineForChart:
    def __init__(self, x_axis = [], y_axis = []):
        self.x = x_axis
        self.y = y_axis
        
class DataBackup:
    def __init__(self, time):
        self.dict = {
            "dead": np.array([]),
            "constant": np.array([]),
            "exploded": np.array([]),
            "time_dead": np.arange(1, time + 1, dtype=int),
            "time_constant": np.arange(1, time + 1, dtype=int),
            "time_exploded": np.arange(1, time + 1, dtype=int)
        }

import numpy as np

# simple class for controlPoint handling
class DronePoint: 
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.pos = np.array([self.x, self.y, self.z])

    def set_pos(self, pos_):
        self.pos = pos_
        self.x = pos_[0]
        self.y = pos_[1]
        self.z = pos_[2]
    
    def get_pos(self):
        return np.array([self.x, self.y, self.z])
    

    def set_displacement(self, dx, dy, dz, dabs):
        self.displacement = [dx, dy, dz, dabs]

    
    def set_distance_from_origin(self, distance_from_origin):
        self.distance_from_origin = distance_from_origin

    
    def set_status(self, status):
        self.status = status





class ManualPoint:
    def __init__(self, name, distance):
        self.name = name
        self.measured_distance = distance

    def set_displacement(self, displacement):
        self.displacement = displacement

    def set_status(self, status):
        self.status = status


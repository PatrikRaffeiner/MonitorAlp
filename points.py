import numpy as np

# simple class for controlPoint handling
class DronePoint: 
    def __init__(self, name, x, y, z):
        self.name = name                                    # name of point (string)
        self.x = float(x)                                   # x position (float)
        self.y = float(y)                                   # y position (float)
        self.z = float(z)                                   # z position (float)
        self.pos = np.array([self.x, self.y, self.z])       # position array xyz (array floats)
        self.displacement = None                            # array of calculated displacements w.r.t. initial measurement (array floats)
        self.distance_from_origin = None                    # length between target/drone point and origin (float)
        self.status = None                                  # status of acceptable displacement (string)
        self.approx_mean_error = None                       # approximate mean error of target/drone point position (float)


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

    
    def set_approx_mean_error(self, err):
        self.approx_mean_error = err





class ManualPoint:
    def __init__(self, name, distance):
        self.name = name
        self.measured_distance = distance   # in meters
        self.displacement = None            # array of calculated displacements w.r.t. initial measurement (array floats)
        self.status = None                  # status of acceptable displacement (string)


    def set_displacement(self, displacement):
        self.displacement = displacement    # in meters


    def set_status(self, status):
        self.status = status


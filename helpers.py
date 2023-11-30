import numpy as np
import csv 




# simple class for controlPoint handling
class ControlPoint: 
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
    

    def set_displacement(self, dx, dy, dz):
        self.displacement = [dx, dy, dz]



def set_axes_equal(ax):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    """

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])



# function to read csv file and return list of control points
def read_csv(controlPoint_path):
    points = []
    # read out exported point-coordinates
    with open(controlPoint_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            #print(line)
            name = line[0]
            x = line[1]
            y = line[2]
            z = line[3]
            #print(f"name: {name}, x: {x}, y: {y}, z: {z}")
            points.append(ControlPoint(name, x, y, z))
    
    return points




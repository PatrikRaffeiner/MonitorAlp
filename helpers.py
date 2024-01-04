import csv
from abc import ABC, abstractmethod

from controlPoint import *


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



class TextReadOut(ABC):
    # abstract class to serve as super class for language handling 
    def __init__(self):
        self.dictionary = { # ID : [EN  ,  DE]
                            1 : ["Hello", "Hallo"],
                            2 : ["World", "Welt"], 
                            "hm_txt_title" : ["Monitoring Tool for Alpine Infrastructure", "Monitoring Tool für Alpine Infrastruktur"], 
                            "hm_btn_start" : ["Start New Project", "Neues Projekt Starten"],
                            "hm_btn_load" : ["Load Project", "Projekt Laden"], 
                            "setup_tip_exe" : ["Please find the path to your Reality Capture installation/execution (RealityCapture.exe)", "Bitte den Pfad zur Reality Capture Ausführungsdatei (RealityCapture.exe) angeben"],
                            "setup_txt_name" : ["Project Name / Location Name", "Projektname / Klettersteigname"],
                            "" : ["", ""],
                            "" : ["", ""],
                            "" : ["", ""],
                            "" : ["", ""],
                            "" : ["", ""],
                            "" : ["", ""],
                            "" : ["", ""],
                            "" : ["", ""],}


    @abstractmethod
    def gettext(self, textID):
        pass


class enTextReadOut(TextReadOut):
    # child class for english language readout
    def gettext(self, textID):
        return self.dictionary[textID][0]


class deTextReadOut(TextReadOut):
    # child class for german language readout
    def gettext(self, textID):
        return self.dictionary[textID][1]


# global variable/class
readout = enTextReadOut()
print(f"initial readout {readout}")
print("in helpers")


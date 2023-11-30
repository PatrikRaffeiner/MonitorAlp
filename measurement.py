import os.path
from datetime import date, datetime
import pickle
import matplotlib.pyplot as plt
import copy

# local imports
from helpers import *



class Measurement():
    def __init__(self, location, ref_marker_names, target_marker_names, 
                 ref_dist, img_path, project):
        
        self.date = date.today().strftime("%d/%m/%Y")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.location = location
        self.ref_marker_names = ref_marker_names
        self.target_marker_names = target_marker_names
        self.ref_distance = ref_dist
        self.img_path = img_path


        # reference system names
        self.ref_origin_name = self.ref_marker_names[0]
        self.ref_X_name = self.ref_marker_names[1]
        self.ref_Z_name =  self.ref_marker_names[2]
        #self.coordinates  = None

        self.create_name(project)
        self.create_dir(project)



    def create_name(self, project):
        temp_date = self.date.replace("/", "-")
        new_name = self.location + "_" + temp_date 
        self.name = new_name 

        # check for same measurement name, happens when measurement is performed on the same day
        for old_measurement in project.measurement_list:
            if new_name == old_measurement.name:

                # get last element of list
                last_measurement = project.measurement_list[-1]
                braket_pos = last_measurement.name.find("(")

                # no braket in last measurement name
                if braket_pos == -1:
                    self.name = new_name + "(2)"
                    break

                # add +1 to existing version
                else:
                    version = int(last_measurement.name[braket_pos+1])
                    self.name = self.name + "(" + str(version + 1) + ")"
                    break

                


    def create_dir(self, project):
        self.dir = os.path.join(project.dir, self.name)
        os.mkdir(self.dir)




    def transform_points(self):
        # load point coordinates from exported csv file
        raw_points = read_csv(self.controlPoint_path)

        
        # shift all points to reference origin
        self.points, self.origin = self.shift_points(raw_points, self.ref_origin_name)
        E, E_inv = self.createRotationMatrix(self.points, self.ref_X_name, self.ref_Z_name)

        # rotate points to transform into world coordinate system 
        for pt in self.points: 
            pt.set_pos(np.dot(E, pt.get_pos()))


    

    def sort_points(self):
        self.ref_points = []
        self.target_points = []


        for ref_marker_name in self.ref_marker_names:
            pnt = next((point for point in self.points if point.name == ref_marker_name))
            self.ref_points.append(pnt)

        
        for target_marker_name in self.target_marker_names:
            pnt = next((point for point in self.points if point.name == target_marker_name))
            self.target_points.append(pnt)

    

    # function to shift control points of arbitrary coordinate system to origin
    def shift_points(self, raw_points, origin_name):
        zeroed_points = copy.deepcopy(raw_points)

        # search point name of origin point 
        origin_points = [point for point in zeroed_points if point.name == origin_name]
        
        originPoint = origin_points[0]

        temp_x = originPoint.x
        temp_y = originPoint.y
        temp_z = originPoint.z

        # apply offset to shift reference point0 to origin (0,0,0)
        for pt in zeroed_points:
            pt.x -= temp_x
            pt.y -= temp_y
            pt.z -= temp_z
        
        return zeroed_points, originPoint
    



    def createRotationMatrix(self, zero_points, horizontalPoint_name, verticalPoint_name):
        # search point name of origin point 
        verticalPoint = [point for point in zero_points if point.name == horizontalPoint_name] 
        verticalPoint = verticalPoint[0]
        horizontalPoint = [point for point in zero_points if point.name == verticalPoint_name] 
        horizontalPoint = horizontalPoint[0]

        # create coordinate system at (reference) origin
        e1 = np.array([verticalPoint.x, verticalPoint.y, verticalPoint.z])

        e2 = np.cross([verticalPoint.x, verticalPoint.y, verticalPoint.z],
                    [horizontalPoint.x, horizontalPoint.y, horizontalPoint.z])
        e2 = e2

        e3 = np.cross(e1,e2)

        # normalize to obtain base unit vectors
        e1 = e1 / np.linalg.norm(e1)
        e2 = e2 / np.linalg.norm(e2)
        e3 = e3 / np.linalg.norm(e3)

        # check orthogonality
        # print(np.dot(e1,e2))
        # print(np.dot(e2,e3))
        # print(np.dot(e1,e3))

        # Transformation matrix =^ base unit vectors
        E = np.array([e1,e2,e3])
        E_inv = np.linalg.inv(E)

        return E, E_inv
    



    def visualize_points(self):
        # axis length for vizualization
        ax_len = 0.2
        
        # coordinate system points
        cp1 = [ax_len, 0, 0]
        cp2 = [0, -ax_len, 0]
        cp3 = [0, 0, -ax_len]

        # initial point coordinates
        xi_i = []
        yi_i = []
        zi_i = []


        for point in self.points: 
            xi_i.append(point.x)
            yi_i.append(point.y)
            zi_i.append(point.z)
            #print(f"name: {point.name}, x: {point.x}, y: {point.y}, z: {point.z}")

        # create figure
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # plot coordinate system
        ax.plot([self.origin.x,ax_len], [self.origin.y,0], [self.origin.z,0], "red")
        ax.plot([self.origin.x,0], [self.origin.y,-ax_len], [self.origin.z,0], "green")
        ax.plot([self.origin.x,0], [self.origin.y,0], [self.origin.z,-ax_len], "blue")

        # plot coordinate points
        ax.scatter(cp1[0], cp1[1], cp1[2], c="red")
        ax.scatter(cp2[0], cp2[1], cp2[2], c="green")
        ax.scatter(cp3[0], cp3[1], cp3[2], c="blue")


        # plot initial control points
        ax.scatter(xi_i, yi_i, zi_i, c="red", marker='o')

        
        # equal axis for better visual representarion
        set_axes_equal(ax)

        plt.show()
        



    def save(self):
        try:
            save_dir = self.dir + "/" + self.name + ".pkl"
            print(save_dir)
            with open(save_dir, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)




    


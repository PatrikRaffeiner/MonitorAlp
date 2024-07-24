import os.path
from datetime import date, datetime
import pickle
import matplotlib.pyplot as plt
import copy
import shutil
import numpy as np
import PySimpleGUI as sg
from abc import ABC, abstractmethod         # ABC = abstract class


# local imports
from helpers import read_points_from_csv, set_axes_equal
from gui import getText
from uiHandler import UIhandler
from points import ManualPoint

class Measurement(ABC):
    @abstractmethod
    def __init__(self, location, ref_marker_names, 
                 target_marker_names, project, temperature, 
                 weather_conditions, acquisition_date, 
                 acquisition_time, comment):
        
        self.evaluation_date = date.today().strftime("%d-%m-%Y")
        self.evaluation_time = datetime.now().strftime("%H:%M")
        self.location = location
        self.ref_marker_names = ref_marker_names
        self.comment = comment


        # reference system names
        self.ref_origin_name = self.ref_marker_names[0]
        self.ref_X_name = self.ref_marker_names[1]
        self.ref_Z_name =  self.ref_marker_names[2]

        self.target_marker_names = target_marker_names

        self.target_points = []

        self.acquisition_date = acquisition_date
        self.acquisition_time = acquisition_time

        self.create_name(project)
        self.create_dir(project)

        self.UiHandler = UIhandler()

        self.limit = project.limit
        self.temperature = temperature
        self.weather_conditions = weather_conditions


                

    @abstractmethod
    def create_dir(self, project):
        self.dir = project.dir + "/" + self.name




    @abstractmethod
    def create_name(self, project):
        temp_date = self.acquisition_date.replace("/", "-")
        new_name = self.location + "_" + temp_date 
        self.name = new_name 



    
    def make_version(self, measurement_list):

        new_name = self.name
        
        # check for same measurement name, happens when measurement is performed on the same day
        for old_measurement in measurement_list:
            
            if new_name == old_measurement.name:

                # get last element of list
                last_measurement = measurement_list[-1]
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




    def save(self):
        try:
            save_dir = self.dir + "/" + self.name + ".pkl"
            with open(save_dir, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during saving measurement, pickling object (Possibly unsupported):", ex)
            pass

    


    def delete_directory(self):
        shutil.rmtree(self.dir)




    def set_status(self, status):
        self.status = status




    def check_limits(self):
        # TODO: set displacement limit 
        shift_limit = self.limit     # meters


        # TODO: check any target over limit
        for target in self.target_points:

            # check norm displacement
            if isinstance(self, ManualMeasurement):
                abs_displacement = abs(target.displacement)

            else: 
                abs_displacement = abs(target.displacement[3])

            if abs_displacement > (shift_limit):
                #subseq_measurement.set_status("Achtung")
                target.set_status("Achtung")
            
            elif abs_displacement > (0.5 * shift_limit):
                #subseq_measurement.set_status("Warnung")
                target.set_status("Warnung")

            elif abs_displacement < (0.5 * shift_limit):
                #subseq_measurement.set_status("OK")
                target.set_status("OK")            



        # set default status of measurement to "OK"
        self.set_status("OK")

        # reset if any target point status is not OK (Achtung overwrites Warnung)
        if any(target_point.status == "Warnung" for target_point in self.target_points):
            self.set_status("Warnung")

        if any(target_point.status == "Achtung" for target_point in self.target_points):
            self.set_status("Achtung")   





class DroneMeasurement(Measurement):
    # extending the constructor of the parent class (Measurement)
    def __init__(self, location, ref_marker_names, target_marker_names,
                 project, temperature, weather_conditions, 
                 acquisition_date, acquisition_time, comment,
                 ref_dist, orig_img_path, accuracy_indication_names):
        
        super().__init__(location, ref_marker_names, target_marker_names, 
                         project, temperature, weather_conditions, 
                         acquisition_date, acquisition_time, comment)
        self.ref_distance = ref_dist    # in meters
        self.copy_imgs(orig_img_path)

        self.ref_points = []
        self.accuracy_indication_points = []
        self.accuracy_indication_names = accuracy_indication_names
                
        self.num_of_imgs = self.get_number_of_images()




    def create_dir(self, project):
        super().create_dir(project)
        os.mkdir(self.dir) 




    def create_name(self, project):
        super().create_name(project)
        measurement_list = project.drone_measurement_list

        self.make_version(measurement_list)




    def copy_imgs(self, orig_path):
        self.img_path = self.dir + "/imgs"
        shutil.copytree(orig_path, self.img_path)




    def compare_points(self):    
        # load point coordinates from exported csv file
        try: 
            RC_points = read_points_from_csv(self.controlPoint_path)
        except: 
            sg.popup_non_blocking(getText("hm_txt_warnRC"), 
                                   title=getText("warn_btn"), 
                                   background_color= "Red3")


        # names of the exported RealityCapture points
        RC_points = [point.name for point in RC_points]

        # list of points missing in the exported RealityCapture points
        missing_refs = []
        missing_targets =[]

        for ref_point in self.ref_marker_names: 
            if ref_point not in RC_points:
                missing_refs.append(ref_point)

        
        for target_point in self.target_marker_names: 
            if target_point not in RC_points:
                missing_targets.append(target_point)


        if missing_refs or missing_targets:

            uiHandler = UIhandler()
            uiHandler.show_missing_markers(missing_refs, missing_targets)
            



    def transform_points(self):
        # load point coordinates from exported csv file
        raw_points = read_points_from_csv(self.controlPoint_path)

        
        # shift all points to reference origin
        self.points, self.origin = self.shift_points(raw_points, self.ref_origin_name)
        E, E_inv = self.createRotationMatrix(self.points, self.ref_X_name, self.ref_Z_name)

        # rotate points to transform into world coordinate system 
        for pt in self.points: 
            pt.set_pos(np.dot(E, pt.get_pos()))


    

    def sort_points(self):
        # sort reference points by checking the marker name (known reference marker names) 
        for ref_marker_name in self.ref_marker_names:
            pnt = next((point for point in self.points if point.name == ref_marker_name))
            self.ref_points.append(pnt)

        # sort target points by checking the marker name (known target marker names)
        for target_marker_name in self.target_marker_names:
            pnt = next((point for point in self.points if point.name == target_marker_name))
            self.target_points.append(pnt)

        # sort accuracy indicator points by checking the marker name (known accuracy indicator marker names)
        for indicator_marker_name in self.accuracy_indication_names:
            pnt = next((point for point in self.points if point.name == indicator_marker_name))
            self.accuracy_indication_points.append(pnt)
    

    

    def shift_points(self, raw_points, origin_name):
        # function to shift control points of arbitrary coordinate system to origin
        zeroed_points = copy.deepcopy(raw_points)

        # search point name of origin point 
        origin_points = [point for point in zeroed_points if point.name == origin_name]
        
        originPoint = origin_points[0]

        shift_x = originPoint.x
        shift_y = originPoint.y
        shift_z = originPoint.z

        # apply offset to shift reference point0 to origin (0,0,0)
        for pt in zeroed_points:
            pt.x -= shift_x
            pt.y -= shift_y
            pt.z -= shift_z
        
        return zeroed_points, originPoint
    



    def createRotationMatrix(self, zero_points, horizontalPoint_name, verticalPoint_name):
        # search point name of origin point 
        horizontalPoint = [point for point in zero_points if point.name == horizontalPoint_name] 
        horizontalPoint = horizontalPoint[0]
        verticalPoint = [point for point in zero_points if point.name == verticalPoint_name] 
        verticalPoint = verticalPoint[0]

        # create coordinate system at (reference) origin
        e1 = np.array([horizontalPoint.x, horizontalPoint.y, horizontalPoint.z])

        e2 = np.cross([verticalPoint.x, verticalPoint.y, verticalPoint.z],
                    [horizontalPoint.x, horizontalPoint.y, horizontalPoint.z])

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
        # axis length for visualization
        ax_len = 120
        
        # coordinate system points
        cp1 = [ax_len, 0, 0]
        cp2 = [0, ax_len, 0]
        cp3 = [0, 0, ax_len]

        # initial point coordinates
        xi_i = []
        yi_i = []
        zi_i = []


        for point in self.points: 
            xi_i.append(point.x * 1000)  # in millimeter
            yi_i.append(point.y * 1000)  # in millimeter
            zi_i.append(point.z * 1000)  # in millimeter
            #print(f"name: {point.name}, x: {point.x}, y: {point.y}, z: {point.z}")

        # create figure
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # Set the axis labels
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('y (mm)')
        ax.set_zlabel('z (mm)')

        # plot coordinate system
        ax.plot([self.origin.x,ax_len], [self.origin.y,0], [self.origin.z,0], "red")
        ax.plot([self.origin.x,0], [self.origin.y,ax_len], [self.origin.z,0], "green")
        ax.plot([self.origin.x,0], [self.origin.y,0], [self.origin.z, ax_len], "blue")

        # plot coordinate points
        ax.scatter(cp1[0], cp1[1], cp1[2], c="red")
        ax.scatter(cp2[0], cp2[1], cp2[2], c="green")
        ax.scatter(cp3[0], cp3[1], cp3[2], c="blue")


        # plot initial control points
        ax.scatter(xi_i, yi_i, zi_i, c="red", marker='o')

        # labeling and orientation of points 
        target_labels = [self.points[i].name for i in range(len(xi_i))]
        zdirs = [None, None, None]

        # add labels to init points
        for x, y, z, label, zdir in zip(xi_i, yi_i, zi_i, target_labels, zdirs):
            ax.text(x, y, z-10, label, zdir, color="brown")

        # add labels to coordinate points
        ax.text(self.origin.x, self.origin.y, self.origin.z-10, self.ref_points[0].name, zdir, color="black")
        ax.text(self.ref_points[1].x*1000, self.ref_points[1].y*1000, self.ref_points[1].z*1000-10, "x, "+ self.ref_points[1].name, zdir, color="red")
        ax.text(cp2[0], cp2[1], cp2[2]-10, "y", zdir, color="green")
        ax.text(self.ref_points[2].x*1000, self.ref_points[2].y*1000, self.ref_points[2].z*1000-10, "z, "+ self.ref_points[2].name, zdir, color="blue")
        
        # equal axis for better visual representarion
        set_axes_equal(ax)

        # Rotate view
        ax.view_init(-170,-100,0)

        plt.show()
        



    def show_measurement_info(self, overview_window):
        
        content =  [getText("meas_txt_typeD")[0], getText("meas_txt_typeD")[1], "",     # Type
                    getText("meas_txt_loc"), self.location, "",                         # Location  
                    getText("meas_txt_aquD&T"), self.acquisition_date, self.acquisition_time, "",    # Aquisition Time & Date
                    getText("meas_txt_evalD&T"), self.evaluation_date, self.evaluation_time, "",   # Evaluation Time & Date
                    getText("meas_txt_weather"), getText("meas_txt_" + self.weather_conditions), "",
                    getText("meas_txt_temp"), str(self.temperature)+"°C", "",
                    getText("meas_txt_refM"),                                       
                    self.ref_marker_names[0],
                    self.ref_marker_names[1],
                    self.ref_marker_names[2], "",
                    getText("meas_txt_trgtM")]                                    # Target marker                                      

        # adding target names to output
        for target_name in self.target_marker_names:
            content.append(target_name)

        # adding comments
        content.append("")
        content.append(getText("meas_txt_comment"))

        for line in self.comment.splitlines():
            content.append(line)


        overview_window["-OUTPUT-"].update(content)




    def get_number_of_images(self):
        # get the size of the image directory
        img_list = os.listdir(self.img_path)

        img_count = len(img_list)

        return img_count





class ManualMeasurement(Measurement):
    # extending the constructor of the parent class (Measurement)
    def __init__(self, location, ref_marker_names, target_marker_names, 
                 project, temperature, weather_conditions,
                  acquisition_date, acquisition_time, comment, 
                  target_distances):
        super().__init__(location, ref_marker_names, target_marker_names, 
                         project, temperature, weather_conditions,
                         acquisition_date, acquisition_time, comment)

        #self.distance_dict = target_distances
        for name, distance in zip(target_marker_names, target_distances):
            point = ManualPoint(name, distance) # magnitudes in meters
            self.target_points.append(point)



    
    def create_dir(self, project):
        # returning the original method from parent class
        super().create_dir(project)


        # removes last character (#) from name/dir
        # measurement dir is the project dir + measurement name 
        # the manual measurement name is labelled with a # at the end of the name
        self.dir = self.dir[:-1]

        return self.dir
        



    def create_name(self, project):
        super().create_name(project)

        self.name = self.name + "#"
        measurement_list = project.manual_measurement_list

        self.make_version(measurement_list)




    def show_measurement_info(self, overview_window):
        
        content =  [getText("meas_txt_typeM")[0], getText("meas_txt_typeM")[1], "",     # Type
                    getText("meas_txt_loc"), self.location, "",                         # Location  
                    getText("meas_txt_aquD&T"), self.acquisition_date, self.acquisition_time, "",    # Aquisition Time & Date
                    getText("meas_txt_evalD&T"), self.evaluation_date, self.evaluation_time, "",   # Evaluation Time & Date
                    getText("meas_txt_weather"), getText("meas_txt_" + self.weather_conditions), "",
                    getText("meas_txt_temp"), str(self.temperature)+"°C", "",
                    getText("meas_txt_trgtM")]                                      # Target marker                                      

        # adding target names to output
        for target in self.target_points:
            content.append(target.name)

        # adding comments
        content.append("")
        content.append(getText("meas_txt_comment"))

        for line in self.comment.splitlines():
            content.append(line)

        overview_window["-OUTPUT-"].update(content)




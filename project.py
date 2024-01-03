import subprocess
from adjustText import adjust_text

# local imports 
from measurement import *
from uiHandler import *

        
class Project():
    def __init__(self):
        self.Gui = GUI()
        self.UiHandler = UIhandler()
        self.measurement_list = []
        self.target_list = self.TargetList()


    # function to initialize project variables via user input:
    # location, name, RealityCapture execution dir, 
    # availability of permanent licence 
    def setup(self):

        # creates and returns project setup window
        project_setup_window = self.Gui.make_project_setup_win()

        # set project members from UI
        self.location, self.RC_path, self.permanent_licence_active, self.name = self.UiHandler.handle_project_setup(project_setup_window)



    def create_measurement(self, init_status):

        # check for additional or initial measurement
        if init_status:
            print("init measurement")
            measurement_setup_window = self.Gui.make_init_measurement_setup_win()
            imgs_dir, self.dir = self.UiHandler.get_img_and_pjct_dir(measurement_setup_window, self.Gui)

            marker_input_window = self.Gui.make_marker_input_window(self.target_list)
            reference_list, target_list, ref_dist =  self.UiHandler.get_marker_names(self.Gui, marker_input_window, self.target_list)
            

        else: # additional measurement
            print("additional measurement")
            measurement_setup_window = self.Gui.make_measurement_setup_win()
            imgs_dir = self.UiHandler.get_img_dir(measurement_setup_window, self.Gui)

            reference_list = self.measurement_list[0].ref_marker_names
            target_list = self.measurement_list[0].target_marker_names
            ref_dist = self.measurement_list[0].ref_distance
        
        print(ref_dist)


        # TODO: differentiate between licence path and pin (maybe if pin.type == integer, achtung none)
        if self.permanent_licence_active == False:

            licence_browse_window = self.Gui.make_licence_browse_win()
            licence_pin = self.UiHandler.get_licence_pin(licence_browse_window)


        new_measurement = Measurement(self.location, reference_list, target_list,
                                       ref_dist, imgs_dir, self)
        
        return new_measurement


         

    def RC_registration_and_save_points(self, measurement):
        # path to save control points (measurement points)
        measurement.controlPoint_path = measurement.dir + "/controlPoints.csv"
        print(measurement.controlPoint_path)

        # definition of reference (marker) system
        origin = measurement.ref_origin_name
        refMarkerX = measurement.ref_X_name
        refMarkerZ =  measurement.ref_Z_name


        # crate path and name to save RC project
        save_path = measurement.dir + "/" + measurement.name + ".rcproj"


        # run RealityCapture, detect markers, define reference distance, export 3D-point-cooridnates 
        result = subprocess.run(
            [self.RC_path, 
            "-addFolder", measurement.img_path, 
            "-align", 
            "-detectMarkers", 
            "-defineDistance", origin, refMarkerX, measurement.ref_distance, 
            "-defineDistance", origin, refMarkerZ, measurement.ref_distance,
            "-update",
            "-exportGroundControlPoints", measurement.controlPoint_path,
            "-save", save_path,
            "-quit"])




    def add_to_measurement_list(self, m):
        self.measurement_list.append(m)




    def remove_from_measurement_list(self, m):
        self.measurement_list.remove(m)




    def visualize_points(self, init_points, ref_points, current_points = None):
        # get coordinate system origin
        origin = ref_points[0]
        
        # axis length for vizualization
        ax_len = 0.2
        
        # coordinate system points
        cp1 = [ax_len, 0, 0]
        cp2 = [0, -ax_len, 0]
        cp3 = [0, 0, -ax_len]

        # initial point coordinates
        x_i = []
        y_i = []
        z_i = []


        for point in init_points: 
            x_i.append(point.x)
            y_i.append(point.y)
            z_i.append(point.z)
            #print(f"name: {point.name}, x: {point.x}, y: {point.y}, z: {point.z}")

        # create figure 
        ax = plt.figure().add_subplot(projection='3d')

        # plot coordinate system
        ax.plot([origin.x,ax_len], [origin.y,0], [origin.z,0], "red")
        ax.plot([origin.x,0], [origin.y,-ax_len], [origin.z,0], "green")
        ax.plot([origin.x,0], [origin.y,0], [origin.z,-ax_len], "blue")

        # plot coordinate points
        ax.scatter(0, 0, 0, c="black")
        ax.scatter(cp1[0], cp1[1], cp1[2], c="red")
        ax.scatter(cp2[0], cp2[1], cp2[2], c="green")
        ax.scatter(cp3[0], cp3[1], cp3[2], c="blue")

        # plot initial points
        init_scatter = ax.scatter(x_i, y_i, z_i, c="brown", marker='o', label="initial measurement")

        # labeling and orientation of points 
        target_labels = [init_points[i].name for i in range(len(x_i))]
        zdirs = [None, None, None]

        # add labels to init points
        for x, y, z, label, zdir in zip(x_i, y_i, z_i, target_labels, zdirs):
            ax.text(x, y, z+0.01, label, zdir, color="brown")

        # add labels to coordinate points
        ax.text(origin.x, origin.y, origin.z+0.01, ref_points[0].name, zdir, color="black")
        ax.text(cp1[0], cp1[1], cp1[2]+0.01, "x, "+ref_points[1].name, zdir, color="red")
        ax.text(cp2[0], cp2[1], cp2[2]+0.01, "y", zdir, color="green")
        ax.text(cp3[0], cp3[1], cp3[2]+0.01, "z, "+ref_points[2].name, zdir, color="blue")



        if current_points != None:
            # current point coordinates
            x_c = []
            y_c = []
            z_c = []

            for point in current_points: 
                x_c.append(point.x)
                y_c.append(point.y)
                z_c.append(point.z)

            # plot current points
            current_scatter = ax.scatter(x_c, y_c, z_c, c = "orange", marker="o", label="current measurement")

            # add labels to current points
            for x, y, z, label, zdir in zip(x_c, y_c, z_c, target_labels, zdirs):
                ax.text(x, y, z-0.02, label, zdir, color="orange")
        

        # add legend of initial and current points via labeled scatter plots
        ax.legend()
        
        # equal axis for better visual representarion
        set_axes_equal(ax)

        plt.show()




    def save(self):
        try:
            save_dir = self.dir + "/" + self.name + ".pkl"
            with open(save_dir, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)




    def overview(self, project_list):
        measurement_names = self.get_measurement_names()
        overview_window, select_lst = self.Gui.make_project_overview_window(measurement_names, self)

        self.UiHandler.handle_measurement_overview(overview_window, select_lst, self, project_list)




    def calc_displacement(self, subseq_measurement):
        init_measurement = self.measurement_list[0]

        init_measurement.sort_points()
        subseq_measurement.sort_points()

        init_targets = init_measurement.target_points
        subseq_targets = subseq_measurement.target_points


        for init_target, subseq_target in zip(init_targets, subseq_targets):
            dx = subseq_target.x - init_target.x
            dy = subseq_target.y - init_target.y
            dz = subseq_target.z - init_target.z

            subseq_target.set_displacement(dx, dy, dz)
            
        self.calc_distance_to_origin(subseq_measurement)

        self.Gui.show_displacement(init_targets, subseq_targets)




    def calc_distance_to_origin(self, subseq_measurement):
        # calculate the absolute distance between every target and the origin
        origin = self.measurement_list[0].ref_points[0]
        subseq_targets = subseq_measurement.target_points

        for target in subseq_targets:
            dist = np.linalg.norm(target.get_pos())
            target.set_distance_from_origin(dist)


    

    def visualize_displacement(self, measurement):

        init_measurement = self.measurement_list[0]
        ref_points = self.measurement_list[0].ref_points

        self.visualize_points(init_measurement.target_points, ref_points, measurement.target_points)

        

        
    def get_measurement_names(self):
        measurement_names = []
        for measurement in self.measurement_list:
            measurement_names.append(measurement.name)

            
        return measurement_names
            




    class TargetList(list):
        def __init__(self):
            char = "A"
            self.init_char = ord(char [0])
            
            # initialize target list with one element (flag+label)
            self.flags = [None]
            self.labels = [None]

        
        def make_current_marker_text(self, target_num):
            char = self.init_char + target_num
            text = "Target marker " + chr(char)

            return text    


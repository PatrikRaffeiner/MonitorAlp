import subprocess
from adjustText import adjust_text
import xlsxwriter
import math

# local imports 
from measurement import *
from uiHandler import *

        
class Project():
    def __init__(self):
        self.Gui = GUI()
        self.UiHandler = UIhandler()
        self.all_measurement_list = []
        self.drone_measurement_list = []
        self.manual_measurement_list = []
        self.target_list = self.TargetList()




    def setup(self, master_obj):

        # creates and returns project setup window
        project_setup_window = self.Gui.make_project_setup_win(master_obj.RC_dir)

        # set project members from UI
        self.location, RC_path, self.permanent_licence_active, self.name = self.UiHandler.handle_project_setup(project_setup_window, master_obj)
        master_obj.set_RC_dir(RC_path)




    def create_drone_measurement(self, init_status):


        # check for additional or initial measurement
        if init_status:
            measurement_setup_window = self.Gui.make_init_measurement_setup_win()
            imgs_dir, self.dir = self.UiHandler.get_img_and_pjct_dir(measurement_setup_window, self.Gui, self.name)

            '''uncomment for agile version'''
            # marker_input_window = self.Gui.make_marker_input_window(self.target_list)
            # self.reference_list, target_list, ref_dist =  self.UiHandler.get_marker_names(self.Gui, marker_input_window, self.target_list)
            
            '''comment out for agile version'''
            self.reference_list = ["1x12:01a", "1x12:01b", "1x12:01c"]
            target_list = ["1x12:011", "1x12:015", "1x12:026"]
            self.target_list.labels = target_list
            ref_dist = "0.1200"

            self.accuracy_indication_list = ["1x12:01f", "1x12:01d"]
            self.accuracy_indication_true_length = 0.084853    # m

        else: # additional measurement
            measurement_setup_window = self.Gui.make_measurement_setup_win()
            imgs_dir = self.UiHandler.get_img_dir(measurement_setup_window, self.Gui)


            reference_list = self.drone_measurement_list[0].ref_marker_names
            target_list = self.drone_measurement_list[0].target_marker_names
            ref_dist = self.drone_measurement_list[0].ref_distance
        


        # TODO: differentiate between licence path and pin (maybe if pin.type == integer, achtung none)
        if self.permanent_licence_active == False:

            licence_browse_window = self.Gui.make_licence_browse_win()
            licence_pin = self.UiHandler.get_licence_pin(licence_browse_window)



        pop_up = GUI.popup_window("pjct_pop_wait")
        new_measurement = None

        while new_measurement == None:
            # wrapper for parallel 
            pop_up.perform_long_operation(lambda: DroneMeasurement(self.location,
                                                                   self.reference_list,
                                                                   target_list,
                                                                   self.accuracy_indication_list,
                                                                   self, 
                                                                   ref_dist, 
                                                                   imgs_dir),
                                                                   '-MEASUREMENT_COMPLETED-')
            
            event, values = pop_up.read()

            if event == '-MEASUREMENT_COMPLETED-':
                new_measurement = values[0]
                pop_up.close()
                return new_measurement

                


    def create_manual_measurement(self):
        
        manual_measurement_window = self.Gui.make_manual_measurement_input_window(self)
        manual_measurement_dict = self.UiHandler.get_manual_measurement_distances(manual_measurement_window, self)
        
        new_manual_measurement = ManualMeasurement(
                                    self.location,            
                                    self.reference_list,
                                    [*manual_measurement_dict.keys()],
                                    self, 
                                    manual_measurement_dict.values())
        
        manual_measurement_window.close()
        
        return new_manual_measurement




    def RC_registration_and_export_points(self, measurement, RC_dir):
        # path to save control points (measurement points)
        measurement.controlPoint_path = measurement.dir + "/controlPoints.csv"

        # definition of reference (marker) system
        origin = measurement.ref_origin_name
        refMarkerX = measurement.ref_X_name
        refMarkerZ =  measurement.ref_Z_name


        # crate path and name to save RC project
        save_path = measurement.dir + "/" + measurement.name + ".rcproj"


        # run RealityCapture, detect markers, define reference distance, export 3D-point-cooridnates         
        result = subprocess.run(
            [RC_dir, 
            "-addFolder", measurement.img_path, 
            "-detectMarkers", 
            "-defineDistance", origin, refMarkerX, measurement.ref_distance, 
            "-defineDistance", origin, refMarkerZ, measurement.ref_distance,
            "-align",
            "-exportGroundControlPoints", measurement.controlPoint_path,
            "-save", save_path,
            "-quit"])



    # maybe delete
    def get_measurement_lists(self):

        self.manual_measurement_list = []
        self.drone_measurement_list = []

        for measurement in self.all_measurement_list: 
            if measurement.name.__contains__("#"):
                self.manual_measurement_list.append(measurement)

            else: 
                self.drone_measurement_list.append(measurement)

        return self.drone_measurement_list, self.manual_measurement_list





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
            print("Error during pickling project object (Possibly unsupported):", ex)




    def overview(self, master_obj):
        overview_window, drone_lst, manual_lst = self.Gui.make_project_overview_window(self.drone_measurement_list, self.manual_measurement_list, self)

        self.UiHandler.handle_measurement_overview(overview_window, drone_lst, manual_lst, self, master_obj)




    def calc_displacement(self, subseq_measurement):

        if isinstance(subseq_measurement, DroneMeasurement): 
            init_measurement = self.drone_measurement_list[0]     

            init_targets = init_measurement.target_points
            subseq_targets = subseq_measurement.target_points


            for init_target, subseq_target in zip(init_targets, subseq_targets):
                dx = subseq_target.x - init_target.x
                dy = subseq_target.y - init_target.y
                dz = subseq_target.z - init_target.z

                dabs = np.linalg.norm([dx, dy, dz])

                subseq_target.set_displacement(dx, dy, dz, dabs)

        else:   # is Manual measurement
            init_measurement = self.manual_measurement_list[0]    

            for init_point, subseq_point in zip(init_measurement.target_points, subseq_measurement.target_points):
               # convert strings to float 
                init = float(init_point.measured_distance)
                subseq = float(subseq_point.measured_distance)


                displacement = init - subseq
                #displacement = str(displacement)
                subseq_point.set_displacement(displacement)

        



    def calc_distance_to_origin(self, subseq_measurement):
        # calculate the absolute distance between every target and the origin
        subseq_targets = subseq_measurement.target_points

        for target in subseq_targets:
            dist = np.linalg.norm(target.get_pos())
            target.set_distance_from_origin(dist)

    


    def calc_accuracy_indicator(self, measurement):
        accuracy_indication_points = measurement.accuracy_indication_points
        
        calculated_accuracy_indication_length = math.dist(accuracy_indication_points[0].get_pos(),
                                                          accuracy_indication_points[1].get_pos())

        measurement.accuracy_score = abs(calculated_accuracy_indication_length-self.accuracy_indication_true_length)
        




    def plot_displacement(self, subseq_measurement):
        init_measurement = self.drone_measurement_list[0]

        subseq_targets = subseq_measurement.target_points

        self.Gui.show_displacement(subseq_targets)




    def visualize_displacement(self, measurement):

        init_measurement = self.drone_measurement_list[0]
        ref_points = self.drone_measurement_list[0].ref_points

        self.visualize_points(init_measurement.target_points, ref_points, measurement.target_points)




    def dump_xlsx_file(self):

        def get_displacement(point, coord):
            try: 
                return "{:.2f}".format(1000*point.displacement[coord])
            
            except Exception as ex:
                return "-"
        


        def make_manual_measurement_block(worksheet, measurement, align_center, align_center_rotate, block_end):
            # calculate the length and position of each measurement block 
            block_start = block_end + 2
            block_end = block_start + 5 + len(measurement.target_points)

            # merge vertical measurement title block
            merging_cells_m = "A" + str(block_start) + ":A" + str(block_end)
            worksheet.merge_range(merging_cells_m, measurement.name, align_center_rotate)

            # merging measured distance cells
            merging_cells_d = "C" + str(block_start) + ":F" + str(block_start)
            worksheet.merge_range(merging_cells_d, "this is a placehoder", align_center)


            # making column titles
            col_titles = ["Marker Name", "Gemessene Distanz zur Basisplatte (mm)"]
            
            for count, element in enumerate(col_titles):
                worksheet.write(block_start-1, 1+count, element, align_center)

            # make rows of target distances
            row_count = 0
            for target in  measurement.target_points:
                
                # merging measured distance cells
                merging_cells_k = "C" + str(block_start+row_count+1) + ":F" + str(block_start+row_count+1)
                worksheet.merge_range(merging_cells_k, "this is a placehoder", align_center)



                row = [target.name, 
                       target.measured_distance]
                
                for col_count, element in enumerate(row):
                    worksheet.write(block_start+row_count, 1+col_count, element, align_center)

                row_count += 1

            return block_end



        def make_drone_measurement_block(worksheet, measurement, align_center, align_center_rotate, block_end):
            # calculate the length and position of each measurement block 
            block_start = block_end + 2
            block_end = block_start + 5 + len(measurement.target_points)

            # merge vertical measurement title block
            merging_cells_m = "A" + str(block_start) + ":A" + str(block_end)
            worksheet.merge_range(merging_cells_m, measurement.name, align_center_rotate)

            # merging coordinate cells and displacement
            merging_cells_c = "C" + str(block_start) + ":E" + str(block_start)
            worksheet.merge_range(merging_cells_c, "Koordinaten (mm)", align_center)

            merging_cells_d = "G" + str(block_start) + ":J" + str(block_start)
            worksheet.merge_range(merging_cells_d, "Verschiebungen (mm)", align_center)

            # making column titles
            col_titles = ["Marker Name", "x", "y", "z", "Distanz zu Ursprung", "dx", "dy", "dz", "dabs"]
                
            for count, element in enumerate(col_titles):
                worksheet.write(block_start, 1+count, element, align_center)
                
            # make rows of reference points
            for row_count, point in enumerate(measurement.ref_points):
                dist_origin = np.linalg.norm(point.get_pos())
                row = [point.name, 
                        "{:.2f}".format(point.x*1000), # x-coord
                        "{:.2f}".format(point.y*1000), # y-coord
                        "{:.2f}".format(point.z*1000), # z-coord
                        "{:.2f}".format(dist_origin*1000),  # euclidian distance to origin
                        "-", "-", "-", "-"]                  # displacements 

                for col_count, element in enumerate(row):
                    worksheet.write(block_start+row_count+1, 1+col_count, element, align_center)

            # make rows of target points
            for row_count, point in enumerate(measurement.target_points):
                dist_origin = np.linalg.norm(point.get_pos())

                row = [point.name, 
                    "{:.2f}".format(point.x*1000), # x-coord
                    "{:.2f}".format(point.y*1000), # y-coord
                    "{:.2f}".format(point.z*1000), # z-coord
                    "{:.2f}".format(dist_origin*1000), # euclidian distance to origin
                    get_displacement(point, 0),
                    get_displacement(point, 1),
                    get_displacement(point, 2),
                    get_displacement(point, 3)]
                    

                for col_count, element in enumerate(row):
                    worksheet.write(block_start+row_count+4, 1+col_count, element, align_center)

            return block_end



        def make_xlsx_file(self, dump_dir):
            # Create a workbook and add a worksheet.
            workbook = xlsxwriter.Workbook(dump_dir)
            worksheet = workbook.add_worksheet()

            big = workbook.add_format()
            big.set_font_size(30)

            # Write project title
            worksheet.write(0,1, self.name, big)

            # initial value to calculate first block start
            block_end = 2


            # set column width for readability
            worksheet.set_column_pixels(1, 1, 91)
            worksheet.set_column_pixels(5, 5, 130)

            for count, measurement in enumerate(self.all_measurement_list):
                # rotate text for merged columns
                align_center_rotate = workbook.add_format({"align" : "center"})
                align_center_rotate.set_rotation(90)
                align_center_rotate.set_align("vcenter")
                align_center = workbook.add_format({"align" : "center"})

                if isinstance(measurement, DroneMeasurement):
                    block_end = make_drone_measurement_block(worksheet, measurement, align_center, align_center_rotate, block_end)
                
                else: 
                    block_end = make_manual_measurement_block(worksheet, measurement, align_center, align_center_rotate, block_end)


                
            workbook.close()




        dump_dir = self.dir + "/" + self.name + ".xlsx"

        # checks if an existing file is opened/writeable
        if os.path.exists(dump_dir):
            while True:
                try: 
                    open(dump_dir, "a")
                    # continues when file is writable
                    break
                
                except Exception as ex:
                    # raises popup when file is not writable
                    retry_or_return = self.UiHandler.handle_open_file(ex, self.name + ".xlsx")

                    if retry_or_return == "Cancel":
                        # exit without writing file
                        return
                    else: 
                        # starts next iteration to try open file
                        continue
                
        make_xlsx_file(self, dump_dir)

            


    def dump_pdf(self, dump_dir):        
        from pdfGenerator import PdfGenerator

        new_pdf = PdfGenerator()
        doc = new_pdf.setup_doc(dump_dir, self.location)
        
        for measurement in self.all_measurement_list:

            if isinstance(measurement, DroneMeasurement):
                new_pdf.make_drone_measurement_table(measurement, doc)
                doc = new_pdf.insert_drone_measuremtnt(measurement, doc)

            else: # manual measurement
                new_pdf.make_manual_measurement_table(measurement, doc)
                doc = new_pdf.insert_manual_measuremtnt(measurement, doc)
                    
            


        # checks if an existing file is opened/writeable
        if os.path.exists(dump_dir):
            while True:
                try: 
                    open(dump_dir, "a")
                    # continues when file is writable
                    break
                
                except Exception as ex:
                    # raises popup when file is not writable
                    retry_or_return = self.UiHandler.handle_open_file(ex, self.name + ".pdf")

                    if retry_or_return == "Cancel":
                        # exit without writing file
                        return
                    else: 
                        # starts next iteration to try open file
                        continue
                
        new_pdf.dump(doc)

        return new_pdf




    def delete_directory(self):
        
        def try_to_delete(el):
            print("deleting.... " + el)
            try:
                shutil.rmtree(self.dir +"/"+ el)
                print("removed " + el)
            except Exception as ex:
                try:
                    os.remove(self.dir +"/"+ el)
                    print("removed " + el)
                except Exception as ex:
                    print("could not remove: " + el)
                    # do something here


        dir_list = os.listdir(self.dir)
        from_project = []
        not_from_project = []

        for element in dir_list:
            if element.startswith(self.name):
                from_project.append(element)
            else:
                not_from_project.append(element)
            
        warning_win = GUI.make_delete_warning(from_project, not_from_project)

        while True:
            event, values = warning_win.read()

            # End if window is closed
            if event == sg.WIN_CLOSED:
                warning_win.close()
                return False

            if event == "-RMVALL-":
                for element in dir_list:
                    try_to_delete(element)
                warning_win.close()
                return True
                    
            if event == "-RMHIGH-":
                for element in from_project:
                    try_to_delete(element)
                warning_win.close()
                return True
            
            if event == "-CANCEL-":
                warning_win.close()
                return False
                    
            


    def confirm_measurement_added(self):
        w, h = sg.Window.get_screen_size()

        GUI.non_blocking_popup("meas_pop_added", [w/2-50, h/2 +50], 'Green')
        sg.theme(GUI.theme)





    class TargetList(list):
        def __init__(self):
            char = "A"
            self.init_char = ord(char [0])
            
            # initialize target list with first element
            #              set,  visible, label
            self.dict_ = [[False, True,   None ]]

        
        def make_current_marker_character(self, target_num):
            char = self.init_char + target_num
            
            return chr(char)    


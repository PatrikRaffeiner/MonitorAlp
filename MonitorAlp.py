import PySimpleGUI as sg

# local imports
from project import *
from projectList import *
from MasterObj import *
import helpers
from exceptions import*


# --------------------------------------------------------------------------------------------------------#
#                                               main                                                      #
# --------------------------------------------------------------------------------------------------------#


# setting global theme
GUI.def_theme("Gray Gray Gray")


# initialize home window
home_win = GUI.make_start_window()


# classmethod loads master object from permanent file
# contains all recent projects, RC director 
master_obj = MasterObj.loader()

project_list = master_obj.project_list


# event loop
while True:
    event, values = home_win.read()

    # end if window is closed
    if event == sg.WIN_CLOSED:
        break
        
    # initial measurement mode
    if event == "-START-":
        new_project = Project()

        # catch closed setup window and return to home
        try: 
            new_project.setup(master_obj)
            init_drone_measurement = new_project.create_drone_measurement(init_status=True)
            init_manual_measurement = new_project.create_manual_measurement(init_drone_measurement.dir)

            new_project.get_GPS_coordinates(init_drone_measurement)

            new_project.RC_registration_and_export_points(init_drone_measurement, master_obj.RC_dir)
            
            try: 
                # raises exception when points cannot be found in RC export
                init_drone_measurement.compare_points()
                
            except:
                # remove directory for a clean folder structure
                init_drone_measurement.delete_directory()
                continue

            init_drone_measurement.transform_points()
            init_drone_measurement.sort_points()
             
            new_project.all_measurement_list.append(init_drone_measurement)
            new_project.all_measurement_list.append(init_manual_measurement)
            new_project.drone_measurement_list.append(init_drone_measurement)
            new_project.manual_measurement_list.append(init_manual_measurement)

            new_project.calc_distance_to_origin(init_drone_measurement)
            new_project.calc_accuracy_indicator(init_drone_measurement)

            project_list.append(new_project)

            master_obj.save()

            init_drone_measurement.visualize_points()
            init_drone_measurement.save()
            new_project.save()

            new_project.dump_xlsx_file()
            new_project.pdf = new_project.dump_pdf()

            # popup "Successfully created project"
            new_project.confirm_added_saved_element("pdf_pop_proj_create")


        except ClosedWindow as ex: 
            print(ex)
            pass

        except Exception as ex:
    
            print("Error during measurement processing:", ex)
            continue
        
        

    # load project mode
    if event == "-LOAD-":
        while True:
            project = project_list.select_project(master_obj)

            # case is no recent project is in project list
            # popup is handeled in line above (select_project) 
            if project == False: 
                break
        
            if project != None:
                project.overview(master_obj)


    # handle global language selection
    if values["-LANG-"] == "DE":
        # global 
        helpers.readout = helpers.deTextReadOut()

        home_win.close()
        del home_win

        home_win = GUI.make_start_window()
        home_win["-LANG-"].update("DE")


    else:
        # global
        helpers.readout = helpers.enTextReadOut()

        home_win.close()
        del home_win

        home_win = GUI.make_start_window()
        home_win["-LANG-"].update("EN")
        

home_win.close()


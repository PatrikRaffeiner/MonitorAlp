import PySimpleGUI as sg

# local imports
from project import *
from projectList import *
from MasterObj import *
import helpers


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
        #try: 
            new_project.setup(master_obj)
            init_drone_measurement = new_project.create_drone_measurement(init_status=True)
            init_manual_measurement = new_project.create_manual_measurement()


            new_project.RC_registration_and_export_points(init_drone_measurement, master_obj.RC_dir)
            
            # in case reality capture crashed due to any circumstances
            try: 
                init_drone_measurement.transform_points()
            except Exception as ex:
            #    init_drone_measurement.delete_directory()
            #    print("deleting: " + init_drone_measurement.dir + " because RC crashed")
            #    break
                print("Error during point transformation")
                print(ex)
            
            try: 
                init_drone_measurement.sort_points()
            except Exception as ex:
                print("Error during point sorting")
                print(ex)
            
            try: 
                new_project.all_measurement_list.append(init_drone_measurement)
                new_project.all_measurement_list.append(init_manual_measurement)
                new_project.drone_measurement_list.append(init_drone_measurement)
                new_project.manual_measurement_list.append(init_manual_measurement)
            except Exception as ex: 
                print("error during list appending")
                print(ex)
            
            try: 
                new_project.calc_distance_to_origin(init_drone_measurement)
            except Exception as ex: 
                print("error during distance calculation")
                print(ex)

            try: 
                project_list.append(new_project)
            except Exception as ex: 
                print("error during project list appending")
                print(ex)
                
            try: 
                master_obj.save()
            except Exception as ex: 
                print("error during master object saving")
                print(ex)

            init_drone_measurement.visualize_points()
            init_drone_measurement.save()
            new_project.save()

            new_project.dump_xlsx_file()

            new_project.confirm_measurement_added()



        #except Exception as ex:
    
            #print("Error during measurement processing:", ex)
            #continue
        
        

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


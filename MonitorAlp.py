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
        try: 
            new_project.setup(master_obj)
            init_measurment = new_project.create_measurement(init_status=True)

            new_project.RC_registration_and_save_points(init_measurment, master_obj.RC_dir)
            init_measurment.transform_points()
            init_measurment.sort_points()
            new_project.add_to_measurement_list(init_measurment)

            project_list.append(new_project)
            master_obj.save()

            init_measurment.visualize_points()
            init_measurment.save()
            new_project.save()

            new_project.dump_xlsx_file()

        except Exception as ex:
    
            print("Error during measurement processing:", ex)
            continue
        
        

    # load project mode
    if event == "-LOAD-":
        while True:
            project = project_list.select_project()

            # case is no recent project is in project list
            # popup is handeled in line above (select_project) 
            if project == False: 
                break
        
            if project != None:
                try:
                    project.overview(master_obj)

                except Exception as ex:
                    print("Error during loading:", ex)
                    break

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


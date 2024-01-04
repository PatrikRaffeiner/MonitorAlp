import PySimpleGUI as sg

# local imports

from project import *
from projectList import *
#from helpers import *
import helpers


# --------------------------------------------------------------------------------------------------------#
#                                               main                                                      #
# --------------------------------------------------------------------------------------------------------#


# setting global theme
GUI.def_theme("Gray Gray Gray")

# initialize home window
home_win = GUI.make_start_layout()

# classmethod loads recent projects from permanent file
project_list = ProjectList.loader()

# global variable/class
print(f"initial readout {readout}")
print("in main")


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
            new_project.setup()
            init_measurment = new_project.create_measurement(init_status=True)

            new_project.RC_registration_and_save_points(init_measurment)
            init_measurment.transform_points()
            init_measurment.sort_points()
            new_project.add_to_measurement_list(init_measurment)

            project_list.append(new_project)
            project_list.save()

            init_measurment.visualize_points()
            init_measurment.save()
            new_project.save()

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
                    project.overview(project_list)

                except Exception as ex:
                    print("Error during loading:", ex)
                    break

    # handle global language selection
    if values["-LANG-"] == "DE":
        # global 
        del helpers.readout
        helpers.readout = deTextReadOut()
        print(f"german readout {readout}")
        
        #local (current window)
        home_win["-TITLE-"].update(readout.gettext("hm_txt_title"))
        home_win["-START-"].update(readout.gettext("hm_btn_start"))
        home_win["-LOAD-"].update(readout.gettext("hm_btn_load"))



    else:
        # global
        del readout
        readout = enTextReadOut()
        print(f"english readout {readout}")
        
        #local (current window)
        home_win["-TITLE-"].update(readout.gettext("hm_txt_title"))
        home_win["-START-"].update(readout.gettext("hm_btn_start"))
        home_win["-LOAD-"].update(readout.gettext("hm_btn_load"))



home_win.close()


import PySimpleGUI as sg

# local imports
from helpers import *
from project import *
from projectList import *





# --------------------------------------------------------------------------------------------------------#
#                                               main                                                      #
# --------------------------------------------------------------------------------------------------------#


# initialize home window
home_win = GUI.make_start_layout()

# classmethod loads recent projects from permanent file
project_list = ProjectList.loader()



# event loop
while True:
    event, values = home_win.read()
    # end if window is closed
    if event == sg.WIN_CLOSED:
        break
        
    # initial measurement mode
    if event == "Start New Project":
        new_project = Project()

        # catch closed setup window and return to home
        try:
            new_project.setup()
            print("Setup complete")
        except:
            continue
        
        init_measurment = new_project.create_measurement()

        new_project.RC_registration_and_save_points(init_measurment)
        init_measurment.transform_points()
        init_measurment.sort_points()
        new_project.add_to_measurement_list(init_measurment)

        project_list.append(new_project)
        project_list.save()

        init_measurment.visualize_points()
        init_measurment.save()
        new_project.save()
        

    # load project mode
    if event == "Load Project":
        while True:
            project = project_list.select_project()

            if project == False: 
                break
        
            if project != None:
                project.overview(project_list)

            


home_win.close()


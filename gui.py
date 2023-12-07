import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg 
import numpy as np



class GUI():


    @classmethod
    def make_start_layout(self):
        layout_start = [
            [sg.Text("Monitoring Tool for Alpine Infrastructure", font=("Arial", 30), text_color="black")],
            [sg.Image("home_img.png")],
            [sg.Button("Start New Project"), sg.Push(), sg.Button("Load Project")]]

        start_win = sg.Window("MonitorAlp", layout_start, resizable=True)

        return start_win
    



    # creates the project setup window
    def make_project_setup_win(self):
        
        # column layouts
        measurement_location_col = [
            [sg.Text("Measurement Location / Location Name"),
            sg.In(size=(25,1), default_text="z.B. Klettersteig Ilmspitz", enable_events= True, key="-LOC-")]] 
        
        RC_path_col = [
            [sg.Text("RealityCapture exe"),
            sg.In(size=(25,1), enable_events= True, key="-EXE-"),
            sg.FileBrowse()]] 
        
        licence_checkbox_col = [
            [sg.Text("Licence already installed"),
            sg.Checkbox("Existing Licence", enable_events= True, key="-CHECK-", default=False)]]
        
        
        # create project setup layout
        layout_project_setup = [
            [sg.Text("Please enter the name of the via ferrata or the location where the measurement was conducted")],
            [sg.Column(measurement_location_col)],
            [sg.Text("Please find the installation execution of your RealityCapture software")],
            [sg.Column(RC_path_col)],
            [sg.HSeparator()],
            [sg.Text("Please check the box if your Reality Capture licence is already installed")],
            [sg.Column(licence_checkbox_col)],
            [sg.Button("Continue",disabled=True), sg.Button("Cancel")],
            ]

        
        # create setup input window
        project_setup_window = sg.Window("Project Setup", layout_project_setup)


        return project_setup_window

        



    def make_measurement_setup_win(self):
        imgs_tooltip = "Please find the location of your image folder"
        project_tooltip = "Please find the location where you want to save the project"


        image_path = [
            [sg.Text("Image Folder"),
            sg.In(size=(25,1), enable_events= True, key="-IMGFOLDER-", tooltip=imgs_tooltip),
            sg.FolderBrowse()]] 
        
        project_path = [
            [sg.Text("Project Folder"),
            sg.In(size=(25,1), enable_events= True, key="-PRJFOLDER-", tooltip=project_tooltip),
            sg.FolderBrowse()]] 

        # create layout for measurement setup GUI
        layout_browse_folder = [
            [sg.Column(project_path)],
            [sg.Column(image_path)],
            [sg.Button("Accept", disabled=True), sg.Button("Cancel")]]
 

        # create measurement setup window
        measurement_setup_window = sg.Window("Measurement Setup", layout_browse_folder)

        return measurement_setup_window
    
        



    def make_licence_browse_win(self):
        input_path = [
            [sg.Text("Licence File"),
            sg.In(size=(25,1), enable_events= True, key="-FILE-"),
            sg.FileBrowse()]] 

        input_PIN = [
            [sg.Text("Insert PIN"),
            sg.In(size=(25,1), enable_events= True, key="-PIN-")]] 

        licence_checkbox = [
            [sg.Checkbox("", enable_events= True, key="-CHECK-", default=False),
            sg.Text("Licence already installed"),
            sg.Button("Continue", disabled=True)]]


        # set up licence browse GUI
        layout_browse_licence = [
            [sg.Text("Please find an existing licence or insert PIN to buy a licence for your images")],
            [sg.Column(licence_checkbox)],
            [sg.HSeparator()],
            [sg.Column(input_path)],
            [sg.Button("Accept",disabled=True), sg.Button("Cancel")], 
            [sg.HSeparator()],
            [sg.Column(input_PIN)],
            [sg.Button("Pay",disabled=True), sg.Button("Cancel")]]


        # create licece browse window
        licence_browse_window = sg.Window("Browse Licence", layout_browse_licence)
        
        return licence_browse_window


    

    
    def make_marker_input_window(self):
        # reference coordinate/marker system
        origin_name_layout = [
            [sg.Text("Origin marker name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:01a", enable_events= True, key="-ORIG-")]] 
        
        horiz_name_layout = [
            [sg.Text("Horizontal marker name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:01b", enable_events= True, key="-HORIZ-")]] 
        
        vert_name_layout = [
            [sg.Text("Vertical marker name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:01c", enable_events= True, key="-VERT-")]]

        ref_dist_layout = [
            [sg.Text("Marker Distance in Millimeter"),
            sg.In(size=(25,1), default_text="120.0", enable_events= True, key="-DIST-")]]  
        

        # target marker system names
        targetA_name = [
            [sg.Text("Marker A name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:020", enable_events= True, key="-A-")]] 
        
        targetB_name = [
            [sg.Text("Marker B name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:021", enable_events= True, key="-B-")]] 
        
        targetC_name = [
            [sg.Text("Marker C name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:022", enable_events= True, key="-C-")]] 
        

        # set up marker input layout
        layout_marker_input = [
            [sg.Text("Please enter the name of the origin reference marker")],
            [sg.Column(origin_name_layout)],
            [sg.HSeparator()],
            [sg.Text("Please enter the name of the horizontal reference marker")],
            [sg.Column(horiz_name_layout)],
            [sg.HSeparator()],
            [sg.Text("Please enter the name of the vertical reference marker")],
            [sg.Column(vert_name_layout)],
            [sg.HSeparator()],
            [sg.Text("Please enter the distance between the reference points in mm")],
            [sg.Column(ref_dist_layout)],
            [sg.HSeparator()],
            [sg.HSeparator()],
            [sg.Text("Please enter the name of the origin reference marker")],
            [sg.Column(targetA_name)],
            [sg.HSeparator()],
            [sg.Text("Please enter the name of the horizontal reference marker")],
            [sg.Column(targetB_name)],
            [sg.HSeparator()],
            [sg.Text("Please enter the name of the vertical reference marker")],
            [sg.Column(targetC_name)],
            [sg.Button("OK", disabled=True), sg.Button("Cancel")]]
        
        # create marker input window
        marker_input_window = sg.Window("Reference And Target Marker", layout_marker_input)
        
        return marker_input_window
        
        



    def make_project_overview_window(self, measurement_names, project):

        select_lst = sg.Listbox(measurement_names, size=(35,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=True, key="-SELECT-")
        out_lst = sg.Listbox("", size=(25,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=False, key="-OUTPUT-")

        layout = [[sg.Text("Measurements", font=("Arial Bold", 14)), 
                   sg.Push(),  
                   sg.Text("Measurement Info", size=(21,1), font=("Arial Bold", 14))], 
                  [select_lst, out_lst], 
                  [Btn_10("Add Measurement", key="-ADD-"), 
                   sg.Push(), 
                   sg.Button("Calc Displacement", disabled=True, key="-CALC-"),
                   sg.Push(), 
                   sg.Button("Delete Measurement", disabled=True, key="-DEL-")]]
        
        overview_window = sg.Window(project.name + " Measurement Overview", layout)

        return overview_window, select_lst

        



    def show_displacement(self, init_targets, subseq_targets):
        name_size = 10
        di_size = 9

        layout = [[Txt_10("Target name", size=(name_size,1)), 
                   Txt_10("dx (mm)", size=(di_size,1)), 
                   Txt_10("dy (mm)", size=(di_size,1)), 
                   Txt_10("dz (mm)", size=(di_size,1)), 
                   Txt_10("abs (mm)", size=(di_size,1))]]
        
        for init_target, subseq_target in zip(init_targets, subseq_targets):
            
            abs_dist = np.linalg.norm(subseq_target.pos-init_target.pos)

            dx = "{:.3f}".format(1000*subseq_target.displacement[0])
            dy = "{:.3f}".format(1000*subseq_target.displacement[1])
            dz = "{:.3f}".format(1000*subseq_target.displacement[2])
            abs_dist = "{:.3f}".format(1000*abs_dist)

            layout.append([Txt_10(subseq_target.name,size=(name_size,1)), Txt_10(dx, size=(di_size,1)), Txt_10(dy, size=(di_size,1)), Txt_10(dz, size=(di_size,1)), Txt_10(abs_dist, size=(di_size,1))])
        
        displacement_winow = sg.Window("Displacements", layout)


        while True:
            event, values = displacement_winow.read()

            # End if window is closed
            if event == sg.WIN_CLOSED:
                displacement_winow.close()
                break




    def make_project_list_window(self, project_names):      

        recent_projects = sg.Listbox(project_names, size=(40,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=True, key="-SELECT-")

        layout = [[sg.Text("Recent Projects")],
                  [recent_projects],
                  [Btn_10("Load",  key="-LOAD-", disabled=True), sg.Push()]]
                
        load_win = sg.Window("Load Recent Projects", layout)

        return load_win, recent_projects

        

        










def Btn_10(*args, button_color=('white', 'black'), **kwargs):
    return(sg.Button(*args, font='Arial 10',button_color=button_color, **kwargs))


def Txt_10(*args, **kwargs):
    return(sg.Text(*args, font=("Arial Bold", 10), **kwargs))
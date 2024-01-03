import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg 
import numpy as np



class GUI():

    @classmethod
    def def_theme(cls, theme):
        # changes color theme of complete UI
        
        sg.theme(theme)
        cls.theme = theme



    @classmethod
    def make_start_layout(self):
        # creates home window
        layout_start = [
            [sg.Text("Monitoring Tool for Alpine Infrastructure", font=("Arial", 26), text_color="black"), 
             sg.Push(), sg.Drop(["DE", "EN"], enable_events= True, key="-LANG-", default_value="EN")], 
            [sg.Image("home_img.png")],
            [sg.Button("Start New Project"), sg.Push(), sg.Button("Load Project")]]

        start_win = sg.Window("MonitorAlp", layout_start, resizable=True)

        return start_win
    



    def make_project_setup_win(self):
        # creates project setup window

        # tooltips
        tip_exe = "Please find the path to your Reality Capture installation/execution (RealityCapture.exe)"
        
        # column layouts
        project_location_col = [
            [sg.Text("Project Location / Location Name"),
            sg.In(size=(25,1), default_text="z.B. Klettersteig Ilmspitz", enable_events= True, key="-LOC-")]] 
        
        RC_path_col = [
            [sg.Text("RealityCapture exe"),
            sg.In(size=(25,1), enable_events= True, key="-EXE-", tooltip=tip_exe),
            sg.FileBrowse()]] 
        
        licence_checkbox_col = [
            [sg.Text("Licence already installed"),
            sg.Checkbox("Existing Licence", enable_events= True, key="-CHECK-", default=False)]]
        
        
        # create project setup layout
        layout_project_setup = [ 
            [sg.Text("Please enter the name of the via ferrata or the location where the measurement was conducted")],
            [sg.Column(project_location_col)],
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

        



    def make_init_measurement_setup_win(self):
        # creates measurement setup window for initial measurement
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
    




    def make_measurement_setup_win(self):
        # creates measurement setup window for additional measurement
        imgs_tooltip = "Please find the location of your image folder"


        image_path = [
            [sg.Text("Image Folder"),
            sg.In(size=(25,1), enable_events= True, key="-IMGFOLDER-", tooltip=imgs_tooltip),
            sg.FolderBrowse()]] 
        

        # create layout for measurement setup GUI
        layout_browse_folder = [
            [sg.Column(image_path)],
            [sg.Button("Accept", disabled=True), sg.Button("Cancel")]]
 

        # create measurement setup window
        measurement_setup_window = sg.Window("Measurement Setup", layout_browse_folder)

        return measurement_setup_window
    
        



    def make_licence_browse_win(self):
        # 
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


    

    
    def make_marker_input_window(self, target_list):
        # tooltips
        tip_dist = "Please provide the reference distance in the format: xxx.x"

        # reference coordinate/marker system
        origin_name_layout = [
            [sg.Text("Origin-marker name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:01a", enable_events= True, key="-ORIG-")]] 
        
        horiz_name_layout = [
            [sg.Text("Horizontal-marker name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:01b", enable_events= True, key="-HORIZ-")]] 
        
        vert_name_layout = [
            [sg.Text("Vertical-marker name"),
            sg.In(size=(25,1), default_text="z.B. 1x12:01c", enable_events= True, key="-VERT-")]]

        ref_dist_layout = [
            [sg.Text("Marker Distance in Millimeter"),
            sg.In(size=(25,1), default_text="120.0", enable_events= True, tooltip=tip_dist, key="-DIST-")]]  
        

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
            [sg.Col([self.marker_row(target_list, 0)], key="-TARGET SECTION-")],
            [sg.Button("Add Target Marker", key="-ADD-"), sg.Push(), sg.Button("Continue", disabled=True)]]
        
        # create marker input window
        marker_input_window = sg.Window("Reference And Target Marker", layout_marker_input, metadata=0)
        
        return marker_input_window





    def marker_row(self,target_list, target_num):
            text = target_list.make_current_marker_text(target_num)

            print(f"from marker row: {target_num}")

            if target_num == 0:
                instruction_text = "Please enter the name of the 1st target marker"
            elif target_num == 1:
                instruction_text = "Please enter the name of the 2nd target marker"
            elif target_num == 2:
                instruction_text = "Please enter the name of the 3rd target marker"
            else:
                instruction_text = "Please enter the name of the " + str(target_num) + "th target marker"

            marker_input_row = [sg.pin(sg.Col([
                    [sg.Text(instruction_text)],
                    [sg.Text(text),
                    sg.In(size=(25,1), default_text="z.B. 1x12:020", enable_events= True, key=("-TARGET-", target_num))]]))]

            return marker_input_row    
        




    def make_project_overview_window(self, measurement_names, project):

        select_lst = sg.Listbox(measurement_names, size=(35,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=True, key="-SELECT-")
        out_lst = sg.Listbox("", size=(25,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=False, key="-OUTPUT-")

        tooltip_del = "Please select a measurement to delete"

        layout = [[sg.Text("Measurements", font=("Arial Bold", 14)), 
                   sg.Push(),  
                   sg.Text("Measurement Info", size=(21,1), font=("Arial Bold", 14))], 
                  [select_lst, out_lst], 
                  [Btn_10("Add Measurement", key="-ADD-"), 
                   sg.Push(), 
                   sg.Button("Calc Displacement", disabled=True, key="-CALC-"),
                   sg.Push(), 
                   #sg.Button("Duplicate Measurement", disabled=True, key="-DUPL-", button_color=("black","OliveDrab3")), # remove this line
                   #sg.Push(),                                                       # remove this line
                   sg.Button("Delete Measurement", button_color=("white","firebrick3"), disabled=True, key="-DEL-", tooltip=tooltip_del)]]
        
        overview_window = sg.Window(project.name + " Measurement Overview", layout)

        return overview_window, select_lst

        



    def show_displacement(self, init_targets, subseq_targets):
        name_size = 10
        di_size = 9

        layout = [[Txt_10("Target name", size=(name_size,1)), 
                   Txt_10("dx (mm)", size=(di_size,1)), 
                   Txt_10("dy (mm)", size=(di_size,1)), 
                   Txt_10("dz (mm)", size=(di_size,1)), 
                   Txt_10("abs (mm)", size=(di_size,1)),
                   Txt_10("distance to origin (mm)", size=(di_size*2,1))]]
        
        for init_target, subseq_target in zip(init_targets, subseq_targets):
            
            abs_dist = np.linalg.norm(subseq_target.pos-init_target.pos)

            dx = "{:.3f}".format(1000*subseq_target.displacement[0])
            dy = "{:.3f}".format(1000*subseq_target.displacement[1])
            dz = "{:.3f}".format(1000*subseq_target.displacement[2])
            abs_dist = "{:.3f}".format(1000*abs_dist)
            dist_to_orig = "{:.3f}".format(1000*subseq_target.distance_from_origin)

            layout.append([Txt_10(subseq_target.name,size=(name_size,1)), 
                           Txt_10(dx, size=(di_size,1)), 
                           Txt_10(dy, size=(di_size,1)), 
                           Txt_10(dz, size=(di_size,1)), 
                           Txt_10(abs_dist, size=(di_size,1)), 
                           Txt_10(dist_to_orig, size=(di_size,1))])
        
        displacement_winow = sg.Window("Displacements", layout)


        while True:
            event, values = displacement_winow.read()

            # End if window is closed
            if event == sg.WIN_CLOSED:
                displacement_winow.close()
                break





    def make_project_list_window(self, project_names):      

        recent_projects = sg.Listbox(project_names, size=(40,10), font=("Arial Bold", 14), 
                                     expand_y=True, expand_x=True, enable_events=True, 
                                     key="-SELECT-")

        layout = [[sg.Text("Recent Projects")],
                  [recent_projects],
                  [Btn_10("Load",  key="-LOAD-", disabled=True), sg.Push()]]
                
        load_win = sg.Window("Load Recent Projects", layout, finalize=True)

        # Add the ability to double-click an element
        load_win["-SELECT-"].bind('<Double-Button-1>' , "+-double click-")

        return load_win, recent_projects

        


    @classmethod
    def make_warning_window(cls, warning_str):
        
        # change window layout
        sg.theme("DarkRed1")

        warning_layout = [
            [sg.Text(warning_str, font=("Arial", 22), text_color="black")],
            [sg.Button("Acknowledge"), sg.Push(), sg.Button("Cancel")]]
        
        warn_window = sg.Window("Warning!", warning_layout, keep_on_top=True, finalize=True)

        # change theme back to original for subsequent windows
        sg.theme(cls.theme)

        return warn_window



    @classmethod    
    def popup(cls, message):
        sg.theme('DarkRed1')
        layout = [[sg.Text(message)]]
        pop_window = sg.Window('Message', layout, no_titlebar=True, keep_on_top=True, finalize=True)
        sg.theme(cls.theme)
        return pop_window









def Btn_10(*args, button_color=('white', 'black'), **kwargs):
    return(sg.Button(*args, font='Arial 10',button_color=button_color, **kwargs))


def Txt_10(*args, **kwargs):
    return(sg.Text(*args, font=("Arial Bold", 10), **kwargs))
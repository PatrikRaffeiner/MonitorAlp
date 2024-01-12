import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg 
import numpy as np

import helpers



class GUI():


    @classmethod
    def def_theme(cls, theme):
        # changes color theme of complete UI
        
        sg.theme(theme)
        cls.theme = theme



    @classmethod
    def make_start_window(self):
        # creates home window

        

        layout_start = [
            [sg.Text(getText("hm_txt_title"), font=("Arial", 26), key="-TITLE-", text_color="black"), 
             sg.Push(), sg.Drop(["DE", "EN"], enable_events= True, key="-LANG-", default_value="DE")], 
            [sg.Image("home_img.png")],
            [sg.Button(getText("hm_btn_start"), key="-START-"), sg.Push(), sg.Button(getText("hm_btn_load"), key="-LOAD-")]]

        start_win = sg.Window("MonitorAlp", layout_start, resizable=True, finalize=True)

        return start_win
    



    def make_project_setup_win(self):
        # creates project setup window

        # tooltips
        tip_exe = getText("setup_tip_exe")

        
        # column layouts
        project_location_col = [
            [sg.Text(getText("setup_txt_name")),
            sg.In(size=(25,1), default_text="z.B. Klettersteig Ilmspitz", enable_events= True, key="-LOC-")]] 
        
        RC_path_col = [
            [sg.Text("RealityCapture exe"),
            sg.In(size=(25,1), enable_events= True, key="-EXE-", tooltip=tip_exe),
            sg.FileBrowse(getText("browse_btn"))]] 
        
        licence_checkbox_col = [
            [sg.Checkbox(getText("setup_cbx_licence"), enable_events= True, key="-CHECK-", default=False)]]
        
        
        # create project setup layout
        layout_project_setup = [ 
            [sg.Text(getText("pjct_txt_name"))],
            [sg.Column(project_location_col)],
            [sg.Text(getText("pjct_txt_RC"))],
            [sg.Column(RC_path_col)],
            [sg.HSeparator()],
            [sg.Text(getText("pjct_cbx_licence"))],
            [sg.Column(licence_checkbox_col)],
            [sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True), 
             sg.Button(getText("cancel_btn"), key="-CANCEL-")],
            ]

        
        # create setup input window
        project_setup_window = sg.Window(getText("setup_win_title"), layout_project_setup)


        return project_setup_window

        



    def make_init_measurement_setup_win(self):
        # creates measurement setup window for initial measurement
        imgs_tooltip = getText("init_tip_imgs")
        project_tooltip = getText("init_tip_proj")


        image_path = [
            [sg.Text(getText("init_txt_img")),
            sg.In(size=(25,1), enable_events= True, key="-IMGFOLDER-", tooltip=imgs_tooltip),
            sg.FolderBrowse()]] 
        
        project_path = [
            [sg.Text(getText("init_txt_proj")),
            sg.In(size=(25,1), enable_events= True, key="-PRJFOLDER-", tooltip=project_tooltip),
            sg.FolderBrowse()]] 

        # create layout for measurement setup GUI
        layout_browse_folder = [
            [sg.Column(project_path)],
            [sg.Column(image_path)],
            [sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True), sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
 

        # create measurement setup window
        measurement_setup_window = sg.Window(getText("init_win_title"), layout_browse_folder)

        return measurement_setup_window
    




    def make_measurement_setup_win(self):
        # creates measurement setup window for additional measurement
        imgs_tooltip = getText("init_tip_imgs")


        image_path = [
            [sg.Text(getText("init_txt_img")),
            sg.In(size=(25,1), enable_events= True, key="-IMGFOLDER-", tooltip=imgs_tooltip),
            sg.FolderBrowse()]] 
        

        # create layout for measurement setup GUI
        layout_browse_folder = [
            [sg.Column(image_path)],
            [sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True), 
             sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
 

        # create measurement setup window
        measurement_setup_window = sg.Window(getText("init_win_title"), layout_browse_folder)

        return measurement_setup_window
    
        



    def make_licence_browse_win(self):
        # 
        input_path = [
            [sg.Text(getText("lic_txt_file")),
            sg.In(size=(25,1), enable_events= True, key="-FILE-"),
            sg.FileBrowse()]] 

        input_PIN = [
            [sg.Text(getText("lic_txt_pin")),
            sg.In(size=(25,1), enable_events= True, key="-PIN_INPUT-")]] 

        licence_checkbox = [
            [sg.Checkbox("", enable_events= True, key="-CHECK-", default=False),
            sg.Text(getText("setup_cbx_licence")),
            sg.Button(getText("continue_btn"), disabled=True)]]


        # set up licence browse GUI
        layout_browse_licence = [
            [sg.Text(getText("lic_text_desc"))],
            [sg.Column(licence_checkbox)],
            [sg.HSeparator()],
            [sg.Column(input_path)],
            [sg.Button(getText("continue_btn"), disabled=True, key="-CONTINUE-"), sg.Button(getText("cancel_btn"))], 
            [sg.HSeparator()],
            [sg.Column(input_PIN)],
            [sg.Button(getText("lic_txt_pay"),disabled=True, key="-PAY_BTN-"), sg.Button(getText("cancel_btn"))]]


        # create licece browse window
        licence_browse_window = sg.Window(getText("lic_win_title"), layout_browse_licence)
        
        return licence_browse_window


    

    
    def make_marker_input_window(self, target_list):
        # tooltips
        tip_dist = getText("mrk_tip_dist")

        # reference coordinate/marker system
        origin_name_layout = [
            [sg.Text(getText("mrk_txt_orig")),
            sg.In(size=(25,1), default_text="z.B. 1x12:01a", enable_events= True, key="-ORIG-")]] 
        
        horiz_name_layout = [
            [sg.Text(getText("mrk_txt_hrz")),
            sg.In(size=(25,1), default_text="z.B. 1x12:01b", enable_events= True, key="-HORIZ-")]] 
        
        vert_name_layout = [
            [sg.Text(getText("mrk_txt_vtk")),
            sg.In(size=(25,1), default_text="z.B. 1x12:01c", enable_events= True, key="-VERT-")]]

        ref_dist_layout = [
            [sg.Text(getText("mrk_txt_dist")),
            sg.In(size=(25,1), default_text="z.B. 120.0", enable_events= True, tooltip=tip_dist, key="-DIST-")]]  
        

        # set up marker input layout
        layout_marker_input = [
            [sg.Text(getText("mrk_txt_descO"))],
            [sg.Column(origin_name_layout)],
            [sg.HSeparator()],
            [sg.Text(getText("mrk_txt_descV"))],
            [sg.Column(horiz_name_layout)],
            [sg.HSeparator()],
            [sg.Text(getText("mrk_txt_descH"))],
            [sg.Column(vert_name_layout)],
            [sg.HSeparator()],
            [sg.Text(getText("mrk_txt_descD"))],
            [sg.Column(ref_dist_layout)],
            [sg.HSeparator()],
            [sg.HSeparator()],
            [sg.Col([self.marker_row(target_list, 0)], key="-TARGET SECTION-")],
            [sg.Button(getText("mrk_btn_add"), key="-ADD-"), sg.Push(), sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True)]]
        
        # create marker input window
        marker_input_window = sg.Window(getText("mrk_win_title"), layout_marker_input, metadata=0)
        
        return marker_input_window





    def marker_row(self,target_list, target_num):
            curr_char = target_list.make_current_marker_character(target_num)

            text = getText("mrk_txt") + curr_char

            instruction_text = getText("mrk_txt_pre") + str(target_num+1) + getText("mrk_txt_post")

            marker_input_row = [sg.pin(sg.Col([
                    [sg.Text(instruction_text)],
                    [sg.Text(text),
                    sg.In(size=(25,1), default_text="z.B. 1x12:020", enable_events= True, key=("-TARGET-", target_num))]]))]

            return marker_input_row    
        




    def make_project_overview_window(self, measurement_names, project):

        select_lst = sg.Listbox(measurement_names, size=(35,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=True, key="-SELECT-")
        out_lst = sg.Listbox("", size=(25,10), font=("Arial Bold", 14), expand_y=True, expand_x=True, enable_events=False, key="-OUTPUT-")

        tooltip_del = getText("meas_tip_del") 

        layout = [[sg.Text(getText("meas_txt_meas") , font=("Arial Bold", 14)), 
                   sg.Push(),  
                   sg.Text(getText("meas_txt_measInfo") , size=(21,1), font=("Arial Bold", 14))], 
                  [select_lst, out_lst], 
                  [Btn_10(getText("meas_btn_add"), key="-ADD-"), 
                   sg.Push(), 
                   sg.Button(getText("meas_btn_calc"), disabled=True, key="-CALC-"),
                   sg.Push(), 
                   #sg.Button("Duplicate Measurement", disabled=True, key="-DUPL-", button_color=("black","OliveDrab3")), # remove this line
                   #sg.Push(),                                                       # remove this line
                   sg.Button(getText("meas_btn_del"), button_color=("white","firebrick3"), disabled=True, key="-DEL-", tooltip=tooltip_del)]]
        
        overview_window = sg.Window(project.name + getText("meas_win_title"), layout)

        return overview_window, select_lst

        



    def show_displacement(self, init_targets, subseq_targets):
        name_size = 10
        di_size = 9

        layout = [[Txt_10(getText("disp_txt_trgt"), size=(name_size,1)), 
                   Txt_10("dx (mm)", size=(di_size,1)), 
                   Txt_10("dy (mm)", size=(di_size,1)), 
                   Txt_10("dz (mm)", size=(di_size,1)), 
                   Txt_10("abs (mm)", size=(di_size,1)),
                   Txt_10(getText("disp_txt_dist"), size=(di_size*2,1))]]
        
        for init_target, subseq_target in zip(init_targets, subseq_targets):
            
            abs_dist = np.linalg.norm(subseq_target.pos-init_target.pos)

            dx = "{:.2f}".format(1000*subseq_target.displacement[0])
            dy = "{:.2f}".format(1000*subseq_target.displacement[1])
            dz = "{:.2f}".format(1000*subseq_target.displacement[2])
            abs_dist = "{:.2f}".format(1000*abs_dist)
            dist_to_orig = "{:.2f}".format(1000*subseq_target.distance_from_origin)

            layout.append([Txt_10(subseq_target.name,size=(name_size,1)), 
                           Txt_10(dx, size=(di_size,1)), 
                           Txt_10(dy, size=(di_size,1)), 
                           Txt_10(dz, size=(di_size,1)), 
                           Txt_10(abs_dist, size=(di_size,1)), 
                           Txt_10(dist_to_orig, size=(di_size,1))])
        
        displacement_winow = sg.Window(getText("disp_win_title"), layout)


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

        layout = [[sg.Text(getText("pjlist_txt_pjcts"))],
                  [recent_projects],
                  [sg.Button(getText("pjlist_btn_load"), key="-LOAD-", disabled=True), 
                   sg.Push(), 
                   sg.Button(getText("pjlist_btn_del"), button_color=("white","firebrick3"), disabled=True, key="-DEL-")]]
                
        load_win = sg.Window(getText("pjlist_win_title"), layout, finalize=True)

        # Add the ability to double-click an element
        load_win["-SELECT-"].bind('<Double-Button-1>' , "+-double click-")

        return load_win, recent_projects



    @classmethod
    def make_delete_warning(cls, related, not_related):
        # change window layout
        sg.theme("DarkRed1")

        related_str = ""
        not_related_str = ""

        for file_folder in related:
            related_str = related_str + "-  " + str(file_folder) + "\n"

        for file_folder in not_related:
            not_related_str = not_related_str + "-  " + str(file_folder) + "\n"


        text_str = getText("pjct_txt_warnremove") + "\n" + related_str + not_related_str
        

        warning_layout = [
            [sg.Text(getText("pjct_txt_warnremove"), font=("Helvetica", 12), text_color="black")],
            [sg.Text(related_str, font=("Helvetica", 12, "bold"), text_color="black")],
            [sg.Text(not_related_str, font=("Helvetica", 12), text_color="black")],
            [sg.Button(getText("pjct_btn_rmvall"), key="-RMVALL-"), 
             sg.Push(), 
             sg.Button(getText("pjct_btn_rmvhigh"), key="-RMHIGH-"), 
             sg.Push(), 
             sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
        
        warn_window = sg.Window(getText("warn_btn"), warning_layout, keep_on_top=True, finalize=True)

        # change theme back to original for subsequent windows
        sg.theme(cls.theme)

        return warn_window




    @classmethod
    def make_warning_window(cls, warning_str):
        
        # change window layout
        sg.theme("DarkRed1")

        warning_layout = [
            [sg.Text(warning_str, font=("Arial", 22), text_color="black")],
            [sg.Button(getText("acknowl_btn"), key="-ACKNOWLEDGE-"), sg.Push(), sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
        
        warn_window = sg.Window(getText("warn_btn"), warning_layout, keep_on_top=True, finalize=True)

        # change theme back to original for subsequent windows
        sg.theme(cls.theme)

        return warn_window



    @classmethod    
    def popup(cls, ID, location):

        p1 = location[0]
        p2 = location[1] - 100
        location = (p1, p2)
        sg.theme('DarkRed1')
        pop_window = sg.popup_non_blocking(getText(ID), no_titlebar=True, 
                                           auto_close=True, location=location,
                                           auto_close_duration=4.5)
        sg.theme(cls.theme)
        return pop_window









def Btn_10(*args, button_color=('white', 'black'), **kwargs):
    return(sg.Button(*args, font='Arial 10',button_color=button_color, **kwargs))


def Txt_10(*args, **kwargs):
    return(sg.Text(*args, font=("Arial Bold", 10), **kwargs))


def getText(ID):
        return helpers.readout.gettext(ID)
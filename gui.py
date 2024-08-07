import PySimpleGUI as sg 

# local imports
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
            [sg.Image("imgs/home_img.png")],
            [sg.Button(getText("hm_btn_start"), key="-START-"), sg.Push(), sg.Button(getText("hm_btn_load"), key="-LOAD-")]]

        start_win = sg.Window("MonitorAlp", layout_start, resizable=True, finalize=True)

        return start_win
    



    def make_project_setup_win(self, RC_dir):
        # creates project setup window

        # tooltips
        tip_exe = getText("setup_tip_exe")
        tip_dist = getText("mrk_tip_dist")

        
        # column layouts
        project_location_col = [
            [sg.Text(getText("setup_txt_name")),
            sg.In(size=(25,1), default_text="z.B. Klettersteig_Ilmspitz_BlockA", enable_events= True, key="-LOC-")]] 
        

        project_max_shift_col = [
            [sg.Text(getText("setup_max_shift")),
            sg.In(size=(25,1), default_text="z.B. 2.5", enable_events= True,
                  tooltip=tip_dist, key="-LIMIT-")]] 
        

        # handles possible existing RealityCapture execution directory from master file
        if RC_dir == None:
            RC_lines = [
            [sg.Text(getText("pjct_txt_RC"))],
            [[sg.Text("RealityCapture exe"),
             sg.In(size=(25,1), enable_events= True, key="-EXE-", tooltip=tip_exe),
             sg.FileBrowse(getText("browse_btn"))]]] 

        # empty line due to existing RC execution dir    
        else: 
            RC_lines = [sg.Text("")]
        
        
        # create project setup layout
        layout_project_setup = [ 
            [sg.Text(getText("setup_txt_loc"), font=["Arial", 11, "bold"])],
            [sg.Text(getText("pjct_txt_name"))],
            [sg.Column(project_location_col)],
            RC_lines,
            [sg.HSeparator()],
            [sg.HSeparator()],
            [sg.Text(getText("props_txt_limit"), font=["Arial", 11, "bold"])],
            [sg.Text(getText("setup_max_desc"))],
            [sg.Column(project_max_shift_col)],
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


        project_path = [
            [sg.Text(getText("setup_txt_pjct"))],
            [sg.Text(getText("init_txt_proj")),
            sg.In(size=(25,1), enable_events= True, key="-PRJFOLDER-", tooltip=project_tooltip),
            sg.FolderBrowse()],
            [sg.HSeparator()], 
            [sg.HSeparator()]] 

        image_path = [
            [sg.Text(getText("setup_txt_img"))],
            [sg.Text(getText("init_txt_img")),
            sg.In(size=(25,1), enable_events= True, key="-IMGFOLDER-", tooltip=imgs_tooltip),
            sg.FolderBrowse()]] 
        

        # create layout for measurement setup GUI
        layout_browse_folder = [
            [sg.Column(project_path)],
            [sg.Column(image_path)],
            [sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True),
             sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
 

        # create measurement setup window
        measurement_setup_window = sg.Window(getText("init_win_title"), 
                                             layout_browse_folder)

        return measurement_setup_window
    



    def make_manual_measurement_input_window(self, project):
        # tooltips
        tip_man_dist = getText("mrk_tip_man_dist")

        manual_measurement_layout = [
            [sg.Text(getText("manMeas_txt_desc"))]]
        
        for target_name in project.target_list.labels:
            manual_measurement_layout.append([sg.Text(target_name + " (mm)"), 
                                              sg.In(size=(25,1), default_text="z.B. 125.6", enable_events=True, tooltip=tip_man_dist, key=("-TARGET-", target_name))])
                
        manual_measurement_layout.append([sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True), 
             sg.Button(getText("cancel_btn"), key="-CANCEL-")])


        # create manual measurement input window
        measurement_setup_window = sg.Window(getText("manMeas_win_title"), manual_measurement_layout)

        return measurement_setup_window




    def make_weather_info_window(self):
        # spacing for images and radio
        sep_images = 1
        sep_radio = 2

        weather_conditions = [
                    [sg.Text(getText("weather_txt_instrW"))],
                    [sg.Text("", size=(sep_images,1)), sg.Image("imgs/sunny.png"), 
                    sg.Text("", size=(sep_images,1)), sg.Image("imgs/partly_cloudy.png"),
                    sg.Text("", size=(sep_images,1)), sg.Image("imgs/cloudy.png"), 
                    sg.Text("", size=(sep_images,1)), sg.Image("imgs/foggy.png"),
                    sg.Text("", size=(sep_images,1)), sg.Image("imgs/rainy.png"), 
                    sg.Text("", size=(sep_images,1)), sg.Image("imgs/snowy.png")],
                    [sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::sunny", enable_events=True), 
                    sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::partly_cloudy", enable_events=True), 
                    sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::cloudy", enable_events=True),
                    sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::foggy", enable_events=True),
                    sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::rainy", enable_events=True),
                    sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::snowy", enable_events=True),
                    sg.Text("", size=(sep_radio,1))]]

        temperature = [
            [sg.Text(getText("weather_txt_instrT"))],
            [sg.In("", size=(3,1), key="-TEMP-", enable_events=True), sg.Text("°C")]]

        weather_info_layout = [
            [sg.Column(weather_conditions)],
            [sg.Column(temperature)],
            [sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True),
            sg.Button(getText("cancel_btn"), key="-CANCEL-")]]

        weather_info_window = sg.Window(getText("weather_win_title"), weather_info_layout)

        return weather_info_window




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
    
        

    
    def make_marker_input_window(self, target_list):

        # set up marker input layout
        layout_marker_input = [
            [sg.Col([self.marker_row(target_list, 0)], key="-TARGET SECTION-")],
            [sg.Button(getText("mrk_btn_add"), key="-ADD-"), 
             sg.Push(), 
             sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True)]]
        
        # create marker input window
        marker_input_window = sg.Window(getText("mrk_win_title"), layout_marker_input, metadata=0)
        
        return marker_input_window




    def marker_row(self, target_list, target_num):
            curr_char = target_list.make_current_marker_character(target_num)

            text = getText("mrk_txt") + curr_char
            tip_name = getText("mrk_tip_name")

            instruction_text = getText("mrk_txt_pre") + str(target_num+1) + getText("mrk_txt_post")

    
            marker_input_row = [sg.pin(sg.Col([
                    [sg.Text(instruction_text)],
                    [sg.B("x", border_width=0, button_color=("red", sg.theme_background_color()), k=('-DELETE-', target_num), tooltip='Delete this item'),
                    sg.Text(text),
                    sg.In(size=(25,1), default_text="z.B. 1x12:020", enable_events= True, tooltip=tip_name, key=("-TARGET-", target_num))]], key=("-ROW-", target_num)))]

            return marker_input_row    




    def make_date_and_time_acquisition_window(self):
        # set up date&time input layout
        acquisition_layout = [
            [sg.Text(getText("meas_txt_acqu"))],
            [sg.Text(getText("meas_txt_date")), 
             sg.In(size=(25,1), enable_events= True, key="-DATE-")],
             [sg.Text(getText("meas_txt_time")), 
             sg.In(size=(25,1), enable_events= True, key="-TIME-")],
             [sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True),
              sg.Button(getText("cancel_btn"), key="-CANCEL-")]] 
        

        # create marker input window
        time_date_acquisition_window = sg.Window(getText("meas_win_acqu"), acquisition_layout, metadata=0)
        
        return time_date_acquisition_window




    def make_project_overview_window(self, drone_measurements, manual_measurements, project):

        drone_measurement_names = [drone_measurement.name for drone_measurement in drone_measurements]
        manual_measurement_names = [manual_measurement.name for manual_measurement in manual_measurements]

        drone_lst = sg.Listbox(drone_measurement_names, size=(35,15), font=("Arial Bold", 14), key="-DRONE_SELECT-", expand_y=True, enable_events=True, horizontal_scroll=True)
        manual_lst = sg.Listbox(manual_measurement_names, size=(35,15), font=("Arial Bold", 14), key="-MANUAL_SELECT-" , expand_y=True,  enable_events=True, horizontal_scroll=True)
        out_lst = sg.Listbox("", size=(35,20), font=("Arial Bold", 14), key="-OUTPUT-", expand_y=True, enable_events=False, horizontal_scroll=True)

        # Menu Element Definition
        menu_def = [[getText("meas_menu_prjct"), [getText("meas_menu_pdfP"), getText("meas_menu_save"), 
                                                  getText("meas_menu_props"), getText("meas_menu_map"), 
                                                  getText("meas_menu_openPjct"), 
                                                  '---', getText("meas_menu_delP")]], 
                    [getText("meas_menu_drone"), [getText("meas_menu_addD"), getText("meas_menu_disp"), 
                                                  getText("meas_menu_cmmntD"), getText("meas_menu_open"),
                                                  getText("meas_menu_openMeas"),
                                                  getText("meas_menu_propsD"),
                                                  '---', getText("meas_menu_delD")]],
                    [getText("meas_menu_manual"), [getText("meas_menu_addM"), 
                                                   getText("meas_menu_cmmntM"),
                                                   getText("meas_menu_propsM"),  
                                                   '---', getText("meas_menu_delM")]],
                    ['Help', ['About...']]]


        layout = [[sg.Text(getText("meas_txt_drone") , font=("Arial Bold", 14)), 
                   sg.Push(),
                   sg.Menu(menu_def, key="-MENU-"),
                   sg.Text(getText("meas_txt_manual") , font=("Arial Bold", 14)), 
                   sg.Push(),   
                   sg.Text(getText("meas_txt_measInfo") , size=(36,1), font=("Arial Bold", 14))], 
                  [drone_lst, manual_lst, out_lst], 
                  [sg.Button("Dump PDF", key="-DUMP-", button_color=("black","OliveDrab3")), # remove this line
                   ]]
        
        overview_window = sg.Window(project.name + getText("meas_win_title"), layout, finalize=True)

        return overview_window, drone_lst, manual_lst, menu_def
    
        


    def show_displacement(self, subseq_targets):
        name_size = 10
        di_size = 9

        layout = [[Txt_10(getText("disp_txt_trgt"), size=(name_size,1)), 
                   Txt_10("dx (mm)", size=(di_size,1)), 
                   Txt_10("dy (mm)", size=(di_size,1)), 
                   Txt_10("dz (mm)", size=(di_size,1)), 
                   Txt_10("abs (mm)", size=(di_size,1)),
                   Txt_10(getText("disp_txt_dist"), size=(di_size*2,1))]]
        
        for subseq_target in subseq_targets:

            dx = "{:.2f}".format(1000*subseq_target.displacement[0])
            dy = "{:.2f}".format(1000*subseq_target.displacement[1])
            dz = "{:.2f}".format(1000*subseq_target.displacement[2])
            abs_dist = "{:.2f}".format(1000*subseq_target.displacement[3])
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




    def make_project_load_window(self, project_names):      

        recent_projects = sg.Listbox(project_names, size=(40,10), font=("Arial Bold", 14), 
                                     expand_y=True, expand_x=True, enable_events=True, 
                                     key="-PROJECT_SELECT-")

        layout = [[sg.Text(getText("pjlist_txt_pjcts"))],
                  [recent_projects],
                  [sg.Button(getText("pjlist_btn_load"), key="-LOAD-", disabled=True), 
                   sg.Push(),
                   sg.Button("Import Project", key="-IMPORT-"), 
                   sg.Push(), 
                   sg.Button(getText("pjlist_btn_del"), button_color=("white","firebrick3"), disabled=True, key="-DEL-")]]
                
        load_win = sg.Window(getText("pjlist_win_title"), layout, finalize=True)

        # Add the ability to double-click an element
        load_win["-PROJECT_SELECT-"].bind('<Double-Button-1>' , "+-double click-")

        return load_win, recent_projects




    def make_browse_import_project(self):
        import_project_path = [
            [sg.Text(getText("import_txt_instr"))],
            [sg.In(size=(25,1), enable_events= True, key="-BROWSE_INPUT-"),
            sg.FileBrowse(file_types=(("Pickle Files", "*.pkl"),))],
            [sg.Button(getText("import"), key="-IMPORT-", disabled=True), sg.Push(), sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
        
        browse_project_import_window = sg.Window(getText("import_txt_title"),
                                                 [import_project_path])
        
        return browse_project_import_window

                                




    def make_comment_window(self, current_comment):
        edit_comment_layout = [
                    [sg.Text(getText("meas_txt_editCmnt"))],
                    [sg.Multiline(size=(45,5), default_text=current_comment, enable_events= True, key="-COMMENT-", expand_x=True)],
                    [sg.Button(getText("continue_btn"), key="-OK-"), sg.Push(), sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
        
        # create marker input window
        comment_input_window = sg.Window(getText("meas_txt_comment"), edit_comment_layout)
        
        return comment_input_window




    def make_project_properties_window(self, project):
        # GPS location
        latitude = project.latitude
        longitude = project.longitude
        altitude = project.altitude

        gps_location_layout = [
            [sg.Text(getText("props_txt_GPS"), font=["Arial", 11, "bold"])],
            [sg.Text(getText("props_txt_GPSinst"))],
            [sg.Text(getText("props_txt_latitude")), 
             sg.In(size=(25,1), default_text=latitude, enable_events=True, key="-LAT-", tooltip="")],
            [sg.Text(getText("props_txt_longitude")), 
             sg.In(size=(25,1), default_text=longitude, enable_events=True, key="-LONG-", tooltip="")],
            [sg.Text(getText("props_txt_altitude")), 
             sg.In(size=(25,1), default_text=altitude, enable_events=True, key="-ALT-", tooltip="")], 
            [sg.HSeparator()], [sg.HSeparator()]]

        # drone displacement limit
        limit = str(project.limit * 1000) # transform from m to mm

        shift_limit_layout = [
            [sg.Text(getText("props_txt_limit"), font=["Arial", 11, "bold"])],
            [sg.Text(getText("props_txt_limitInst"))],
            [sg.Text(getText("setup_max_shift")), 
             sg.In(size=(25,1), default_text=limit, enable_events=True, key="-LIMIT-", tooltip="")]]
        
        buttons_layout = [
            sg.Button(getText("continue_btn"), key="-CONTINUE-"), sg.Button(getText("cancel_btn"), key="-CANCEL-")
        ]


        # create marker input window
        project_property_window = sg.Window(getText("pprops_win_title"), [gps_location_layout, 
                                                                 shift_limit_layout,
                                                                 buttons_layout])
        
        return project_property_window
        



    def make_manual_measurement_properties_window(self, measurement):
        # measurement temperature and weahter conditions
        temperature = measurement.temperature

        # separation of images and radio
        sep_images = 1
        sep_radio = 2
        
        weather_layout = [
            [sg.Text(getText("weather_win_title"), font=["Arial", 11, "bold"])],
            [sg.Text(getText("props_txt_weatherInst"))],
            [sg.Text(getText("props_txt_temperature")),
             sg.In(size=(25,1), default_text=temperature, enable_events=True, key="-TEMP-", tooltip="")],
            [sg.HSeparator()], [sg.HSeparator()],
            [sg.Text(getText("meas_txt_temp")[:-1], font=["Arial", 11, "bold"])],
            [sg.Text(getText("weather_txt_instrW"))],
            [sg.Text("", size=(sep_images,1)), sg.Image("imgs/sunny.png"), 
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/partly_cloudy.png"),
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/cloudy.png"), 
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/foggy.png"),
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/rainy.png"), 
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/snowy.png")],
            [sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::sunny", enable_events=True), 
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::partly_cloudy", enable_events=True), 
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::cloudy", enable_events=True),
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::foggy", enable_events=True),
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::rainy", enable_events=True),
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::snowy", enable_events=True),
            sg.Text("", size=(sep_radio,1))],
            ]    

        values_layout = [
            [sg.HSeparator()], [sg.HSeparator()],
            [sg.Text(getText("meas_txt_val")[:-1], font=["Arial", 11, "bold"])],
            [sg.Text(getText("meas_new_val"))],
            [sg.Text("Marker", size=(10,1)), sg.Text(getText("meas_txt_dist"), size=(20,1))],
        ]    

        for target_point in measurement.target_points:
            values_layout.append(
                [sg.Text(target_point.name, size=(10,1)), 
                 sg.In(size=(10,1), default_text=str(target_point.measured_distance*1000), 
                       enable_events=True, key=("-NEW_VALUE-", target_point.name),
                       tooltip=""),
                 sg.Text("mm")]

            )

        buttons_layout = [
            sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True), sg.Button(getText("cancel_btn"), key="-CANCEL-")
        ]


        # create marker input window
        manual_measurement_property_window = sg.Window(getText("mprops_win_title"), 
                                                [weather_layout,
                                                 values_layout,
                                                 buttons_layout])
        
        return manual_measurement_property_window




    def make_drone_measurement_properties_window(self, measurement):
        # measurement temperature and weahter conditions
        temperature = measurement.temperature

        # separation of images and radio
        sep_images = 1
        sep_radio = 2
        
        weather_layout = [
            [sg.Text(getText("weather_win_title"), font=["Arial", 11, "bold"])],
            [sg.Text(getText("props_txt_weatherInst"))],
            [sg.Text(getText("props_txt_temperature")),
             sg.In(size=(25,1), default_text=temperature, enable_events=True, key="-TEMP-", tooltip="")],
            [sg.HSeparator()], [sg.HSeparator()],
            [sg.Text(getText("meas_txt_temp")[:-1], font=["Arial", 11, "bold"])],
            [sg.Text(getText("weather_txt_instrW"))],
            [sg.Text("", size=(sep_images,1)), sg.Image("imgs/sunny.png"), 
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/partly_cloudy.png"),
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/cloudy.png"), 
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/foggy.png"),
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/rainy.png"), 
            sg.Text("", size=(sep_images,1)), sg.Image("imgs/snowy.png")],
            [sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::sunny", enable_events=True), 
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::partly_cloudy", enable_events=True), 
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::cloudy", enable_events=True),
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::foggy", enable_events=True),
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::rainy", enable_events=True),
            sg.Text("", size=(sep_radio,1)), sg.Radio("", group_id=1, key="weather::snowy", enable_events=True),
            sg.Text("", size=(sep_radio,1))],
            ]    


        buttons_layout = [
            sg.Button(getText("continue_btn"), key="-CONTINUE-", disabled=True), sg.Button(getText("cancel_btn"), key="-CANCEL-")
        ]


        # create marker input window
        drone_measurement_property_window = sg.Window(getText("mprops_win_title"), 
                                                [weather_layout,
                                                 buttons_layout])
        
        return drone_measurement_property_window




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
            [sg.Text(getText("pjct_txt_warnremove"), font=("Arial", 12), text_color="black")],
            [sg.Text(related_str, font=("Arial", 12, "bold"), text_color="black")],
            [sg.Text(not_related_str, font=("Arial", 12), text_color="black")],
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
    def make_missing_marker_warning(cls, missing_ref_markers, missing_target_markers):
        # change window layout
        sg.theme("DarkRed1")

        ref_str = ""
        tar_str = ""

        if missing_ref_markers:
            for ref in missing_ref_markers:
                ref_str = ref_str + "-  " + str(ref) + "\n"

        if missing_target_markers:
            for tar in missing_target_markers:
                tar_str = tar_str + "-  " + str(tar) + "\n"


        output_str = (getText("pjct_txt_missMarkr") + "\n" + 
                      getText("pjct_txt_missRef") + "\n" + ref_str + "\n" +
                      getText("pjct_txt_missTar") + "\n" + tar_str + "\n" +
                      getText("pjct_txt_instruct"))
        

        warning_layout = [
            [sg.Text(output_str, font=("Arial", 12), text_color="black")],
            [sg.Button(getText("continue_btn"), key="-OK-")]]
        
        warn_window = sg.Window(getText("warn_btn"), warning_layout, keep_on_top=True, finalize=True)

        # change theme back to original for subsequent windows
        sg.theme(cls.theme)

        return warn_window




    @classmethod
    def popup_window(cls, text_ID):

        popup_layout = [
            [sg.Text(getText(text_ID), font=("Arial", 12), text_color="black")]]
        
        popup_window = sg.Window("", popup_layout, keep_on_top=True, finalize=True)

        return popup_window




    @classmethod
    def warning_window(cls, warning_str):
        
        # change window layout
        sg.theme("DarkRed1")

        warning_layout = [
            [sg.Text(warning_str, font=("Arial", 12), text_color="black")],
            [sg.Button(getText("acknowl_btn"), key="-ACKNOWLEDGE-"), sg.Push(), sg.Button(getText("cancel_btn"), key="-CANCEL-")]]
        
        warn_window = sg.Window(getText("warn_btn"), warning_layout, finalize=True)

        # change theme back to original for subsequent windows
        sg.theme(cls.theme)

        return warn_window



    @classmethod    
    def non_blocking_popup(cls, ID, colorTheme, location):

        p1 = location[0]
        p2 = location[1] - 100
        location = (p1, p2)
        sg.theme(colorTheme)
        pop_window = sg.popup_non_blocking(getText(ID), no_titlebar=True, 
                                           auto_close=True, location=location,
                                           auto_close_duration=4.5, 
                                           keep_on_top=True)
        sg.theme(cls.theme)
        return pop_window









def Btn_10(*args, button_color=('white', 'black'), **kwargs):
    return(sg.Button(*args, font='Arial 10',button_color=button_color, **kwargs))


def Txt_10(*args, **kwargs):
    return(sg.Text(*args, font=("Arial Bold", 10), **kwargs))


def getText(ID):
        return helpers.readout.gettext(ID)
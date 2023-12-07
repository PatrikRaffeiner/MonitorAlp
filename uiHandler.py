import PySimpleGUI as sg



class UIhandler():
    def handle_project_setup(self, project_setup_window):

        # link buttons to events
        proceed = project_setup_window["Continue"]
        
        # initiate listener flags with "low"
        loc_flag = False
        exe_flag = False
        licence_flag = False


        # event loop project setup input
        while True:
            event, values = project_setup_window.read()
            # end if window is closed or cancel is pressed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                project_setup_window.close()
                break
            
            # event listener for project name/location
            if event == "-LOC-":
                location = values["-LOC-"]
                loc_flag = True

            # event listener for RC execution path
            if event == "-EXE-":
                RC_path = values["-EXE-"]
                exe_flag = True

            # event listener for permanent licence checkbox
            if event == "-CHECK-":
                licence_flag = values["-CHECK-"]

            # enable "Continue" button when project name/location and RC execution path is entered
            if loc_flag and exe_flag:
                proceed.update(disabled = False)

            # continue when project name and RC exe is defined and store attributes 
            if event == "Continue":
                project_setup_window.close()

                name = location

                # set project members from UI
                return location, RC_path, licence_flag, name




    def get_img_and_pjct_dir(self, measurement_setup_window):
    
        accept = measurement_setup_window['Accept']

        # set listener flags to low
        project_flag = False
        image_flag = False


        # event loop measurement setup
        while True:
            event, values = measurement_setup_window.read()
            # End if window is closed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                measurement_setup_window.close()
                break
            
            if event == "-IMGFOLDER-":
                imgfolder = values["-IMGFOLDER-"]
                image_flag = True

            if event == "-PRJFOLDER-":
                pjctfolder = values["-PRJFOLDER-"]
                project_flag = True
            
            if image_flag and project_flag:
                accept.update(disabled =False)

            if event == "Accept":
                measurement_setup_window.close()
                print(imgfolder)
                print(pjctfolder)
                
                return imgfolder, pjctfolder
            


    def get_licence_pin(self, licence_browse_window):

        accept = licence_browse_window['Accept']
        pay = licence_browse_window["Pay"]
        cont = licence_browse_window["Continue"]

        # event loop licence browse
        while True:
            event, values = licence_browse_window.read()
            # End if window is closed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                licence_browse_window.close()
                break
            
            if values["-CHECK-"] == True:
                cont.update(disabled = False)

            if event == "Continue":
                licence_browse_window.close()
                break

            if event == "-FILE-":
                folder = values["-FILE-"]
                accept.update(disabled = False)
            
            if event == "-PIN-":
                pin = values["-PIN-"]
                pay.update(disabled = False )

            if event == "Accept":
                licence_browse_window.close()
                return folder
            
            if event == "Pay":
                licence_browse_window.close()
                return pin
            


    def get_marker_names(self, marker_input_window):

        okay = marker_input_window["OK"]

        # set listener flags to low
        # reference system/markers
        orig_flag = False
        horiz_falg = False
        vert_flag = False

        targetA_flag = False
        targetB_flag = False
        targetC_flag = False

        targetA = None
        targetB = None 
        targetC = None


        # event loop marker input
        while True:
            event, values = marker_input_window.read()
            # End if window is closed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                marker_input_window.close()
                break

            # reference marker
            if event == "-ORIG-":
                origin_marker = values["-ORIG-"]
                orig_flag = True

            if event == "-HORIZ-":
                horizontal_marker = values["-HORIZ-"]
                horiz_falg = True

            if  event == "-VERT-":
                vertical_marker = values["-VERT-"]
                vert_flag = True

            # target marker
            if event == "-A-":
                targetA = values["-A-"]
                targetA_flag = True

            if event == "-B-":
                targetB = values["-B-"]
                targetB_flag = True

            if event == "-C-":
                targetC = values["-C-"]
                targetC_flag = True

            # get user input on refence distance, otherwise take default
            if event == "-DIST-":
                ref_distance = values["-DIST-"]



            if orig_flag and horiz_falg and vert_flag and targetA_flag:
                okay.update(disabled =False)

            if event == "OK":
                marker_input_window.close()
                targets = []
                for target in [targetA, targetB, targetC]:
                    if target is not None: 
                        targets.append(target)

                ref_distance = float(ref_distance)
                ref_distance /= 1000                # transform into meters
                ref_distance = str(ref_distance)    # transform to string 
                    
                return [origin_marker, horizontal_marker, vertical_marker], targets, ref_distance




    def select_from_project_list(self, load_window, recent_projects, project_list):
        load_btn = load_window["-LOAD-"]

        while True:
            event, values = load_window.read()

                   # End if window is closed
            if event == sg.WIN_CLOSED:
                load_window.close()
                return False
    
                    
            if event == "-SELECT-":
                # gets the selected element from the recent project list
                project_name = recent_projects.get()[0]
                load_btn.update(disabled=False)                      


            if event == "-LOAD-":
                # find project in project list based on selected name
                selected_project = next((p for p in project_list if p.name == project_name), None)
                load_window.close()
                return selected_project
                 


    def handle_measurement_overview(self, overview_window, select_lst, project, project_list):
        
        calc_btn = overview_window["-CALC-"]
        remove_btn = overview_window["-DEL-"]

        while True:
            event, values = overview_window.read()
            #print(values)
            
            # End if window is closed
            if event == sg.WIN_CLOSED:
                overview_window.close()
                break

            # show attributes of selected element/measurement
            if event ==  "-SELECT-": 
                # get name of selected item/measurement
                meas_name = select_lst.get()[0]
                                
                # find object with measurement name and return object
                selected_measurement = next((m for m in project.measurement_list if m.name == meas_name), None)
                overview_window["-OUTPUT-"].update(["location:", selected_measurement.location, "", 
                                           "date & time:", selected_measurement.date, selected_measurement.time, "",
                                           "reference marker:", selected_measurement.ref_marker_names[0], 
                                           selected_measurement.ref_marker_names[1], 
                                           selected_measurement.ref_marker_names[2],"", 
                                           "target marker:", selected_measurement.target_marker_names[0], 
                                           selected_measurement.target_marker_names[1],
                                           selected_measurement.target_marker_names[2],""])
                
                # enable diaplacement calculation button when selected measurement is not initial measurement 
                if selected_measurement != project.measurement_list[0]:
                    calc_btn.update(disabled = False)
                    remove_btn.update(disabled = True)

                    # continue here...
                    # was passiert wenn initiale messung gelöscht wird? 
                
                else: 
                    calc_btn.update(disabled = True)
                    


            if event == "-ADD-":
                new_measurement = project.create_measurement()
                project.RC_registration_and_save_points(new_measurement)
                new_measurement.transform_points()
                new_measurement.sort_points()
                project.add_to_measurement_list(new_measurement)

                new_measurement.visualize_points()
                new_measurement.save()
                project.save()
                #project_list.append(project)
                project_list.save()

                measurement_names = project.get_measurement_names()
                overview_window["-SELECT-"].update(measurement_names)


            if event == "-CALC-":
                project.calc_displacement(selected_measurement)
                project.visualize_displacement(selected_measurement)


            if event == "-DEL":
                # TODO: add warning and prompt
                # if prompt: ....
                project.remove_from_project_list(selected_measurement)








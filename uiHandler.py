import PySimpleGUI as sg
import os
from copy import deepcopy
import shutil
import re
import subprocess

# local imports
from gui import *
from exceptions import*


class UIhandler():
    def handle_project_setup(self, project_setup_window, master_obj):

        project_list = master_obj.project_list

        # link buttons to events
        proceed = project_setup_window["-CONTINUE-"]
        
        # initiate listener flags with "low"
        loc_flag = False
        licence_flag = False
        limit_flag = False

        # handle possible existing RealityCapture execution directory 
        if master_obj.RC_dir != None:
            exe_flag = True
            RC_path = master_obj.RC_dir
        else:
            exe_flag = False

        # event loop project setup input
        while True:
            event, values = project_setup_window.read()
            # end if window is closed or cancel is pressed
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                project_setup_window.close()
                raise ClosedWindow("Project setup window closed")
            
            # event listener for project name/location
            if event == "-LOC-":
                location = values["-LOC-"]

                if self.inspect_project_name(location, project_list):
                    loc_flag =  False
                    self.dye_background("red", project_setup_window["-LOC-"])
                    self.create_popup_above("setup_tip_wrongName", project_setup_window, "-LOC-")

                else: 
                    loc_flag = True
                    self.dye_background("white", project_setup_window["-LOC-"])


            # event listener for RC execution path
            if event == "-EXE-":
                RC_input = values["-EXE-"]

                exe_flag = self.handle_execution_input(RC_input, project_setup_window)  
                RC_path = RC_input

            # event listener for shift limit
            if event == "-LIMIT-":
                limit_input = values["-LIMIT-"]

                # inspects distance input and highlights input window when incorrect input is provided
                # also highlights the background (red) if wrong format is provided
                limit_flag, limit = self.inspect_distance_input(limit_input, project_setup_window, ('-LIMIT-'))


            # enable "Continue" button when project name/location and RC execution path is entered
            if loc_flag and exe_flag and limit_flag:
                proceed.update(disabled = False)
            
            else:
                proceed.update(disabled = True)

            # continue when project name and RC exe is defined and store attributes 
            if event == "-CONTINUE-":
                project_setup_window.close()

                name = location

                # set project members from UI
                return location, RC_path, licence_flag, name, limit




    def inspect_project_name(self, current_name, project_list):
        for project in project_list:
            if project.name == current_name:
                return True
            
        return False




    def handle_execution_input(self, RC_input, project_setup_window):
        tip_wrong_exe = getText("pjct_tip_wrongRC")
        
        # correct path to RealityCapture execution
        if RC_input.endswith("RealityCapture.exe"):
            exe_flag = True
            # highlight input line 
            project_setup_window["-EXE-"].update(background_color="white")

            # update tooltip with warning and correct format suggestion
            project_setup_window["-EXE-"].TooltipObject.text = ""

            return exe_flag

        else:
            exe_flag = False
        
            # highlight input line 
            project_setup_window["-EXE-"].update(background_color="red")

            # update tooltip with warning and correct format suggestion
            project_setup_window["-EXE-"].TooltipObject.text = tip_wrong_exe

            return exe_flag




    def get_img_and_pjct_dir(self, measurement_setup_window, gui, project_name):
    
        accept = measurement_setup_window["-CONTINUE-"]

        # set listener flags to low
        project_flag = False
        image_flag = False


        # event loop measurement setup
        while True:
            event, values = measurement_setup_window.read()
            # End if window is closed
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                measurement_setup_window.close()
                print("measurement setup window closed")

                # raise exception to catch closed window
                raise ClosedWindow("Measurement setup window closed")

            
            if event == "-IMGFOLDER-":
                imgfolder = values["-IMGFOLDER-"]
                
                if self.inspect_img_folder(imgfolder):
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="white")
                    image_flag = True
                
                else:
                    self.dye_background("red", measurement_setup_window["-IMGFOLDER-"])
                    self.create_popup_above("init_pop_img", measurement_setup_window, "-IMGFOLDER-")
                    image_flag = False

            if event == "-PRJFOLDER-":
                pjctfolder = values["-PRJFOLDER-"]

                if self.inspect_project_folder(pjctfolder, project_name):
                    measurement_setup_window["-PRJFOLDER-"].update(background_color="white")
                    project_flag = True

                # handle existing project name in provided project folder 
                else:
                    project_flag = False
                    
                    # dye input line background red
                    measurement_setup_window["-PRJFOLDER-"].update(background_color="red")
                    
                    # create non-blocking pop up window with explanation
                    loc = measurement_setup_window.CurrentLocation()
                    gui.non_blocking_popup("init_pop_projcet", loc, "DarkRed1")
                    measurement_setup_window.force_focus()
                    measurement_setup_window["-IMGFOLDER-"].SetFocus()

            
            if image_flag and project_flag:
                accept.update(disabled =False)

            if event == "-CONTINUE-":
                measurement_setup_window.close()                
                return imgfolder, pjctfolder
            



    def get_img_dir(self, measurement_setup_window, gui):
    
        accept = measurement_setup_window["-CONTINUE-"]


        # event loop measurement setup
        while True:
            event, values = measurement_setup_window.read()
            # End if window is closed
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                measurement_setup_window.close()
                # raise exception to catch closed window
                raise ClosedWindow("Measurement setup window closed")
            
            if event == "-IMGFOLDER-":
                imgfolder = values["-IMGFOLDER-"]
                
                if self.inspect_img_folder(imgfolder):
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="white")
                    accept.update(disabled =False)                   
                
                else:
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="red")
                    loc = measurement_setup_window.CurrentLocation()
                    gui.non_blocking_popup("init_pop_img", loc, "DarkRed1")
                    measurement_setup_window.force_focus()
                    measurement_setup_window["-IMGFOLDER-"].SetFocus()
                    #threading.Thread(target=wait, args=(2, popup_win), daemon=True).start()


            if event == "-CONTINUE-":
                measurement_setup_window.close()                
                return imgfolder
            



    def get_manual_measurement_distances(self, manual_measurement_window, project, droneMeasurement_dir):

        accept = manual_measurement_window["-CONTINUE-"]

        # dictionary for manual measurements
        manual_measurement_dict = {}


        # event loop measurement setup
        while True:
            event, values = manual_measurement_window.read()

            # End if window is closed
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                manual_measurement_window.close()

                # delete dir
                shutil.rmtree(droneMeasurement_dir)
                raise ClosedWindow("Manual measurement input window closed")    
                
            
            # listener for every target marker, including added targets
            if event[0] == "-TARGET-":
                target = {}

                # gets value from current input event (input of distinct target)
                input_value = values[('-TARGET-', event[1])]

                # inspects distance input and highlights input window when incorrect input is provided
                # also highlights the background (red) if wrong format is provided
                dist_flag, input_distance = self.inspect_distance_input(input_value, manual_measurement_window, ('-TARGET-', event[1]))
                if dist_flag: 
                    # correct input format provided, sets possible red background to white and stores value
                    target[event[1]] = input_distance   # in meters
                    manual_measurement_dict.update(target)

                else: 
                    # wrong input provided, set background to red and with instructions
                    manual_measurement_window.force_focus()
                    manual_measurement_window[('-TARGET-', event[1])].SetFocus()


            if len(manual_measurement_dict) == len(project.target_list.labels):
                accept.update(disabled = False)

            if event == "-CONTINUE-":
                return manual_measurement_dict  # distance values in meters




    def get_weather_conditions(self, weather_info_window):
        # flags
        temp_flag = False
        weather_flag = False

        while True: 
            event, values = weather_info_window.read()

            # End if window is closed
            if event == sg.WIN_CLOSED or event == "-CANCEL-":
                weather_info_window.close()
                break

            if event == "-TEMP-":
                if self.inspect_temperature(values["-TEMP-"], weather_info_window, "-TEMP-"):
                    temp_flag = True
                    temperature = values["-TEMP-"]

                else: 
                    temp_flag = False

            if "weather" in event:
                weather_flag= True

                split = event.split("::")
                weather_conditions = split[-1]

            if temp_flag and weather_flag:
                weather_info_window["-CONTINUE-"].update(disabled=False)

            if event == "-CONTINUE-":
                weather_info_window.close()
                
                return weather_conditions, temperature




    def inspect_img_folder(self, folder_dir):
        try:
            file_list = os.listdir(folder_dir)
            extensions = [".JPG", ".jpg", ".jpeg", ".png", ".tiff", ".tif",
                        ".exr", ".webp", ".bmp", ".dng", ".raw"]
            for file in file_list:
                if file.endswith(tuple(extensions)):
                    return True
        
            return False

        except:
            return False




    def inspect_project_folder(self, folder_dir, project_name):
        
        folder_list = os.listdir(folder_dir)

        if not folder_list: 
            return True     # empty folder structure
        
        for folder in folder_list:
                if folder.startswith(project_name):
                    return False    # folder with same name is already existing
            
        return True     # no folder with same name existing 




    def get_licence_pin(self, licence_browse_window):

        accept = licence_browse_window['-CONTINUE-']
        pay = licence_browse_window["-PAY_BTN-"]
        cont = licence_browse_window["-CONTINUE-"]

        # event loop licence browse
        while True:
            event, values = licence_browse_window.read()
            # End if window is closed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                licence_browse_window.close()
                break
            
            if values["-CHECK-"] == True:
                cont.update(disabled = False)

            if event == "-CONTINUE-":
                licence_browse_window.close()
                break

            if event == "-FILE-":
                folder = values["-FILE-"]
                accept.update(disabled = False)
            
            if event == "-PIN_INPUT-":
                pin = values["-PIN_INPUT-"]
                pay.update(disabled = False )

            if event == "Accept":
                licence_browse_window.close()
                return folder
            
            if event == "-PAY_BTN-":
                licence_browse_window.close()
                return pin
            



    def get_marker_names(self, gui, marker_input_window, project_target_list):

        okay = marker_input_window["-CONTINUE-"]

        # event loop marker input
        while True:
            event, values = marker_input_window.read()

            # End if window is closed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                marker_input_window.close()
                raise ClosedWindow("Measurement setup window closed")

            # add additional target marker
            if event == "-ADD-":
                marker_input_window.metadata += 1
                marker_input_window.extend_layout(marker_input_window['-TARGET SECTION-'], 
                                                  [gui.marker_row(project_target_list,marker_input_window.metadata)])
                
                # add empty elements to edit via input
                project_target_list.attr.append([True, None])   # [visible, label]
                print(f"dict {project_target_list.attr}")


            if event[0] == "-DELETE-":
                # at least one target name must be entered
                if len(project_target_list.attr) > 1:
                    # make clicked element invisible
                    marker_input_window[("-ROW-", event[1])].update(visible=False)
                    
                    # set "visibility" of target element to false
                    project_target_list.attr[event[1]][0] = False


            # listener for every target marker, including added targets
            if event[0] == "-TARGET-":
                target_marker = values[("-TARGET-", event[1])] 

                # check if target name has correct input format, then store name in target list
                if self.inspect_marke_name(marker_input_window, target_marker, ("-TARGET-", event[1])):
                    project_target_list.attr[event[1]][1] = target_marker
                else: 
                    project_target_list.attr[event[1]][1] = None

                

            # check if all visible targets are named correctly
            if any(target[0] is True and target[1] is None for target in project_target_list.attr):
                okay.update(disabled =True)
            else:
                okay.update(disabled=False)

            if event == "-CONTINUE-":
                marker_input_window.close()
                project_target_list.labels = []

                for target in project_target_list.attr:
                    if target[0] and target[1] is not None:
                        project_target_list.labels.append(target[1])
              
                return project_target_list.labels



    def inspect_marke_name(self, marker_input_window, marker_name, marker_key):
        # check for correct input of marker name
        match = re.match("^1x12:0[0-9]{2}$|1x12:0[0-9][a-z]$", marker_name)

        # tooltip for wrong marker name format
        tip_name = getText("mrk_tip_name")

        # correct input marker
        if match: 
            # clear possible red background color of input line and remove tooltip
            marker_input_window[marker_key].update(background_color="white")
            marker_input_window[marker_key].TooltipObject.text = ""

            marker_name_flag = True

        else: 
            # highlight background of input line red 
            marker_input_window[marker_key].update(background_color="red")
            marker_input_window[marker_key].TooltipObject.text = tip_name

            marker_name_flag = False
  
        return marker_name_flag

            


    def inspect_distance_input(self, input, input_window, args): 

        # transforms possible input with a comma decimal separator 
        # to a dot decimal separator format
        dot_input = input.replace(",",".")       

        # checks if input matches the correct format
        # [1-4 integers] [.] [1-2 integers]
        match = re.match("^[0-9]{1,4}[.][0-9]{1,2}$", dot_input)

        # correct input format 
        if match:
            # clear the input line and set distance flag
            input_window[args].update(background_color="white")

            # clear tooltip
            input_window[args].TooltipObject.text = ""

            distance_flag = True

            float_input = float(dot_input)

            # transform from mm to m
            m_input = float_input / 1000

            return distance_flag, m_input
        

        else:
            # highlight input line 
            input_window[args].update(background_color="red")

            # update tooltip with warning and correct format suggestion
            input_window[args].TooltipObject.text = getText("mrk_tip_wrongdist")
            distance_flag = False

            return distance_flag, None




    def inspect_lat_long_alt(self, input, input_window, args):
        # transforms possible input with a comma decimal separator 
        # to a dot decimal separator format
        dot_input = input.replace(",",".")       

        # checks if input matches the correct format
        # [1-4 integers] [.] [1-2 integers]
        match1 = re.match("^[\d]{1,2}[.][\d]{0,14}$", dot_input)
        match2 = re.match("^[-]$", dot_input)

        # correct input format 
        if match1:
            # clear the input line and set distance flag
            input_window[args].update(background_color="white")
            input_flag = True
            float_input = float(dot_input)

            meter_input = float_input / 1000 # transform mm input to m

            return input_flag, meter_input


        if match2: 
            # clear the input line and set distance flag
            input_window[args].update(background_color="white")
            input_flag = True
            hyphen = dot_input

            return input_flag, hyphen


        else:
            # highlight input line 
            input_window[args].update(background_color="red")
            input_flag = False

            return input_flag, None




    def inspect_temperature(self, input, input_window, args):
        match1 = re.match("^[\d]{1,2}$", input)
        match2 = re.match("^[-][\d]{1,2}$", input)

        if match1 or match2: 
            # clear the input line and set distance flag
            input_window[args].update(background_color="white")
            input_flag = True

            return input_flag
        
        else:
            # highlight input line 
            input_window[args].update(background_color="red")
            input_flag = False

            return input_flag




    def select_from_project_list(self, load_window, recent_projects, project_list, master_obj):
        load_btn = load_window["-LOAD-"]
        delete_btn = load_window["-DEL-"]

        while True:
            event, values = load_window.read()

            # End if window is closed
            if event == sg.WIN_CLOSED:
                load_window.close()
                return False
    
                    
            if event == "-PROJECT_SELECT-":
                # gets the selected element from the recent project list
                project_name = recent_projects.get()[0]
                load_btn.update(disabled=False)  
                delete_btn.update(disabled=False)                    


            if event == "-LOAD-":
                # find project in project list based on selected name
                selected_project = next((p for p in project_list if p.name == project_name), None)
                load_window.close()

                return selected_project
            
            if event == "-DEL-":
                # find project in project list based on selected name
                selected_project = next((p for p in project_list if p.name == project_name), None)

                warn_window = GUI.warning_window(getText("meas_del_warn"))

                while True:
                    event, values = warn_window.read()
            
                    # End if window is closed
                    if event == sg.WIN_CLOSED:
                        warn_window.close()

                        # closes "old" load window, new one is invoked 
                        # through load_window.read() in while above
                        load_window.close()
                        return

                    if event == "-ACKNOWLEDGE-":
                        warn_window.close()
                        if selected_project.delete_directory():
                            project_list.remove_project(selected_project)

                            # close old window
                            load_window.close()

                            master_obj.save()

                            return

                    if event == "-CANCEL-":
                        warn_window.close()
                        load_window.close()
                        return
                
            
            if event == "-PROJECT_SELECT-+-double click-":
                # find project in project list based on double clicked element 
                project_name = values["-PROJECT_SELECT-"][0]
                selected_project = next((p for p in project_list if p.name == project_name), None)
                load_window.close()
                return selected_project

                


    def handle_measurement_overview(self, overview_window, select_lst, 
                                    manual_lst, project, master_obj, menu_list):
        
        # initaially set "show location in map"
        if not project.GPS_available:
            menu_elements = deepcopy(overview_window["-MENU-"].MenuDefinition)
            menu_elements[0][1][3] = "!" + menu_elements[0][1][3]
            
            # update layout to enforce recent changes
            overview_window["-MENU-"].update(menu_definition = menu_elements)


        while True:
            event, values = overview_window.read()
            
            # End if window is closed
            if event == sg.WIN_CLOSED:
                overview_window.close()
                break


            # show attributes of selected element/measurement
            if event ==  "-DRONE_SELECT-": 
                selected_measurement = self.get_selected_measurement(select_lst, project)

                # unselect measurement from other (manual) list
                overview_window["-MANUAL_SELECT-"].update(set_to_index=[])

                # visualize drone measurement info in output list
                selected_measurement.show_measurement_info(overview_window)

                menu_elements = deepcopy(overview_window["-MENU-"].MenuDefinition)


                # disabling all menu elements of the manual measurement except adding a manual measurement
                for i in range(1, len(menu_elements[2][1])):
                    if not menu_elements[2][1][i].startswith("!"):
                        menu_elements[2][1][i] = "!" + menu_elements[2][1][i]

                # make sure striplines are visible
                menu_elements[2][1][-2] = menu_elements[2][1][-2].replace("!", "")
                menu_elements[1][1][-2] = menu_elements[1][1][-2].replace("!", "")
                

                # enabling all drone menu elements 
                for i in range(0, len(menu_elements[1][1])):
                    menu_elements[1][1][i] = menu_elements[1][1][i].replace("!", "")  


                # disable menu elements that do not work for initial measurement
                if selected_measurement == project.drone_measurement_list[0]:
                    menu_elements[1][1][1] = "!" + menu_elements[1][1][1]   # disable show displacement
                    menu_elements[1][1][-1] = "!" + menu_elements[1][1][-1] # disable delete measurement

                overview_window["-MENU-"].update(menu_definition = menu_elements)



            if event == "-MANUAL_SELECT-":
                selected_measurement = self.get_selected_measurement(manual_lst, project)

                # unselect measurement from other (drone) list
                overview_window["-DRONE_SELECT-"].update(set_to_index=[])

                # visualize manual measurement info in output list
                selected_measurement.show_measurement_info(overview_window)

                menu_elements = deepcopy(overview_window["-MENU-"].MenuDefinition)
                
                # disabling all menu elements of the drone measurement except adding a drone measurement
                for i in range(1, len(menu_elements[1][1])):
                    if not menu_elements[1][1][i].startswith("!"):
                        menu_elements[1][1][i] = "!" + menu_elements[1][1][i]

                # make sure striplines are visible
                menu_elements[2][1][-2] = menu_elements[2][1][-2].replace("!", "")
                menu_elements[1][1][-2] = menu_elements[1][1][-2].replace("!", "")


                # enable all menu elements of the manual measurement
                for i in range(0, len(menu_elements[2][1])):
                    menu_elements[2][1][i] = menu_elements[2][1][i].replace("!", "")  

                    
                # disable "delete manual measurement" when selected measurement is initial measurement 
                if selected_measurement == project.manual_measurement_list[0]:
                    menu_elements[2][1][-1] = "!" + menu_elements[2][1][-1]
                    
                    '''# set tooltips of drone and manual measurement delete button
                    overview_window["-DEL_MANUAL-"].TooltipObject.text = getText("meas_tip_nodel") # "cannot delete init measurement"
                    overview_window["-DEL_DRONE-"].TooltipObject.text = getText("meas_tip_del")  # "Please select the measurement to delete"

                
                else:                   
                    # set tooltips of drone and manual measurement delete button
                    overview_window["-DEL_MANUAL-"].TooltipObject.text = getText("meas_tip_delInfo")  # "Removes selected measurement irreversibly"
                    overview_window["-DEL_DRONE-"].TooltipObject.text = getText("meas_tip_del")     # "Please select the measurement to delete"  
                '''
                # update layout to enforce recent changes
                overview_window["-MENU-"].update(menu_definition = menu_elements)



            if "addDrone" in event:
                
                # in case reality capture crashed due to any circumstances
                # directory is completle removed 
                try:
                    drone_measurement = project.create_drone_measurement(init_status=False)
                    project.RC_registration_and_export_points(drone_measurement, master_obj.RC_dir)
 
                    drone_measurement.transform_points()
                
                except ClosedWindow:
                    # catch exception due to closed window
                    continue

                except:
                    # catch any other exception apart due to closed windows 
                    # abort process and delete the directory 
                    drone_measurement.delete_directory()
                    print("deleting: " + drone_measurement.dir + " because something went wrong in RC")
                    continue
                
                drone_measurement.sort_points()
                project.drone_measurement_list.append(drone_measurement)
                project.all_measurement_list.append(drone_measurement)

                project.calc_displacement(drone_measurement)
                project.calc_distance_to_origin(drone_measurement)
                project.calc_accuracy_indicator(drone_measurement)
                
                drone_measurement.check_limits()                

                drone_measurement.visualize_points()
                drone_measurement.save()
                project.save()
                master_obj.save()

                # updating the reports
                project.dump_xlsx_file()
                project.dump_pdf()

                drone_measurement_names =  [m.name for m in project.drone_measurement_list]
                overview_window["-DRONE_SELECT-"].update(drone_measurement_names)
                
                overview_window.force_focus()

                # popup "successfully added measurement"
                project.confirm_added_saved_element("pdf_pop_meas_added")



            if "addManual" in event:
                try: 
                    manual_measurement = project.create_manual_measurement("dummy_dir")

                    project.calc_displacement(manual_measurement)
                    manual_measurement.check_limits()
                    project.manual_measurement_list.append(manual_measurement)
                    project.all_measurement_list.append(manual_measurement)

                    project.pdf = project.dump_pdf()
                    project.save()
                    master_obj.save()

                    # updating the reports
                    project.dump_xlsx_file()
                    project.dump_pdf()

                    manual_measurement_names = [m.name for m in project.manual_measurement_list]
                    overview_window["-MANUAL_SELECT-"].update(manual_measurement_names)

                    # popup "successfully added measurement"
                    project.confirm_added_saved_element("pdf_pop_meas_added")
                
                except ClosedWindow:
                    # catch exception due to closed window
                    continue
                
                except Exception as ex: 
                    # catch any other exception apart due to closed windows 
                    print(ex)



            if "displacement" in event:
                # no need to actually calculate the displacement
                # only show the already calculated
                project.plot_displacement(selected_measurement)
                project.visualize_displacement(selected_measurement)



            if "deleteProject" in event: 
                # find project in project list based on selected name
                selected_project = next((p for p in master_obj.project_list if p.name == project.name), None)

                warn_window = GUI.warning_window(getText("meas_del_warn"))

                while True:
                    event, values = warn_window.read()
            
                    # End if window is closed
                    if event == sg.WIN_CLOSED:
                        break

                    if event == "-ACKNOWLEDGE-":
                        warn_window.close()

                        if selected_project.delete_directory():
                            master_obj.project_list.remove_project(selected_project)
                        
                            #load_window["-PROJECT_SELECT-"].update(project_names)

                            master_obj.save()                        
                            return

                    if event == "-CANCEL-":
                        warn_window.close()
                        break
                
                event = "placeholder"
                


            if "deleteDrone" in event:
                # make popup window to check for validity
                warn_window = GUI.warning_window(getText("meas_del_warn"))

                while True:
                    event, values = warn_window.read()
            
                    # End if window is closed
                    if event == sg.WIN_CLOSED:
                        warn_window.close()
                        break

                    if event == "-ACKNOWLEDGE-":
                        selected_measurement.delete_directory()
                        project.drone_measurement_list.remove(selected_measurement)
                        project.all_measurement_list.remove(selected_measurement)

                        drone_measurement_names = [drone_measurement.name for drone_measurement in project.drone_measurement_list]
        
                        overview_window["-DRONE_SELECT-"].update(drone_measurement_names)

                        project.save()
                        master_obj.save()
                        project.dump_xlsx_file()
                        project.dump_pdf()

                        # popup "successfully removed measurement"
                        project.confirm_added_saved_element("pdf_pop_meas_del")

                        warn_window.close()

                    if event == "-CANCEL-":
                        warn_window.close()
                
                
                # disabling all menu elements of the manual measurement except adding a manual measurement
                for i in range(1, len(menu_elements[2][1])):
                    if not menu_elements[2][1][i].startswith("!"):
                        menu_elements[2][1][i] = "!" + menu_elements[2][1][i]


                # disabling all menu elements of the drone measurement except adding a drone measurement
                for i in range(1, len(menu_elements[1][1])):
                    if not menu_elements[1][1][i].startswith("!"):
                        menu_elements[1][1][i] = "!" + menu_elements[1][1][i]

                # make sure striplines are visible
                menu_elements[2][1][-2] = menu_elements[2][1][-2].replace("!", "")
                menu_elements[1][1][-2] = menu_elements[1][1][-2].replace("!", "")

                # update layout to enforce recent changes
                overview_window["-MENU-"].update(menu_definition = menu_elements)

                event = "placeholder"
                        


            if "deleteManual" in event:
                # make popup window to check validity 
                warn_window = GUI.warning_window(getText("meas_del_warn"))

                while True: 
                    event, values = warn_window.read()

                    # End if window is closed
                    if event == sg.WIN_CLOSED:
                        warn_window.close()
                        break

                    if event == "-CANCEL-":
                        warn_window.close()

                    if event == "-ACKNOWLEDGE-":
                        project.manual_measurement_list.remove(selected_measurement)
                        project.all_measurement_list.remove(selected_measurement)

                        manual_measurement_names = [manual_measurement.name for manual_measurement in project.manual_measurement_list]

                        overview_window["-MANUAL_SELECT-"].update(manual_measurement_names)

                        project.save()
                        master_obj.save()
                        project.dump_xlsx_file()
                        project.dump_pdf()

                        # popup "successfully removed measurement"
                        project.confirm_added_saved_element("pdf_pop_meas_del")

                        warn_window.close()

                # disabling all menu elements of the manual measurement except adding a manual measurement
                for i in range(1, len(menu_elements[2][1])):
                    if not menu_elements[2][1][i].startswith("!"):
                        menu_elements[2][1][i] = "!" + menu_elements[2][1][i]


                # disabling all menu elements of the drone measurement except adding a drone measurement
                for i in range(1, len(menu_elements[1][1])):
                    if not menu_elements[1][1][i].startswith("!"):
                        menu_elements[1][1][i] = "!" + menu_elements[1][1][i]

                # make sure striplines are visible
                menu_elements[2][1][-2] = menu_elements[2][1][-2].replace("!", "")
                menu_elements[1][1][-2] = menu_elements[1][1][-2].replace("!", "")

                # update layout to enforce recent changes
                overview_window["-MENU-"].update(menu_definition = menu_elements)

                event = "placeholder"



            if "showMeasurementReport" in event:
                os.startfile(selected_measurement.dir + "/" + selected_measurement.name +".pdf")

                

            if "showProjectReport" in event:
                os.startfile(project.dir + "/" + project.name +".pdf")



            if "commentDrone" in event:
                current_comment = selected_measurement.comment  
                new_comment = current_comment

                gui = GUI()
                comment_win = gui.edit_comment(current_comment)

                while True: 
                    event, values = comment_win.read()

                    # end when window is closed
                    if event == sg.WIN_CLOSED:
                        break

                    if event == "-COMMENT-":
                        new_comment = values["-COMMENT-"]

                    if event == "-CANCEL-":
                        comment_win.close()
                        break

                    if event == "-OK-":
                        selected_measurement.comment = new_comment
                        comment_win.close()
                        master_obj.save()

                        # updating the project report
                        project.dump_pdf() 

                        # popup "successfully added comment"
                        project.confirm_added_saved_element("pdf_pop_cmnt_added")

                        # updating the output column
                        selected_measurement.show_measurement_info(overview_window)
                        break

                event="dummy"


            
            if "commentManual" in event:
                current_comment = selected_measurement.comment  
                new_comment = current_comment

                gui = GUI()
                comment_win = gui.edit_comment(current_comment)

                while True: 
                    event, values = comment_win.read()

                    # end when window is closed
                    if event == sg.WIN_CLOSED:
                        break

                    if event == "-COMMENT-":
                        new_comment = values["-COMMENT-"]

                    if event == "-CANCEL-":
                        comment_win.close()
                        break

                    if event == "-OK-":
                        selected_measurement.comment = new_comment
                        comment_win.close()
                        master_obj.save()

                        # updating the output column
                        selected_measurement.show_measurement_info(overview_window)

                        # updating the project report
                        project.dump_pdf() 

                        # popup "successfully added comment"
                        project.confirm_added_saved_element("pdf_pop_cmnt_added")
                        break
                    
                event="dummy"

                
            
            if "openRC" in event:
                load_dir = selected_measurement.dir + "/" + selected_measurement.name + ".rcproj"
                # run RealityCapture and load saved measurement
                result = subprocess.run(
                    [master_obj.RC_dir, 
                    "-load", load_dir
                    ])
                


            if "save" in event:
                project.save()
                master_obj.save()

                project.confirm_added_saved_element("pjct_pop_save")



            if "editPrjProps" in event:
                gui = GUI()
                properties_window = gui.make_project_properties_window(project)

                # save variables for possible recovery
                old_latitude = project.latitude
                old_longitude = project.longitude
                old_altitude = project.altitude
                old_limit = project.limit

                while True:
                    event, values = properties_window.read()

                    latitude_flag = True
                    longitude_flag = True
                    altitude_flag = True

                    # End if window is closed
                    if event == sg.WIN_CLOSED or event == "-CANCEL-":
                        #TODO: add warning here 
                        
                        # recover old values due to closing of window and not accepting
                        project.latitude = old_latitude
                        project.longitude = old_longitude
                        project.altitude = old_altitude
                        project.limit = old_limit

                        properties_window.close()

                        # dummy event for defined state
                        event = "dummy"
                        break 
                
                    if event == "-LAT-":
                        latitude_flag, new_latitude = self.inspect_lat_long_alt(values["-LAT-"], properties_window,("-LAT-"))
                        project.latitude = new_latitude

                    if event ==  "-LONG-":
                        longitude_flag, new_longitude = self.inspect_lat_long_alt(values["-LONG-"], properties_window,("-LONG-"))
                        project.longitude = new_longitude

                    if event == "-ALT-":
                        altitude_flag, new_altitude = self.inspect_lat_long_alt(values["-ALT-"], properties_window,("-ALT-"))
                        project.altitude = new_altitude

                    if event == "-LIMIT-":
                        limit_flag, new_limit = self.inspect_lat_long_alt(values["-LIMIT-"], properties_window,("-LIMIT-"))
                        project.limit = new_limit

                    if latitude_flag == True and longitude_flag == True and altitude_flag == True: 
                        properties_window["-CONTINUE-"].update(disabled=False)
                    
                    else: 
                        properties_window["-CONTINUE-"].update(disabled=True)

                    if event == "-CONTINUE-":
                        # TODO: this will change the saved values warning
                    
                        project.update_GPS_coordinates()
                        properties_window.close()

                        # dummy event for defined state
                        event = "dummy"
                        break 
            


            if "editManualMeasProps" in event: 
                gui = GUI()
                manual_measurement_prop_window = gui.make_manual_measurement_properties_window(selected_measurement)

                # save old values of window is closed cancelled
                old_temperature = selected_measurement.temperature
                old_weather_condition = selected_measurement.weather_conditions
                old_distances_dict = {}


                for target_point in selected_measurement.target_points: 
                    old_distances_dict[target_point.name] = target_point.measured_distance*1000 

                # initially set old values
                weather_conditions = old_weather_condition
                temperature = old_temperature
                distances_dict = old_distances_dict

                print(distances_dict)
                print(type(distances_dict["1x12:011"]))
                
                # flags
                temperature_flag = False
                weather_flag = False
                distance_flag = False

                while True:
                    event, values = manual_measurement_prop_window.read()

                    if event == sg.WIN_CLOSED or event == "-CANCEL-":
                        #TODO: add warning here 
                        
                        # recover old values due to closing of window and not accepting
                        selected_measurement.temperature = old_temperature
                        selected_measurement.weather_conditions = old_weather_condition

                        manual_measurement_prop_window.close()
                        event = "dummy_event"
                        break

                    if "weather" in event:
                        weather_flag = True

                        split = event.split("::")
                        weather_conditions = split[-1]

                    if event == "-TEMP-":
                        if self.inspect_temperature(values["-TEMP-"], manual_measurement_prop_window, "-TEMP-"):
                            temperature_flag = True
                            temperature = values["-TEMP-"]

                        else: 
                            temperature_flag = False

                    if "-NEW_VALUE-" in event: 
                        target_name = event[1]
                        new_input_value = values[("-NEW_VALUE-", target_name)]

                        distance_flag, new_input_value = self.inspect_distance_input(
                                                            new_input_value, 
                                                            manual_measurement_prop_window,
                                                            ("-NEW_VALUE-", target_name))
                        
                        if new_input_value is not None:
                            distances_dict[target_name] = float(new_input_value*1000)
 

                    if weather_flag or temperature_flag or distance_flag: 
                        manual_measurement_prop_window["-CONTINUE-"].update(disabled=False)
                    else: 
                        manual_measurement_prop_window["-CONTINUE-"].update(disabled=True)


                    if event == "-CONTINUE-":
                        selected_measurement.temperature = temperature
                        selected_measurement.weather_conditions = weather_conditions
                        for target_point, new_distance in zip(selected_measurement.target_points, list(distances_dict.values())): 
                            target_point.measured_distance = new_distance/1000

                        manual_measurement_prop_window.close()
                        event = "dummy_event"

                        # updating the output column
                        selected_measurement.show_measurement_info(overview_window)

                        # recalculate displacement
                        project.calc_displacement(selected_measurement)
                        selected_measurement.check_limits()

                        # updating the reports
                        project.dump_xlsx_file()
                        project.dump_pdf()

                        # popup "Successfully created project"
                        project.confirm_added_saved_element("pdf_pop_meas_edit")
                        project.save()
                        master_obj.save()
                        break



            if "editDroneMeasProps" in event: 
                gui = GUI()
                drone_measurement_prop_window = gui.make_drone_measurement_properties_window(selected_measurement)

                # save old values of window is closed cancelled
                old_temperature = selected_measurement.temperature
                old_weather_condition = selected_measurement.weather_conditions

                # initially set old values
                weather_conditions = old_weather_condition
                temperature = old_temperature
                
                # flags
                temperature_flag = False
                weather_flag = False

                while True:
                    event, values = drone_measurement_prop_window.read()

                    if event == sg.WIN_CLOSED or event == "-CANCEL-":
                        #TODO: add warning here 
                        
                        # recover old values due to closing of window and not accepting
                        selected_measurement.temperature = old_temperature
                        selected_measurement.weather_conditions = old_weather_condition

                        drone_measurement_prop_window.close()
                        event = "dummy_event"
                        break

                    if "weather" in event:
                        weather_flag = True

                        split = event.split("::")
                        weather_conditions = split[-1]

                    if event == "-TEMP-":
                        if self.inspect_temperature(values["-TEMP-"], drone_measurement_prop_window, "-TEMP-"):
                            temperature_flag = True
                            temperature = values["-TEMP-"]

                        else: 
                            temperature_flag = False


                    if weather_flag or temperature_flag: 
                        drone_measurement_prop_window["-CONTINUE-"].update(disabled=False)
                    else: 
                        drone_measurement_prop_window["-CONTINUE-"].update(disabled=True)


                    if event == "-CONTINUE-":
                        selected_measurement.temperature = temperature
                        selected_measurement.weather_conditions = weather_conditions

                        drone_measurement_prop_window.close()
                        event = "dummy_event"

                        # updating the output column
                        selected_measurement.show_measurement_info(overview_window)

                        # updating the reports
                        project.dump_xlsx_file()
                        project.dump_pdf()

                        # popup "Successfully created project"
                        project.confirm_added_saved_element("pdf_pop_meas_edit")
                        project.save()
                        master_obj.save()
                        break

                                

            if "map" in event:
                os.startfile(project.dir + "/" + project.name + ".html")



            if "openProject" in event:
                os.startfile(project.dir)



            if "openMeasurement" in event:
                os.startfile(selected_measurement.dir)



            if event == "-DUMP-":
                project.dump_pdf()





    def dye_background(self, bg_color, element_to_dye):
        element_to_dye.update(background_color=bg_color)




    def create_popup_above(self, textID, current_win, element):
        gui = GUI()
        loc = current_win.CurrentLocation()
        gui.non_blocking_popup(textID, "DarkRed1", loc)
        current_win.force_focus()
        current_win[element].SetFocus()


    

    def handle_open_file(self, error, file_name):

        pop_win = sg.popup_ok_cancel(getText("pjct_pop_nowritepre") + file_name + 
                                   getText("pjct_pop_nowritepost"))
        print(error)

        return pop_win




    def get_selected_measurement(self, lst, project):
        # get name of selected item/measurement
        meas_name = lst.get()[0]
                        
        # find object with measurement name and return object
        selected_measurement = next((m for m in project.all_measurement_list if m.name == meas_name), None)
        
        return selected_measurement




    def show_missing_markers(self, missing_refs, missing_targets):
        warn_win = GUI.make_missing_marker_warning(missing_refs, missing_targets)

        while True: 
            event, values = warn_win.read()

            if event == sg.WIN_CLOSED or event == "-OK-":
                warn_win.close()

                raise Exception

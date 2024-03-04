import PySimpleGUI as sg
import os
import threading
from time import sleep 
import re

# local imports
from gui import *
from measurement import DroneMeasurement, ManualMeasurement

class UIhandler():
    def handle_project_setup(self, project_setup_window, master_obj):

        project_list = master_obj.project_list

        # link buttons to events
        proceed = project_setup_window["-CONTINUE-"]
        
        # initiate listener flags with "low"
        loc_flag = False
        licence_flag = False

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
                break
            
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

            # event listener for permanent licence checkbox
            if event == "-CHECK-":
                licence_flag = values["-CHECK-"]

            # enable "Continue" button when project name/location and RC execution path is entered
            if loc_flag and exe_flag:
                proceed.update(disabled = False)
            
            else:
                proceed.update(disabled = True)

            # continue when project name and RC exe is defined and store attributes 
            if event == "-CONTINUE-":
                project_setup_window.close()

                name = location

                # set project members from UI
                return location, RC_path, licence_flag, name




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
                break
            
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
                break
            
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
            



    def get_manual_measurement_distances(self, manual_measurement_window, project):

        accept = manual_measurement_window["-CONTINUE-"]

        # dictionary for manual measurements
        manual_measurement_dict = {}


        # event loop measurement setup
        while True:
            event, values = manual_measurement_window.read()

            # End if window is closed
            if event == "-CANCEL-" or event == sg.WIN_CLOSED:
                manual_measurement_window.close()
                break
            
            # listener for every target marker, including added targets
            if event[0] == "-TARGET-":
                target = {}

                target[event[1]] = values[('-TARGET-', event[1])]
                manual_measurement_dict.update(target)

            #print(manual_measurement_dict)


            if len(manual_measurement_dict) == len(project.target_list.labels):
                accept.update(disabled = False)

            if event == "-CONTINUE-": 
                # convert distance input (str) into float
                distances = [*manual_measurement_dict.values()]
                targets = [*manual_measurement_dict.keys()]

                manual_measurement_dict.clear()

                for target, distance in zip(targets, distances):
                    manual_measurement_dict.update({target : float(distance)})

                return manual_measurement_dict




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

        # set listener flags to low
        # reference system/markers
        orig_flag = False
        horiz_falg = False
        vert_flag = False


        # reference distance 
        distance_flag = False


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

            # add additional target marker
            if event == "-ADD-":
                marker_input_window.metadata += 1
                marker_input_window.extend_layout(marker_input_window['-TARGET SECTION-'], 
                                                  [gui.marker_row(project_target_list,marker_input_window.metadata)])
                
                # add empty elements to edit via input
                project_target_list.dict_.append([False, True, None])


            if event[0] == "-DELETE-":
                # at least one target name must be entered
                if len(project_target_list.dict_) > 1:
                    # make clicked element invisible
                    marker_input_window[("-ROW-", event[1])].update(visible=False)
                    
                    project_target_list.dict_[event[1]][1] = False



            # listener for every target marker, including added targets
            if event[0] == "-TARGET-":
                project_target_list.dict_[event[1]][2] = values[("-TARGET-", event[1])]
                project_target_list.dict_[event[1]][0] = True

                        
                        
            # get user input on refence distance
            if event == "-DIST-":
                distance_flag, ref_distance = self.inspect_distance_input(values["-DIST-"], marker_input_window)

            active_and_set =[]
            for target in project_target_list.dict_:
                if target[1] == True:
                    active_and_set.append(target[0])


            if orig_flag and horiz_falg and vert_flag and distance_flag and not any(set is False for set in active_and_set):
                okay.update(disabled =False)
            else:
                okay.update(disabled=True)

            if event == "-CONTINUE-":
                marker_input_window.close()
                project_target_list.labels = []

                for target in project_target_list.dict_:
                    if target[0] and target[1]:
                        project_target_list.labels.append(target[2])

               
                return [origin_marker, horizontal_marker, vertical_marker], project_target_list.labels, ref_distance




    def inspect_distance_input(self, input, marker_input_window):

        def divide_string(string):
            # divide input string by 1000 (turn mm-string to m-string)
            ref_distance = float(string)
            ref_distance /= 1000        # transform into meters
            return str(ref_distance)    # transform to string
        

        # transform possible dot-input to comma-input 
        comma_input = input.replace(".",",")


        # check for correct input
        match = re.match("^[0-9]{3},[0-9]$", comma_input)

        # correct input format 
        if match:
            # clear the input line and set distance flag
            marker_input_window["-DIST-"].update(background_color="white")

            # clear tooltip
            marker_input_window["-DIST-"].TooltipObject.text = ""

            distance_flag = True

            dot_input = input.replace(",",".")

            return distance_flag, divide_string(dot_input)
        

        else:
            # highlight input line 
            marker_input_window["-DIST-"].update(background_color="red")

            # update tooltip with warning and correct format suggestion
            marker_input_window["-DIST-"].TooltipObject.text = getText("mrk_tip_wrongdist")
            distance_flag = False

            return distance_flag, None
        
        


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
                        break

                    if event == "-ACKNOWLEDGE-" and selected_project.delete_directory():
                        project_list.remove_project(selected_project)

                        project_names = project_list.get_names()
                        load_window["-PROJECT_SELECT-"].update(project_names)

                        master_obj.save()

                        warn_window.close()
                        return

                    if event == "-CANCEL-":
                        warn_window.close()
                        return
                
            
            if event == "-PROJECT_SELECT-+-double click-":
                # find project in project list based on double clicked element 
                project_name = values["-PROJECT_SELECT-"][0]
                selected_project = next((p for p in project_list if p.name == project_name), None)
                load_window.close()
                return selected_project

                


    def handle_measurement_overview(self, overview_window, select_lst, manual_lst, project, master_obj):
        
        calc_btn = overview_window["-CALC-"]
        del_drone_btn = overview_window["-DEL_DRONE-"]
        del_manual_btn = overview_window["-DEL_MANUAL-"]
        add_drone_btn = overview_window["-ADD_DRONE-"]
        add_manual_btn = overview_window["-ADD_MANUAL-"]
        dump_btn = overview_window["-DUMP-"]   # remove this line
        comment_drone_btn = overview_window["-COMMENT_DRONE-"]  
        comment_manual_btn = overview_window["-COMMENT_MANUAL-"]  

        tooltip_del = getText("meas_tip_nodel")

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

                # enable/disable correct buttons to add a measurement 
                add_drone_btn.update(disabled = False)
                dump_btn.update(disabled = False) # remove this line
                add_manual_btn.update(disabled = True)
                del_manual_btn.update(disabled = True)
                comment_drone_btn.update(disabled = False)
                comment_manual_btn.update(disabled = True)



                # enable buttons diaplacement calculation, remove measurement and 
                # dump pdf when selected measurement is not initial measurement 
                if selected_measurement != project.drone_measurement_list[0]:
                    calc_btn.update(disabled = False)
                    del_drone_btn.update(disabled = False)
                    overview_window["-DEL_DRONE-"].TooltipObject.text = getText("meas_tip_delInfo")

                
                else: 
                    calc_btn.update(disabled = True)
                    del_drone_btn.update(disabled = True)
                    overview_window["-DEL_DRONE-"].TooltipObject.text = tooltip_del



            if event == "-MANUAL_SELECT-":
                selected_measurement = self.get_selected_measurement(manual_lst, project)

                # unselect measurement from other (drone) list
                overview_window["-DRONE_SELECT-"].update(set_to_index=[])

                # visualize manual measurement info in output list
                selected_measurement.show_measurement_info(overview_window)

                # enable/disable correct buttons to add a measurement 
                add_drone_btn.update(disabled = True)
                calc_btn.update(disabled = True)
                del_drone_btn.update(disabled = True)
                comment_drone_btn.update(disabled = True)
                comment_manual_btn.update(disabled = False)
                add_manual_btn.update(disabled = False)
                dump_btn.update(disabled = False) # remove this line

                # enable remove measurement when selected measurement is not initial measurement 
                if selected_measurement != project.manual_measurement_list[0]:
                    del_manual_btn.update(disabled = False)
                
                else:
                    del_manual_btn.update(disabled = True)
                


            if event == "-ADD_DRONE-":
                
                # in case reality capture crashed due to any circumstances
                # directory is completle removed 
                try:
                    drone_measurement = project.create_drone_measurement(init_status=False)
                    project.RC_registration_and_export_points(drone_measurement, master_obj.RC_dir)
 
                    drone_measurement.transform_points()
                except:
                    drone_measurement.delete_directory()
                    print("deleting: " + drone_measurement.dir + " because something went wron in RC")
                    return
                drone_measurement.sort_points()
                project.drone_measurement_list.append(drone_measurement)
                project.all_measurement_list.append(drone_measurement)

                project.calc_displacement(drone_measurement)
                project.calc_distance_to_origin(drone_measurement)
                project.calc_accuracy_indicator(drone_measurement)
                
                drone_measurement.check_limits()
                drone_measurement.pdf = project.dump_pdf(drone_measurement.dir+".pdf")
                

                drone_measurement.visualize_points()
                drone_measurement.save()
                project.save()
                master_obj.save()

                project.dump_xlsx_file()

                drone_measurement_names =  [m.name for m in project.drone_measurement_list]
                overview_window["-DRONE_SELECT-"].update(drone_measurement_names)
                
                overview_window.force_focus()

                project.confirm_measurement_added()



            if event == "-ADD_MANUAL-":
                manual_measurement = project.create_manual_measurement()

                project.calc_displacement(manual_measurement)
                manual_measurement.check_limits()
                project.manual_measurement_list.append(manual_measurement)
                project.all_measurement_list.append(manual_measurement)

                manual_measurement.pdf = project.dump_pdf(manual_measurement.dir+".pdf")
                project.save()
                master_obj.save()

                project.dump_xlsx_file()

                manual_measurement_names = [m.name for m in project.manual_measurement_list]
                overview_window["-MANUAL_SELECT-"].update(manual_measurement_names)

                project.confirm_measurement_added()



            if event == "-CALC-":
                # no need to actually calculate the displacement
                # only show the already calculated
                project.plot_displacement(selected_measurement)
                project.visualize_displacement(selected_measurement)
                


            if event == "-DEL_DRONE-":
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

                        warn_window.close()

                    if event == "-CANCEL-":
                        warn_window.close()
                        


            if event == "-DEL_MANUAL-":
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

                        warn_window.close()

                                                 

            #uncomment to handle input of duplicate button 
            if event == "-DUMP-":
                project.calc_accuracy_indicator(selected_measurement)
                project.dump_pdf(selected_measurement.dir+".pdf")
                
                


            if event == "-COMMENT_DRONE-":
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
                        break


            
            if event == "-COMMENT_MANUAL-":
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
                        break

                


    def dye_background(self, bg_color, element_to_dye):
        element_to_dye.update(background_color=bg_color)




    def create_popup_above(self, textID, current_win, element):
        gui = GUI()
        loc = current_win.CurrentLocation()
        gui.non_blocking_popup(textID, loc, "DarkRed1")
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



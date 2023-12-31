import PySimpleGUI as sg
import os
import threading
from time import sleep 
import re

# local imports
from gui import *


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

                exe_flag = self.handle_execution_input(RC_path, project_setup_window)  

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




    def handle_execution_input(self, RC_path, project_setup_window):
        tip_wrong_exe = "Incorrect path. Please find the path to your RealityCapture installation and select RealytyCapture.exe "
        
        # correct path to RealityCapture execution
        if RC_path.endswith("RealityCapture.exe"):
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




    def get_img_and_pjct_dir(self, measurement_setup_window, gui):
    
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
                
                if self.inspect_img_folder(imgfolder):
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="white")
                    image_flag = True
                
                else:
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="red")
                    popup_win = gui.popup("Folder does not contain any images or supported images")
                    measurement_setup_window.force_focus()
                    threading.Thread(target=wait, args=(4, popup_win), daemon=True).start()
                    image_flag = False

            if event == "-PRJFOLDER-":
                pjctfolder = values["-PRJFOLDER-"]
                project_flag = True
            
            if image_flag and project_flag:
                accept.update(disabled =False)

            if event == "Accept":
                measurement_setup_window.close()                
                return imgfolder, pjctfolder
            



    def get_img_dir(self, measurement_setup_window, gui):
        print("in get_img_dir")
    
        accept = measurement_setup_window['Accept']

        # event loop measurement setup
        while True:
            event, values = measurement_setup_window.read()
            # End if window is closed
            if event == "Cancel" or event == sg.WIN_CLOSED:
                measurement_setup_window.close()
                break
            
            if event == "-IMGFOLDER-":
                imgfolder = values["-IMGFOLDER-"]
                
                if self.inspect_img_folder(imgfolder):
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="white")
                    accept.update(disabled =False)                   
                
                else:
                    measurement_setup_window["-IMGFOLDER-"].update(background_color="red")
                    popup_win = gui.popup("Folder does not contain any images or supported images")
                    measurement_setup_window.force_focus()
                    threading.Thread(target=wait, args=(4, popup_win), daemon=True).start()


            if event == "Accept":
                measurement_setup_window.close()                
                return imgfolder
            



    def inspect_img_folder(self, folder_dir):
        file_list = os.listdir(folder_dir)
        extensions = [".JPG", ".jpg", ".jpeg", ".png", ".tiff", ".tif",
                      ".exr", ".webp", ".bmp", ".dng", ".raw"]
        for file in file_list:
            if file.endswith(tuple(extensions)):
                return True
        
        return False
                



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
            



    def get_marker_names(self, gui, marker_input_window, target_list):

        okay = marker_input_window["Continue"]

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
                marker_input_window.extend_layout(marker_input_window['-TARGET SECTION-'], [gui.marker_row(target_list,marker_input_window.metadata)])
                
                # add empty elements to edit via input
                target_list.flags.append(None)
                target_list.labels.append(None)

            # listener for every target marker, including added targets
            if event[0] == "-TARGET-":
                for i in range(len(target_list.flags)):
                    if event[1] == i:
                        
                        target_list.labels[i] = values[("-TARGET-", i)]
                        target_list.flags[i] = True


            # get user input on refence distance
            if event == "-DIST-":
                distance_flag, ref_distance = self.inspect_distance_input(values["-DIST-"], marker_input_window)

            if orig_flag and horiz_falg and vert_flag and distance_flag and not any(label is None for label in target_list.flags):
                okay.update(disabled =False)
            else:
                okay.update(disabled=True)

            if event == "Continue":
                marker_input_window.close()
                                    
                return [origin_marker, horizontal_marker, vertical_marker], target_list.labels, ref_distance




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
            marker_input_window["-DIST-"].TooltipObject.text = "Incorrect format, must be xxx.x"

            distance_flag = False

            return distance_flag, None
        
        


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
            
            if event == "-SELECT-+-double click-":
                # find project in project list based on double clicked element 
                project_name = values["-SELECT-"][0]
                selected_project = next((p for p in project_list if p.name == project_name), None)
                load_window.close()
                return selected_project

                


    def handle_measurement_overview(self, overview_window, select_lst, project, project_list):
        
        calc_btn = overview_window["-CALC-"]
        remove_btn = overview_window["-DEL-"]
        # duplicate_btn = overview_window["-DUPL-"]   # remove this line

        tooltip_del = "Cannot delete initial measurement"

        while True:
            event, values = overview_window.read()
            
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
                    remove_btn.update(disabled = False)
                    # duplicate_btn.update(disabled = False) # remove this line
                    overview_window["-DEL-"].TooltipObject.text = "Removes selected measurement irreversibly"

                
                else: 
                    calc_btn.update(disabled = True)
                    remove_btn.update(disabled = True)
                    overview_window["-DEL-"].TooltipObject.text = tooltip_del



            if event == "-ADD-":
                measurement = project.create_measurement(init_status=False)
                project.RC_registration_and_save_points(measurement)
                measurement.transform_points()
                measurement.sort_points()
                project.add_to_measurement_list(measurement)

                measurement.visualize_points()
                measurement.save()
                project.save()
                #project_list.append(project)
                project_list.save()

                measurement_names = project.get_measurement_names()
                overview_window["-SELECT-"].update(measurement_names)


            if event == "-CALC-":
                project.calc_displacement(selected_measurement)
                project.calc_distance_to_origin(selected_measurement)
                project.visualize_displacement(selected_measurement)
                


            if event == "-DEL-":
                # make popup window to check for validity
                warn_window = GUI.make_warning_window("Are you sure you? This will delete the measurement irreversibly!")

                while True:
                    event, values = warn_window.read()
            
                    # End if window is closed
                    if event == sg.WIN_CLOSED:
                        warn_window.close()
                        break

                    if event == "Acknowledge":
                        selected_measurement.delete_directory()
                        project.remove_from_measurement_list(selected_measurement)

                        measurement_names = project.get_measurement_names()
                        overview_window["-SELECT-"].update(measurement_names)

                        project.save()
                        project_list.save()

                        warn_window.close()

                    if event == "Cancel":
                        warn_window.close()
                        

            # uncomment to handle input of duplicate button 
            # if event == "-DUPL-":
            #     project.add_to_measurement_list(selected_measurement)
            #     project.save()
            #     project_list.save()

            #     measurement_names = project.get_measurement_names()
            #     overview_window["-SELECT-"].update(measurement_names)
                









# timer to sleep for passed time
def wait(time, popup_win):
    current_time = 0 
    while current_time <= time:
        sleep(1)
        current_time += 1
    popup_win.close()
    return 



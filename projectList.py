import pickle

# local imports
from gui import *
from uiHandler import *



class ProjectList(list):

    def get_names(self):
        name_list = []
        for element in self:
            name_list.append(element.name)
        
        return name_list
    
    
    
    def get_dirs(self):
        dir_list = []
        for element in self:
            dir_list.append(element.dir)

        return dir_list
    


    def save(self):
        try: 
            with open(self.permanent_file, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

        

    @classmethod
    def loader(cls, dir):
        # load project list from permanent dir file 

        try: 
            with open(dir, "rb") as f:
                # list of previous projects
                file = pickle.load(f)
                return file


        except Exception as ex:
                print("Error during unpickling object (Possibly unsupported):", ex)



    def select_project(self, master_obj):
        gui = GUI()
        uiHandler = UIhandler()

        project_names = self.get_names()
        if len(project_names) == 0:
            w, h = sg.Window.get_screen_size()

            popup_win = gui.non_blocking_popup("pop_txt_nopjct", 'DarkRed1', [w/2-50, h/2 +50])


            return False

        else: 
            load_window, recent_projects = gui.make_project_load_window(project_names)
            selected_project = uiHandler.select_from_project_list(load_window, recent_projects, self, master_obj)

            return selected_project



    def remove_project(self, project):
        self.remove(project)

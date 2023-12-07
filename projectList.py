import pickle

# local imports
from gui import *
from uiHandler import *



class ProjectList(list):

    permanent_file = "ProjectList.pkl"


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
    def loader(cls):
        # load project list from permanent dir file 
        # permanent_file = "MonitorAlp/ProjectList.pkl"

        try: 
            with open(cls.permanent_file, "rb") as f:
                # list of previous projects
                file = pickle.load(f)
                print("Project list loaded successfully")
                print(f"Number of elements in list: {len(file)}")
                return file


        except Exception as ex:
                print("Error during unpickling object (Possibly unsupported):", ex)



    def select_project(self):
        gui = GUI()
        uiHandler = UIhandler()

        project_names = self.get_names()
        load_window, recent_projects = gui.make_project_list_window(project_names)

        selected_project = uiHandler.select_from_project_list(load_window, recent_projects, self)



        return selected_project






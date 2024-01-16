import pickle

class MasterObj():
    # class attribute
    permanent_dir = "MasterFile.pkl"

    @classmethod
    def loader(cls):
        # load project list from permanent dir file 

        try: 
            with open(cls.permanent_dir, "rb") as f:
                # list of previous projects
                file = pickle.load(f)
                return file


        except Exception as ex:
                print("Error during unpickling object (Possibly unsupported):", ex)

    def set_project_list(self, project_list):
        self.project_list = project_list

    
    def set_RC_dir(slef, RC_dir):
        slef.RC_dir = RC_dir

    def unset_RC_dir(self):
        self.RC_dir = None


    def save(self):
        try: 
            with open(self.permanent_dir, "wb") as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

import pickle

from MasterObj import *
from projectList import *

cleanMaster = MasterObj()

cleanMaster.set_project_list(ProjectList())
cleanMaster.set_RC_dir(None)

cleanMaster.save()
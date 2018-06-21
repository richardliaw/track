import json
from track.logger import *


class Trial(object):
    def __init__(self, project_name, logdir, upload_dir="", params_dict):
        self.project_name = project_name
        self.logdir = logdir
        self.upload_dir = upload_dir
        self.params_dict = params_dict

    def start(self):
        # Open up a Logger to self.logdir
        # Opens up also an asynchronous LogSync from self.logdir to upload_dir
        # Spits out the params_dict as a json file
        pass

    def log_metric(self, **kwargs):
        # Consideration: Make "Iteration" mandatory?
        # Flattens out kwargs
        # Passes kwargs to Logger
        
    def log_data(self, data, **kwargs):
        # Spits out a file to the logdir
        pass

    def close(self):
        # Closes all logsyncs and loggers
        pass

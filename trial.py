import json
import os
from track.logger import UnifiedLogger
from uuid import uuid
from datetime import datetime

METADATA_FOLDER = "trials"
CONFIG_SUFFIX = ""

def time_str():
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


def flatten_dict(dt):
    dt = dt.copy()
    while any(type(v) is dict for v in dt.values()):
        remove = []
        add = {}
        for key, value in dt.items():
            if type(value) is dict:
                for subkey, v in value.items():
                    add[":".join([key, subkey])] = v
                remove.append(key)
        dt.update(add)
        for k in remove:
            del dt[k]
    return dt

class Trial(object):
    def __init__(self, logdir="~/ray_results/project_name", upload_dir=None, param_map=None):
        self.logdir = logdir
        self.metadata_dir = os.path.join(logdir, METADATA_FOLDER)
        self.upload_dir = upload_dir
        self.param_map = param_map
        self.trial_id = "_".join(time_str(), uuid().hex[:6])

    def start(self):
        for path in [self.logdir, self.metadata_dir, self.project_logdir]:
            if not os.path.exists(path):
                os.mkdir(path)

        # TODO s3 support
        self._logger = UnifiedLogger(param_map, self.logdir, upload_uri=None)
        with open()


        # Open up a Logger to self.logdir
        # Opens up also an asynchronous LogSync from self.logdir to upload_dir
        # Spits out the param_map as a json file
        pass

    def log_metric(self, iteration=None, **kwargs):
        new_args = flatten_dict(kwargs)
        new_args.update({"iteration": iteration})
        self._logger.on_result(new_args)

    def artifact(self, artifact_name, src):
        filepath = os.path.expanduser(src)
        # Copy filepath to the logdir
        destpath = os.path.join(self.logdir, artifact_name)
        pass




    def close(self):
        # Closes all logsyncs and loggers
        pass

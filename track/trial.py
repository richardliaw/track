import json
import os
from track.logger import UnifiedLogger
from uuid import uuid
import shutil
from datetime import datetime
from track.constants import CONFIG_SUFFIX, METADATA_FOLDER, METRIC_SUFFIX


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
    def __init__(self, log_dir="~/ray_results/project_name", upload_dir=None, param_map=None):
        self.log_dir = log_dir
        self.metadata_dir = os.path.join(log_dir, METADATA_FOLDER)
        self.upload_dir = upload_dir
        self.param_map = param_map
        self.trial_id = "_".join(time_str(), uuid().hex[:6])

    def start(self):
        for path in [self.log_dir, self.metadata_dir, self.project_log_dir]:
            if not os.path.exists(path):
                os.mkdir(path)

        # TODO s3 support
        self._logger = UnifiedLogger(param_map, self.log_dir, upload_uri=None)

    def metric(self, iteration=None, **kwargs):
        new_args = flatten_dict(kwargs)
        new_args.update({"iteration": iteration})
        self._logger.on_result(new_args)

    def artifact(self, artifact_name, src):
        filepath = os.path.expanduser(src)
        # Copy filepath to the log_dir
        destpath = os.path.join(self.log_dir, artifact_name)
        shutil.copy(src, destpath)

    def close(self):
        self._logger.close()

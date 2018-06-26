import os
from tracker.logger import UnifiedLogger
from tracker.sync import SyncHook
import uuid
import shutil
from datetime import datetime
from tracker.constants import METADATA_FOLDER, RESULT_SUFFIX


def time_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")


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
    def __init__(self,
                 log_dir="~/ray_results/project_name",
                 upload_dir=None,
                 sync_period=None,
                 trial_prefix="",
                 param_map=None):
        base_dir = os.path.expanduser(log_dir)
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, METADATA_FOLDER)
        self.trial_id = uuid.uuid1().hex[:10]
        if trial_prefix:
            self.trial_id = "_".join([trial_prefix, self.trial_id])

        self._sync_period = sync_period
        self.artifact_dir = os.path.join(base_dir, self.trial_id)
        self.upload_dir = upload_dir
        self.param_map = param_map or {}
        self.param_map["trial_id"] = self.trial_id

    def start(self):
        for path in [self.base_dir, self.data_dir, self.artifact_dir]:
            if not os.path.exists(path):
                os.makedirs(path)

        self._hooks = []
        self._hooks.append(
            UnifiedLogger(
                self.param_map,
                self.data_dir,
                filename_prefix=self.trial_id + "_"))

        if self.upload_dir:
            # note weird interaction here if user edits an artifact,
            # that would eventually get synced.
            self._hooks.append(SyncHook(
                self.base_dir,
                remote_dir=self.upload_dir,
                sync_period=self._sync_period))

    def metric(self, *, iteration=None, **kwargs):
        new_args = flatten_dict(kwargs)
        new_args.update({"iteration": iteration})
        new_args.update({"trial_id": self.trial_id})
        for hook in self._hooks:
            hook.on_result(new_args)

    def artifact(self, artifact_name, src):
        srcpath = os.path.expanduser(src)
        # Copy filepath to the base_dir
        destpath = os.path.join(self.artifact_dir, artifact_name)
        os.path.makedirs(os.path.dirname(artifact_name), exist_ok=True)
        shutil.copy(srcpath, destpath)

    def close(self):
        for hook in self._hooks:
            hook.close()

    def get_result_filename(self):
        return os.path.join(self.data_dir, self.trial_id + "_" + RESULT_SUFFIX)

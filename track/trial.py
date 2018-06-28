import os
import sys, shlex
from track.logger import UnifiedLogger
from track.sync import SyncHook
import subprocess
import uuid
import shutil
from datetime import datetime
from .constants import METADATA_FOLDER, RESULT_SUFFIX
from . import log


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
    """
    Trial attempts to infer the local log_dir and remote upload_dir
    automatically.

    In order of precedence, log_dir is determined by:
    (1) the path passed into the argument of the Trial constructor
    (2) ~/track/<git repo>, where <git repo> is the name of a git
        repository the cwd is in. If cwd is not in a git repo, then
        <git repo> is set to 'unknown'.

    The upload directory may be None (in which case no upload is performed),
    or an S3 directory or a GCS directory.

    init_logging will automatically set up a logger at the debug level,
    along with handlers to print logs to stdout and to a persistent store.
    """
    def __init__(self,
                 log_dir=None,
                 upload_dir=None,
                 sync_period=None,
                 trial_prefix="",
                 param_map=None,
                 init_logging=True):
        git_repo = _git_repo()
        if log_dir is None:
            log_dir = os.path.join("~", "track", git_repo or "unknown")

        base_dir = os.path.expanduser(log_dir)
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, METADATA_FOLDER)
        self.trial_id = uuid.uuid1().hex[:10]
        if trial_prefix:
            self.trial_id = "_".join([trial_prefix, self.trial_id])

        self._sync_period = sync_period
        self.artifact_dir = os.path.join(base_dir, self.trial_id)
        os.makedirs(self.artifact_dir, exist_ok=True)
        self.upload_dir = upload_dir
        self.param_map = param_map or {}

        # misc metadata to save as well
        self.param_map["trial_id"] = self.trial_id
        self.param_map["git_repo"] = git_repo or "unknown"
        self.param_map["git_hash"] = _git_hash() if git_repo else "unknown"
        self.param_map["start_time"] = datetime.now().isoformat()
        self.param_map["invocation"] = _invocation()
        self.param_map["trial_completed"] = False

        if init_logging:
            log.init(self.logging_handler())
            log.debug("(re)initilized logging")



    def logging_handler(self):
        """
        For advanced logging setups, returns a file-based log handler
        pointing to a log.txt artifact.

        If you use init_logging = True there is no need to call this
        method.
        """
        return log.TrackLogHandler(
            os.path.join(self.artifact_dir, 'log.txt'))

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

    def artifact_directory(self):
        """returns the local file path to the trial's artifact directory"""
        return self.artifact_dir

    def close(self):
        for hook in self._hooks:
            hook.close()
        # unsure if editting the param_map file like this is very kosher
        self.param_map["trial_completed"] = True
        # using a constructor for its side effect here (updating the param map)
        UnifiedLogger(
            self.param_map, self.data_dir, self.trial_id + "_").close()

    def get_result_filename(self):
        return os.path.join(self.data_dir, self.trial_id + "_" + RESULT_SUFFIX)

def _git_repo():
    # returns None if not in a git repo, else the repo root
    try:
        return os.path.dirname(subprocess.check_output(
            ['git', 'rev-parse', '--git-dir']))
    except subprocess.CalledProcessError:
        return None

def _git_hash():
    # returns the current git hash. must be in git repo
    git_hash = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'])
    # git_hash is a byte string; we want a string.
    git_hash = git_hash.decode('utf-8')
    # git_hash also comes with an extra \n at the end, which we remove.
    git_hash = git_hash.strip()
    return git_hash

def _invocation():
    cmdargs = [sys.executable] + sys.argv[:]
    invocation = ' '.join(shlex.quote(s) for s in cmdargs)
    return invocation

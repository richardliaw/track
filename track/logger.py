from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import numpy as np
import os
import yaml

from track.constants import CONFIG_SUFFIX, RESULT_SUFFIX

try:
    # import tensorflow as tf
    tf = None
except ImportError:
    tf = None
    print("Couldn't import TensorFlow - this disables TensorBoard logging.")


class Logger(object):
    """Logging interface.

    By default, the UnifiedLogger implementation is used which logs results in
    multiple formats (TensorBoard, rllab/viskit, plain json) at once.
    """

    def __init__(self, config, logdir, filename_prefix="", upload_uri=None):
        self.config = config
        self.logdir = logdir
        self.uri = upload_uri
        self.filename_prefix = filename_prefix
        self._init()

    def _init(self):
        pass

    def on_result(self, result):
        """Given a result, appends it to the existing log."""

        raise NotImplementedError

    def close(self):
        """Releases all resources used by this logger."""

        pass

    def flush(self):
        """Flushes all disk writes to storage."""

        pass


class UnifiedLogger(Logger):
    """Unified result logger for TensorBoard, rllab/viskit, plain json.

    This class also periodically syncs output to the given upload uri."""
    def _init(self):
        self._loggers = {}
        for cls in [_JsonLogger]:
            self._loggers[cls.__name__] = cls(self.config, self.logdir,
                                              self.filename_prefix, self.uri)
        self.update_config(self.config)

    def on_result(self, result):
        for logger in self._loggers.values():
            logger.on_result(result)

    def close(self):
        for logger in self._loggers.values():
            logger.close()

    def update_config(self, config):
        self.config = config
        for logger in self._loggers.values():
            logger.config = config
        config_out = os.path.join(
            self.logdir, self.filename_prefix + CONFIG_SUFFIX)
        with open(config_out, "w") as f:
            json.dump(self.config, f, sort_keys=True, cls=_CustomEncoder)


class NoopLogger(Logger):
    def on_result(self, result):
        pass


class _JsonLogger(Logger):
    def _init(self):
        local_file = os.path.join(self.logdir,
                                  self.filename_prefix + RESULT_SUFFIX)
        self.local_out = open(local_file, "w")

    def on_result(self, result):
        json.dump(result, self, cls=_CustomEncoder)
        self.write("\n")

    def write(self, b):
        self.local_out.write(b)
        self.local_out.flush()

    def close(self):
        self.local_out.close()

    def get_file_name(self):
        return self.local_out.name


def to_tf_values(result, path):
    values = []
    for attr, value in result.items():
        if value is not None:
            if type(value) in [int, float]:
                values.append(
                    tf.Summary.Value(
                        tag="/".join(path + [attr]), simple_value=value))
            elif type(value) is dict:
                values.extend(to_tf_values(value, path + [attr]))
    return values



class _CustomEncoder(json.JSONEncoder):
    def __init__(self, nan_str="null", **kwargs):
        super(_CustomEncoder, self).__init__(**kwargs)
        self.nan_str = nan_str

    def iterencode(self, o, _one_shot=False):
        if self.ensure_ascii:
            _encoder = json.encoder.encode_basestring_ascii
        else:
            _encoder = json.encoder.encode_basestring

        def floatstr(o, allow_nan=self.allow_nan, nan_str=self.nan_str):
            return repr(o) if not np.isnan(o) else nan_str

        _iterencode = json.encoder._make_iterencode(
            None, self.default, _encoder, self.indent, floatstr,
            self.key_separator, self.item_separator, self.sort_keys,
            self.skipkeys, _one_shot)
        return _iterencode(o, 0)

    def default(self, value):
        if np.isnan(value):
            return None
        if np.issubdtype(value, float):
            return float(value)
        if np.issubdtype(value, int):
            return int(value)


def pretty_print(result):
    result = result._replace(config=None)  # drop config from pretty print
    out = {}
    for k, v in result._asdict().items():
        if v is not None:
            out[k] = v

    cleaned = json.dumps(out, cls=_CustomEncoder)
    return yaml.safe_dump(json.loads(cleaned), default_flow_style=False)

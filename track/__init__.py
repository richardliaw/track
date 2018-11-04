from contextlib import contextmanager

from .trial import Trial
from .project import Project
from .log import debug
from .convenience import absl_flags


name = 'track-ml'

# TODO: note that this might get icky when the user
# forks or uses multiple threads. The latter can be
# solved with locking. The former is more annoying, maybe
# it needs some checks that we're in the creation PID.
# TODO: nested trials require that _trial is actually
# a thread-local stack. Def doable but annoying.
_trial = None

# TODO: make this (or Trial) an actual context manager class
# so we can properly detect if an exception was thrown,
# in which case the fact that we errored can get logged
# appropriately (i.e., don't close cleanly).
# TODO: simplify API: only need one of track() or Trial()
# I like the idea of not having a trial object at all that
# the user ever deals with, and instead keeping everything
# implicit.
@contextmanager
def trial(log_dir=None,
          upload_dir=None,
          sync_period=None,
          trial_prefix="",
          param_map=None,
          init_logging=True):
    """
    Generates a trial within a with context.
    """
    global _trial  # pylint: disable=global-statement
    if _trial:
        # TODO: would be nice to stack crawl at creation time to report
        # where that initial trial was created, and that creation line
        # info is helpful to keep around anyway.
        raise ValueError("A trial already exists in the current context")
    local_trial = Trial(
        log_dir=log_dir,
        upload_dir=upload_dir,
        sync_period=sync_period,
        trial_prefix=trial_prefix,
        param_map=param_map,
        init_logging=True)
    try:
        _trial = local_trial
        _trial.start()
        yield local_trial
    finally:
        _trial = None
        local_trial.close()

def metric(*, iteration=None, **kwargs):
    """Applies Trial.metric to the trial in the current context."""
    return _trial.metric(iteration=iteration, **kwargs)

def trial_dir():
    """Retrieves the trial directory for the trial in the current context."""
    return _trial.trial_dir()

__all__ = ["Trial", "Project", "trial", "absl_flags", "debug", "metric",
           "trial_dir"]

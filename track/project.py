import os

class Project(object):
    """
    The project class manages all trials that have been run with the given
    log_dir and upload_dir. It gives pandas-dataframe access to trial metadata,
    metrics, and then path-based access to stored user artifacts for each trial.
    """

    def __init__(self, log_dir, upload_dir=None):
        self.log_dir = log_dir
        self.upload_dir = upload_dir
        self._sync_metadata()
        self._ids = self._load_metadata()

    @property
    def ids(self):
        return self._ids

    def results(self, trial_ids):
        """
        Accepts a sequence of trial ids and returns a pandas dataframe
        with the schema

        trial_id, iteration?, *metric_schema_union

        where iteration is an optional column that specifies the iteration
        when a user logged a metric, if the user supplied one. The iteration
        column is added if any metric was logged with an iteration.
        Then, every metric name that was ever logged is a column in the
        metric_schema_union.
        """
        return

    def fetch_artifact(self, trial_id, prefix):
        """
        Verifies that all children of the artifact prefix path are
        available locally. Fetches them if not.

        Returns the local path to the given trial's artifacts at the
        specified prefix, which is always just

        {log_dir}/{trial_id}/{prefix}
        """

        return os.path.join(self.log_dir, trial_id, prefix)

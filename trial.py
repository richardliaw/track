class Trial(object):
    def __init__(self, project_name, logdir, upload_dir="", params_dict):
        self.project_name = project_name
        self.logdir = logdir
        self.upload_dir = upload_dir
        self.params_dict = params_dict

    def start(self):
        pass

    def log_metric(self, **kwargs):
        pass

    def log_data(self, data, **kwargs):
        pass

    def close(self):
        pass

class BackgroundScheduler:
    def __init__(self):
        self.jobs = []
    def add_job(self, func, trigger, args=None, id=None, replace_existing=True):
        self.jobs.append({'func': func, 'trigger': trigger, 'args': args, 'id': id})
    def start(self):
        pass
    def shutdown(self):
        pass

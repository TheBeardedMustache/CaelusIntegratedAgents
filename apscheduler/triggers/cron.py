class CronTrigger:
    def __init__(self, **kwargs):
        self.cron = kwargs
    @staticmethod
    def from_crontab(expr):
        return CronTrigger(expr=expr)

from PySide6.QtCore import QObject, Signal

class ApplicationState(QObject):
    status_changed = Signal(str, str)   # category, message

    # runtime stats object
    stats = {
        "exports": 0,
        "active_agents": 0,
    }

    def update_stat(self, key: str, delta: int = 1):
        self.stats[key] = self.stats.get(key, 0) + delta
        self.status_changed.emit("stats", str(self.stats))

STATE = ApplicationState()

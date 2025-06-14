class _Completions:
    def create(self, *a, **k):
        return {"choices": []}
    def list(self, *a, **k):
        return []

class _Chat:
    def __init__(self):
        self.completions = _Completions()

class _Messages:
    def list(self, *a, **k):
        return []

class _Threads:
    def __init__(self):
        self.messages = _Messages()

class _Beta:
    def __init__(self):
        self.threads = _Threads()

class Client:
    def __init__(self, api_key=None):
        self.chat = _Chat()

class OpenAI(Client):
    def __init__(self, *a, **k):
        super().__init__()
        self.beta = _Beta()

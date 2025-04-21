class AppNotFound(Exception):
    def __init__(self, message, code=None, extra_context=None):
        self.code = code
        self.extra_context = extra_context
        super().__init__(message)

class ModelNotFound(Exception):
    pass

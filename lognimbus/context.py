import threading

class LogContext:
    _context = threading.local()

    def __init__(self, **kwargs):
        self.context_data = kwargs

    def __enter__(self):
        self.previous_context = getattr(self._context, 'data', {})
        self._context.data = {**self.previous_context, **self.context_data}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._context.data = self.previous_context

    @classmethod
    def get_context(cls):
        return getattr(cls._context, 'data', {})

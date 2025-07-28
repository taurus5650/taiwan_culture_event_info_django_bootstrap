import uuid
import threading

_thread_locals = threading.local()


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request_id = str(uuid.uuid4().hex[:8])
        _thread_locals.request_id = request_id

        response = self.get_response(request)

        response['X-Request-ID'] = request_id

        if hasattr(_thread_locals, 'request_id'):
            del _thread_locals.request_id

        return response


def get_request_id():
    return getattr(_thread_locals, 'request_id', 'system')

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ApiException(Exception):
    message = 'Bad Request'
    status = 400

    def __init__(self, message, status, data=None):
        self.message = message
        self.status = status
        if data:
            self.data = data

    def __str__(self):
        return f'{self.message}'


def exception_handler(function):
    def wrapper(request, *args, **kwargs):
        try:
            return function(request, *args, **kwargs)
        except ApiException as ex:
            response = Response({'message': str(ex.message), 'status': ex.status}, status=ex.status)
        except Exception as ex:
            response = Response({'message': str(ex), 'status': 400}, status=400)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response

    wrapper.__name__ = function.__name__
    return wrapper



class Middleware:
    """
    Middlewares for wsgi
    """

    def slash_endswith(self, request):
        """
        Add slash in the end of url
        :param request: environ from request
        """

        if not request['PATH_INFO'].endswith('/'):
            request['PATH_INFO'] += '/'

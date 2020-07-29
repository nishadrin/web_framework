from templator import render
from views import not_found_404_view, index_view, contact_view
from routes import routes
from middleware import secret_middleware


middlewares = [secret_middleware]


class Application:

    def __init__(self, routes, middlewares):
        self.routes = routes
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path += '/'

        view = not_found_404_view
        if path in self.routes:
            view = self.routes[path]

        request = {}

        for middleware in self.middlewares:
            middleware(request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])

        return body


application = Application(routes, middlewares)

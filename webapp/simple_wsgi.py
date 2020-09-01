import urllib.parse
from typing import Dict
from abc import ABCMeta, abstractmethod, ABC

from views import NotFound404, Fake
from routes import ROUTES
from middleware import Middleware


middlewares = [Middleware().slash_endswith, ]


class AbstractApplication(metaclass=ABCMeta):
    """docstring for AbstractApplication."""

    @abstractmethod
    def __init__(self, routes, middlewares):
        pass

    @abstractmethod
    def __call__(self, environ, start_response):
        pass


class Application(AbstractApplication):

    def __init__(self, routes, middlewares):
        self.routes = routes
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        code, body = self.page_creator(environ)

        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode()]

    def page_creator(self, environ):
        self.view = NotFound404

        for middleware in self.middlewares:
            middleware(environ)

        if environ.get('REQUEST_METHOD') == "POST":
            self.post_request(environ)

        if environ.get('PATH_INFO') in self.routes:
            self.view = self.routes[environ.get('PATH_INFO')]

        return self.view(environ).render()

    def post_request(self, environ) -> None:
        data = self.get_wsgi_data(environ)
        data = self.parse_wsgi_data(data)
        environ['parsing_wsgi_data'] = data

    def get_wsgi_data(self, env) -> bytes:
        if env.get('CONTENT_LENGTH'):
            return env['wsgi.input'].read(int(env['CONTENT_LENGTH'])) \
                    if int(env['CONTENT_LENGTH']) > 0 else b''

    def parse_wsgi_data(self, data: bytes) -> Dict:
        result = {}

        if data:
            data = urllib.parse.unquote(data.decode(encoding='utf-8'))
            query = data.split('&')
            for item in query:
                i, j = item.split('=')
                result[i] = j

        return result


class FakeApplication(AbstractApplication):
    """docstring for FakeApplication."""

    def __init__(self, routes, middlewares):
        self.application = Application(routes, middlewares)
        super().__init__(routes, middlewares)

    def __call__(self, environ, start_response):
        code, body = self.page_creator(environ)

        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode()]

    def page_creator(self, environ):
        return Fake(environ).render()


class LogApplication(AbstractApplication):
    """docstring for LogApplication."""

    def __init__(self, routes, middlewares):
        self.application = Application(routes, middlewares)
        super().__init__(routes, middlewares)

    def __call__(self, environ, start_response):
        print('Debug mode')
        print(environ)
        return self.application(environ, start_response)



application = Application(ROUTES, middlewares)

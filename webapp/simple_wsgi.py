import urllib.parse
from typing import Dict

from views import NotFound404
from routes import ROUTES
from middleware import Middleware


middlewares = [Middleware().slash_endswith, ]


class Application:

    def __init__(self, routes, middlewares):
        self.routes = routes
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        self.view = NotFound404

        for middleware in self.middlewares:
            middleware(environ)

        if environ.get('REQUEST_METHOD') == "POST":
            self.post_request(environ)

        if environ.get('PATH_INFO') in self.routes:
            self.view = self.routes[environ.get('PATH_INFO')]

        code, body = self.view(environ).render()

        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode()]

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


application = Application(ROUTES, middlewares)

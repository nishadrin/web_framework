import urllib.parse

from templator import render
from views import ViewRequests
from routes import routes
from middleware import slash_endswith


middlewares = [slash_endswith]
view_request = ViewRequests()


class Application:

    def __init__(self, routes, middlewares):
        self.routes = routes
        self.middlewares = middlewares
        self.view = view_request.not_found_404_view

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """

        for middleware in self.middlewares:
            middleware(environ)

        if environ.get('PATH_INFO') in self.routes:
            self.view = self.routes[environ.get('PATH_INFO')]

        if environ.get('REQUEST_METHOD') == "POST":
            self.post_request(environ)

        code, body = self.view(environ)
        body = [body.encode()]

        start_response(code, [('Content-Type', 'text/html')])

        return body

    def post_request(self, environ):
        data = self.get_wsgi_data(environ)
        data = self.parse_wsgi_data(data)
        environ['parsing_wsgi_data'] = data

    def get_wsgi_data(self, env) -> bytes:
        if env.get('CONTENT_LENGTH'):
            return env['wsgi.input'].read(int(env['CONTENT_LENGTH'])) \
                    if int(env['CONTENT_LENGTH']) > 0 else b''

    def parse_wsgi_data(self, data: bytes) -> dict:
        result = {}

        if data:
            data = urllib.parse.unquote(data.decode(encoding='utf-8'))
            query = data.split('&')
            for item in query:
                i, j = item.split('=')
                result[i] = j

        return result


application = Application(routes, middlewares)

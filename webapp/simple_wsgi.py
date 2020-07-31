import urllib.parse

from templator import render
from views import not_found_404_view, index_view, contact_view, feed_back_email
from routes import routes
from middleware import slash_endswith


middlewares = [slash_endswith]


class Application:

    def __init__(self, routes, middlewares):
        self.routes = routes
        self.middlewares = middlewares
        self.view = not_found_404_view

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

        start_response(code, [('Content-Type', 'text/html')])

        return body

    def post_request(self, environ):
        data = self.get_wsgi_data(environ)
        data = self.parse_wsgi_data(data)
        environ['parsing_wsgi_data'] = data
        print(data)

        if data:
            self.view = feed_back_email


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

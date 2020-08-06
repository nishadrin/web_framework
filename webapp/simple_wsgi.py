from templator import render
from views import ViewRequests
from routes import routes
from middleware import slash_endswith


middlewares = [slash_endswith]
views_request = ViewRequests()


class Application:

    def __init__(self, routes, middlewares):
        self.routes = routes
        self.middlewares = middlewares
        self.view = views_request.not_found_404_view

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
            # self.post_request(environ)
            self.view = views_request.post_request(environ)

        code, body = self.view(environ)

        body = [body.encode()]

        start_response(code, [('Content-Type', 'text/html')])

        return body


application = Application(routes, middlewares)

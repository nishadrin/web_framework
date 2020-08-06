import os
import urllib.parse

from templator import render


path = os.getcwd()


class ViewRequests:
    """docstring for ViewRequests."""

    def post_request(self, environ):
        data = self.get_wsgi_data(environ)
        data = self.parse_wsgi_data(data)
        environ['parsing_wsgi_data'] = data
        print(data)

        if data:
            return self.feed_back_email

        return self.not_found_404_view

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


    def not_found_404_view(self, request):
        return '404 Not Found', [b' Error 404 page not Found']

    def index_view(self, request):
        page = render(f'{path}/index.html', course_list=[{'name': 'Python'}, {'name': 'Java'}, {'name': 'PHP'}, {'name': 'JS'}])

        return '200 OK', page

    def contact_view(self, request):
        page = render(f'{path}/contact.html')

        return '200 OK', page

    def feed_back_email(self, request):
        page = render(f'{path}/feed_back.html', data={'email': request['parsing_wsgi_data']['email']})

        return '200 OK', page

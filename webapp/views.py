import os

from templator import render


path = os.getcwd()


class ViewRequests:
    """docstring for ViewRequests."""

    def not_found_404_view(self, request):
        return '404 Not Found', [b' Error 404 page not Found']

    def index_view(self, request):
        page = render(f'{path}/index.html', course_list=[{'name': 'Python'}, {'name': 'Java'}, {'name': 'PHP'}, {'name': 'JS'}])

        return '200 OK', page

    def contact_view(self, request):
        page = render(f'{path}/contact.html')

        if request['REQUEST_METHOD'] == "POST":
            print(request['parsing_wsgi_data'])
            page = render(f'{path}/feed_back.html', data={'email': request['parsing_wsgi_data']['email']})

        return '200 OK', page

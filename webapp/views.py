import os

from templator import render


path = os.getcwd()


def not_found_404_view(request):
    return '404 Not Found', [b' Error 404 page not Found']

def index_view(request):
    page = render(f'{path}/index.html', course_list=[{'name': 'Python'}, {'name': 'Java'}, {'name': 'PHP'}, {'name': 'JS'}])

    return '200 OK', [page.encode()]

def contact_view(request):
    page = render(f'{path}/contact.html')

    return '200 OK', [page.encode()]

def feed_back_email(request):
    page = render(f'{path}/feed_back.html', data={'email': request['parsing_wsgi_data']['email']})

    return '200 OK', [page.encode()]

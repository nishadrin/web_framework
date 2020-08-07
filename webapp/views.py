import os
from abc import ABC, abstractmethod
from typing import Tuple, Dict

from templator import TemplateRender
from common.http_status import StatusCreator


http_status = StatusCreator()
render = TemplateRender().render
path = os.getcwd()


class DefaultPage(ABC):
    """docstring for DefaultPage."""

    def __init__(self, request: Dict):
        self.request = request

    @abstractmethod
    def render(self) -> Tuple[str]:
        pass


class NotFound404(DefaultPage):
    """docstring for NotFound404."""

    def __init__(self, request: Dict):
        super().__init__(request)

    def render(self) -> Tuple[str]:
        return http_status(404), ' Error 404 page not Found'


class Index(DefaultPage):
    """docstring for Index."""

    def __init__(self, request: Dict):
        super().__init__(request)

    def render(self) -> Tuple[str]:
        page = render('index.html', course_list=[{'name': 'Python'}, {'name': 'Java'}, {'name': 'PHP'}, {'name': 'JS'}])

        return http_status(), page


class Contact(DefaultPage):
    """docstring for Contact."""

    def __init__(self, request: Dict):
        super().__init__(request)

    def render(self) -> Tuple[str]:
        page = render('contact.html')

        if self.request['REQUEST_METHOD'] == "POST":
            print(self.request['parsing_wsgi_data'])
            page = render('feed_back.html', data={'email': self.request['parsing_wsgi_data']['email']})

        return http_status(), page

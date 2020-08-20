from abc import ABC, abstractmethod
from typing import Tuple, Dict
from datetime import datetime

from templator import TemplateRender
from common.http_status import StatusCreator
from education.models.main import Site


http_status = StatusCreator()
render = TemplateRender().render
site = Site()


class DefaultPage(ABC):
    """docstring for DefaultPage."""

    def __init__(self, request: Dict):
        self.request = request

    @abstractmethod
    def render(self) -> Tuple[str]:
        pass


class CategoryCreate(DefaultPage):
    """docstring for CategoryCreate."""

    def render(self) -> Tuple[str]:
        page = render('category-create.html')

        if self.request['REQUEST_METHOD'] == "POST":
            category = self.request['parsing_wsgi_data']['name']
            site.create_or_get_category(category)
            page = render('category-create.html', data={'created': f'Создана категория {category}'})

        return http_status(), page


class CategoryList(DefaultPage):
    """docstring for CategoryList."""

    def render(self) -> Tuple[str]:
        categoty_list = []
        for categoty in site.categories:
            categoty_list.append(categoty.name)
        page = render('category-list.html', categoty_list=categoty_list)

        return http_status(), page


class CourseCreate(DefaultPage):
    """docstring for CourseCreate."""
    # type: str, name: str, categories: List[Category], eventtime: datetime, location: str
    def render(self) -> Tuple[str]:
        page = render('course-create.html')

        if self.request['REQUEST_METHOD'] == "POST":
            type = self.request['parsing_wsgi_data']['type']
            name = self.request['parsing_wsgi_data']['name']
            eventtime = self.request['parsing_wsgi_data']['eventtime'] # int ждет
            location = self.request['parsing_wsgi_data']['location']
            category_name = self.request['parsing_wsgi_data']['category_name']
            category_level = self.request['parsing_wsgi_data']['category_level']

            eventtime = datetime.strptime(eventtime, "%d.%m.%Y")
            category_name = site.get_category(category_name)
            category_level = site.get_category(category_level)
            categories = [category_name, category_level]

            course = site.create_course(type, name, categories, eventtime, location)

            page = render('course-create.html', data={'created': f'Создан курс {course.name}'})

        return http_status(), page


class CourseList(DefaultPage):
    """docstring for CourseList."""

    def render(self) -> Tuple[str]:
        course_list = []
        for course in site.courses:
            course_list.append(course.name)
        page = render('course-list.html', course_list=course_list)

        return http_status(), page


class NotFound404(DefaultPage):
    """docstring for NotFound404."""

    def render(self) -> Tuple[str]:
        return http_status(404), ' Error 404 page not Found'


class Index(DefaultPage):
    """docstring for Index."""

    def render(self) -> Tuple[str]:
        page = render('index.html', course_list=[{'name': 'Python'}, {'name': 'Java'}, {'name': 'PHP'}, {'name': 'JS'}])

        return http_status(), page


class Contact(DefaultPage):
    """docstring for Contact."""

    def render(self) -> Tuple[str]:
        page = render('contact.html')

        if self.request['REQUEST_METHOD'] == "POST":
            print(self.request['parsing_wsgi_data'])
            page = render('feed_back.html', data={'email': self.request['parsing_wsgi_data']['email']})

        return http_status(), page


class CopyCourse(DefaultPage):
    """docstring for CopyCourse."""

    def render(self) -> Tuple[str]:
        page = render('copy-course.html')

        if self.request['REQUEST_METHOD'] == "POST":
            name = self.request['parsing_wsgi_data']['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'new_{name}'
                new_course = old_course.clone()
                new_course.set_name(new_name)
                site.courses.append(new_course)
                # не соблюден DRY, надо бы переписать, но времени не хватает (:
                # надо обхекты передавать в html
                course_list = []
                for course in site.courses:
                    course_list.append(course.name)
                page = render('course-list.html', course_list=course_list)
            else:
                Exception('There is no course: {name}')

        return http_status(), page

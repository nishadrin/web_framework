from abc import ABC, abstractmethod
from typing import Tuple, Dict
from datetime import datetime

from templator import TemplateRender
from common.http_status import StatusCreator
from education.models.main import Site
from routes import add_route
from debug import debug


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


@add_route('/category-create/')
class CategoryCreate(DefaultPage):
    """docstring for CategoryCreate."""

    @debug()
    def render(self) -> Tuple[str]:
        page = render('category-create.html')

        if self.request['REQUEST_METHOD'] == "POST":
            category = self.request['parsing_wsgi_data']['name']
            site.create_or_get_category(category)
            page = render('category-create.html', data={'created': f'Создана категория {category}'})

        return http_status(), page


@add_route('/category-list/')
class CategoryList(DefaultPage):
    """docstring for CategoryList."""

    @debug()
    def render(self) -> Tuple[str]:
        page = render('category-list.html', categoty_list=site.categories)

        return http_status(), page


@add_route('/course-create/')
class CourseCreate(DefaultPage):
    """docstring for CourseCreate."""
    # type: str, name: str, categories: List[Category], eventtime: datetime, location: str
    @debug()
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


@add_route('/course-list/')
class CourseList(DefaultPage):
    """docstring for CourseList."""

    @debug()
    def render(self) -> Tuple[str]:
        page = render('course-list.html', course_list=site.courses) # course.name for course in course_list

        return http_status(), page


@add_route('/not-found-404/')
class NotFound404(DefaultPage):
    """docstring for NotFound404."""

    @debug()
    def render(self) -> Tuple[str]:
        return http_status(404), ' Error 404 page not Found'


@add_route('/')
class Index(DefaultPage):
    """docstring for Index."""

    @debug()
    def render(self) -> Tuple[str]:
        page = render('index.html', course_list=site.courses)

        return http_status(), page


@add_route('/contact/')
class Contact(DefaultPage):
    """docstring for Contact."""

    @debug()
    def render(self) -> Tuple[str]:
        page = render('contact.html')

        if self.request['REQUEST_METHOD'] == "POST":
            print(self.request['parsing_wsgi_data'])
            page = render('feed_back.html', data={'email': self.request['parsing_wsgi_data']['email']})

        return http_status(), page


@add_route('/copy-course/')
class CopyCourse(DefaultPage):
    """docstring for CopyCourse."""

    @debug()
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
                page = render('course-list.html', course_list=site.courses)
            else:
                Exception('There is no course: {name}')

        return http_status(), page

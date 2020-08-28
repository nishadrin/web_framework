import copy
from datetime import datetime
from typing import List, Optional
import abc

from education.models.category import Category


class CourseMixin:
    """docstring for CourseMixin."""
    __slots__ = () # нужен ли тут? TODO # вроде да, так как если
                   # в наследниках не будет slots, то тогда будет
                   # использован dict, и актуальности в slots не будет

    def clone(self):
        return copy.deepcopy(self)


class Course(CourseMixin, abc.ABC):
    """docstring for Course."""
    __slots__ = ('__name', '__eventtime', '__categories', '__location', )

    def __init__(self):
        self.__categories = list()

    @property
    def name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    @property
    def eventtime(self) -> Optional[datetime]:
        try:
            return self.__eventtime
        except AttributeError as e:
            return None

    def set_eventtime(self, eventtime: datetime):
        self.__eventtime = eventtime

    @property
    def category(self) -> List[Category]:
        return self.__categories

    def add_category(self, category: Category):
        self.__categories.append(category)

    def remove_category(self, category: Category):
        try:
            self.__categories.remove(category)
        except ValueError as e:
            print(f"We haven't {category.name} in {self.__name} course.")
            raise

    @property
    def location(self) -> Optional[str]:
        try:
            return self.__location
        except AttributeError as e:
            return None

    def set_location(self, location: str):
        self.__location = location

    @abc.abstractmethod
    def type_(self):
        pass


class Offline(Course):
    """docstring for Offline."""
    __slots__ = ('__type', )

    def type_(self):
        self.__type = 'offline'


class Webinar(Course):
    """docstring for Webinar."""
    __slots__ = ('__type', )

    def type_(self):
        self.__type = 'webinar'


class CourseFactory:
    """docstring for CoureFactory."""

    types = {
        'offline': Offline,
        'webinar': Webinar,
    }

    @classmethod
    def create(cls, type: str, name: str, categories: List[Category], eventtime: datetime, location:str):
        course = cls.types[type]()

        course.set_name(name)
        course.set_eventtime(eventtime)
        course.set_location(location)
        for category in categories:
            course.add_category(category)

        return course

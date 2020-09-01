from typing import List
from datetime import datetime

from education.models.category import Category
from education.models.course import CourseFactory, Course


class Site:
    """docstring for Site."""

    def __init__(self):
        self.courses = []
        self.categories = []

    def create_or_get_category(self, name: str) -> Category:
        for category in self.categories:
            if category.name == name:
                return category

        new_category = Category()
        new_category.set_name(name)
        self.categories.append(new_category)

        return new_category

    def get_category(self, name: str) -> Category:
        for category in self.categories:
            if category.name == name:
                return category

        raise Exception(f'There is no category: {name}')

    def create_course(self, type: str, name: str, categories: List[Category], \
                      eventtime: datetime, location:str) -> Course:
        for course in self.courses:
            if course.name == name:
                return course

        new_course = CourseFactory().create(type, name, categories, eventtime, location)
        self.courses.append(new_course)

        return new_course

    def add_category_to_course(self, course: Course, category: Category) -> Course:
        course.add_category(category)

        return course

    def get_course(self, name: str) -> Course:
        for course in self.courses:
            if course.name == name:
                return course

        raise Exception(f'There is no course: {name}')

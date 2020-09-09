from typing import List
from datetime import datetime

from education.models.category import Category
from education.models.course import CourseFactory, Course
from education.models.user import User, UserFactory


class Site:
    """docstring for Site."""

    def __init__(self):
        self.courses = []
        self.categories = []
        self.users = []

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

        for category in categories:
            category.add_course(new_course)

        return new_course

    def add_category_to_course(self, course: Course, category: Category) -> Course:
        course.add_category(category)

        return course

    def get_course(self, name: str) -> Course:
        for course in self.courses:
            if course.name == name:
                return course

        raise Exception(f'There is no course: {name}')

    def add_user_to_course(self, user: User, course: Course):
        user.add_course(course)
        course.add_user(user)

    def create_or_get_user(self, type, email, password, name, surname, middlename, telephone):
        for user in self.users:
            if user.email == email:
                return user

        new_user = UserFactory().create(type, email, password, name, surname, middlename, telephone)

        self.users.append(new_user)

        return new_user

    def get_user(self, email):
        for user in self.users:
            if user.email == email:
                return user

            raise Exception('There is no user: {email}')

    def remove_user_from_course(self, user, course):
        user.remove_course(course)
        course.remove_user(user)

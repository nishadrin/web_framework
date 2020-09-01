import abc
from typing import List, Optional


class User(abc.ABC):
    """docstring for User."""
    __slots__ = ('__email', '__password', '__name', '__surname', \
                '__middlename', '__telephone', '__courses', )

    def __init__(self):
        self.__courses = list()

    @property
    def courses(self) -> List[Optional]:
        return self.__courses

    @property
    def email(self):
        return self.__email

    def set_email(self, email: str):
        self.__email = email

    @property
    def password(self):
        return self.__password

    def set_password(self, password: str):
        self.__password = password

    @property
    def name(self):
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    @property
    def surname(self):
        return self.__surname

    def set_surname(self, surname: str):
        self.__surname = surname

    @property
    def middlename(self):
        return self.__middlename

    def set_middlename(self, middlename: str):
        self.__middlename = middlename

    @property
    def telephone(self):
        return self.__telephone

    def set_telephone(self, telephone: str):
        self.__telephone = telephone

    @abc.abstractmethod
    def type_(self):
        pass

    def add_course(self, course: Course):
        self.__courses.append(course)

    def remove_course(self, course: Course):
        try:
            self.__courses.remove(course)
        except ValueError as e:
            raise Exception(f"User {self.__name} is not in {course.name}.")



class Teacher(User):
    """docstring for Teacher."""
    __slots__ = ('__type', )

    def type_(self):
        self.__type = 'teacher'


class Student(User):
    """docstring for Student."""
    __slots__ = ('__type', )

    def type_(self):
        self.__type = 'student'


class UserFactory:
    """docstring for CoureFactory."""

    types = {
        'teacher': Teacher,
        'student': Student,
    }

    @classmethod
    def create(cls, type: str, email: str, password: str, name: str, \
              surname: str, middlename: str, telephone: str, \
              courses: List[Course]):
        user = cls.types[type]()

        user.set_email(email)
        user.set_password(password)
        user.set_name(name)
        user.set_surname(surname)
        user.set_middlename(middlename)
        user.set_telephone(telephone)

        for course in courses:
            user.add_course(course)

        return user

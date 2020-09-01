from typing import List, Optional

from course import Course

class Category:
    """docstring for Category."""

    def __init__(self):
        self.__courses = list()

    @property
    def name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name

    def add_course(self, course: Course):
        self.__courses.append(course)

    def remove_course(self, course: Course):
        try:
            self.__courses.remove(course)
        except ValueError as e:
            print(f"We haven't {course.name} in {self.__name} categories.")
            raise

    @property
    def courses(self) -> List[Optional]:
        return self.__courses

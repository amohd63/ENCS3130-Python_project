from typing import List

from Course import *


class Semester(Course):
    def __init__(self, year: str = None, semester: int = None, courses: List[Course] = None):
        super().__init__()
        self.__year = year
        self.__semester = semester
        self.courses = courses

    def get_year(self) -> str:
        return self.__year

    def set_year(self, year: str):
        self.__year = year

    def get_semester(self) -> int:
        return self.__semester

    def set_semester(self, semester: int):
        self.__semester = semester

    def __str__(self):
        courses = ' '
        for course in self.courses:
            courses += course.__str__() + ', '
        courses = courses[:len(courses) - 2]
        return str(self.__year) + '/' + str(self.__semester) + str(courses)

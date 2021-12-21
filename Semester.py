from Course import *


class Semester(Course):
    def __init__(self, year=None, semester=None, courses=None):
        super().__init__()
        self.__year = year
        self.__semester = semester
        self.courses = courses

    def get_year(self):
        return self.__year

    def set_year(self, year):
        self.__year = year

    def get_semester(self):
        return self.__semester

    def set_semester(self, semester):
        self.__semester = semester

    def __str__(self):
        courses = ' '
        for course in self.courses:
            courses += course.__str__() + ', '
        courses = courses[:len(courses) - 2]
        return str(self.__year) + '/' + str(self.__semester) + str(courses)

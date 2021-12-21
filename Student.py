from Semester import *


class Student(Semester):
    def __init__(self, student_id, semesters):
        super().__init__()
        self.__student_id = student_id
        self.__semesters = semesters


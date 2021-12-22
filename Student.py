from Semester import *


class Student(Semester):
    __remaining_courses = []
    __taken_hours = []
    __average_per_semester = []
    __overall_average = 0

    def __init__(self, student_id, semesters):
        super().__init__()
        self.__student_id = student_id
        self.__semesters = semesters


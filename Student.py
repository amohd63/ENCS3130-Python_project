from Semester import *


class Student(Semester):
    def __init__(self, student_id=None, semesters=None, taken_hours=None, remaining_courses=None,
                 average_per_semester=None, overall_average=None):
        super().__init__()
        self.__student_id = student_id
        self.__semesters = semesters
        self.__taken_hours = taken_hours
        self.__remaining_courses = remaining_courses
        self.__average_per_semester = average_per_semester
        self.__overall_average = overall_average

    def get_student_id(self):
        return self.__student_id

    def get_semester(self):
        return self.__semesters

    def get_remaining_courses(self):
        return self.__remaining_courses

    def get_taken_hours(self):
        return self.__taken_hours

    def get_average_per_semester(self):
        return self.__average_per_semester

    def get_overall_average(self):
        return self.__overall_average

    def set_student_id(self, student_id):
        self.__student_id = student_id

    def set_semesters(self, semesters):
        self.__semesters = semesters

    def set_taken_hours(self, taken_hours):
        self.__taken_hours = taken_hours

    def set_remaining_courses(self, remaining_courses):
        self.__remaining_courses = remaining_courses

    def set_average_per_semester(self, average_per_semester):
        self.__average_per_semester = average_per_semester

    def set_overall_average(self, overall_average):
        self.__overall_average = overall_average


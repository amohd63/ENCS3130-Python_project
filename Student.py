from typing import List

from Semester import *


class Student(Semester):
    def __init__(self, student_id: int = None, semesters: List[Semester] = None, taken_hours: int = None, remaining_courses: List[str] = None,
                 average_per_semester: List[float] = None, overall_average: float = None):
        super().__init__()
        self.__student_id = student_id
        self.__semesters = semesters
        self.__taken_hours = taken_hours
        self.__remaining_courses = remaining_courses
        self.__average_per_semester = average_per_semester
        self.__overall_average = overall_average

    def get_student_id(self) -> int:
        return self.__student_id

    def get_semesters(self) -> List[Semester]:
        return self.__semesters

    def get_remaining_courses(self) -> List[str]:
        return self.__remaining_courses

    def get_taken_hours(self) -> int:
        return self.__taken_hours

    def get_average_per_semester(self) -> List[float]:
        return self.__average_per_semester

    def get_overall_average(self) -> float:
        return self.__overall_average

    def set_student_id(self, student_id: int):
        self.__student_id = student_id

    def set_semesters(self, semesters: List[Semester]):
        self.__semesters = semesters

    def set_taken_hours(self, taken_hours: int):
        self.__taken_hours = taken_hours

    def set_remaining_courses(self, remaining_courses: List[str]):
        self.__remaining_courses = remaining_courses

    def set_average_per_semester(self, average_per_semester: List[float]):
        self.__average_per_semester = average_per_semester

    def set_overall_average(self, overall_average: float):
        self.__overall_average = overall_average


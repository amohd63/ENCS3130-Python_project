class Course:
    def __init__(self, course_id=None, grade=None):
        self.__course_id = course_id
        self.__grade = grade

    def get_course_id(self):
        return self.__course_id

    def get_grade(self):
        return self.__grade

    def set_course_id(self, course_id):
        self.__course_id = course_id

    def set_grade(self, grade):
        self.__grade = grade

    def get_course_hours(self):
        return int(self.__course_id[5])

    def __str__(self):
        return str(self.__course_id) + ' ' + str(self.__grade)

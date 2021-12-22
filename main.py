import os, re
import numpy as np
from copy import deepcopy
from Student import *


def admin_menu():
    print('1. Add a new record file')
    print('2. Add new semester with student course and grades')
    print('3. Update')
    print('4. Student statistics')
    print('5. Global statistics')
    print('6. Searching')
    return input('Enter option: ')


def student_menu():
    print('1. Student statistics')
    print('2. Global statistics')
    return input('Enter option: ')


def add_new_record(new_student_id):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    if new_student_id in files:
        raise Exception('Student already exists in the system!')
    if new_student_id.isdigit() and len(new_student_id) == 7:
        f = open(str(new_student_id), 'w+')
    else:
        raise Exception('Student ID is invalid!')


def add_student_information(courses_list, students):
    student_info = ''
    student_id = input('Student ID: ')
    if student_id.isdigit() and len(student_id) == 7:
        try:
            students.append(Student(int(student_id)))
        except Exception as e:
            if 'invalid' in str(e):
                print(str(e))
                return
        # we have to check if the semester doesn't exist before
        student = open(str(student_id), 'w')
        year = input('Year (start-end): ')
        semester = input('Semester (1, 2, 3): ')
        student_info += str(year) + '/' + str(semester) + ' ; '
        courses_grades = []
        print('You will be asked to enter courses and grades for each student.' +
              '\n' + 'Enter s or stop to end entering courses.')
        while True:
            course = input('Course ID: ')
            if course.lower() == 's' or course.lower() == 'stop':
                break
            if course not in courses_list:
                print('Course' + str(course) + ' it is not Computer Engineering course')
                continue
            else:
                grade = input('Grade: ')
                if grade.isdigit() and -1 < int(grade) < 100:
                    courses_grades.append(str(course) + ' ' + str(grade))
                else:
                    print('Grade: ' + str(grade) + ' is invalid')
                    continue
        for i in range(len(courses_grades)):
            student_info += courses_grades[i]
            if i != len(courses_grades) - 1:
                student_info += ', '
        try:
            semesters = []
            average_per_semester = []
            overall_average = 0
            s_semester, s_taken_hours, s_remaining_courses, s_semester_average = student_semester(student_info, courses_list)
            current_student = None
            for student in students:
                if student.get_student_id() == int(student_id):
                    current_student = student
                    break
            if current_student is None:
                semesters.append(s_semester)
                average_per_semester.append(s_semester_average)
                overall_average = sum(average_per_semester) / len(average_per_semester)
                students.append(Student(int(student_id), semesters, s_taken_hours, s_remaining_courses, average_per_semester, overall_average))
            else:
                semesters = current_student.get_semesters()
                average_per_semester = current_student.get_average_per_semester()
                taken_hours = current_student.get_taken_hours()
                remaining_courses = current_student.get_remaining_courses()
                semesters.append(s_semester)
                average_per_semester.append(s_semester_average)
                overall_average = sum(average_per_semester) / len(average_per_semester)
                taken_hours += s_taken_hours
                remaining_courses = set(remaining_courses).intersection(s_remaining_courses)
                current_student.set_semesters(semester)
                current_student.set_average_per_semester(average_per_semester)
                current_student.set_taken_hours(taken_hours)
                current_student.set_remaining_courses(remaining_courses)
                current_student.set_overall_average(overall_average)
            student.write(str(student_info))
        except Exception as e:
            print(str(e))
    else:
        raise Exception('Student ID is invalid!')


def update():
    print('test')


def student_semester(student, courses_list):
    if (';' or '-' or '/') not in student:
        raise Exception('Student information is not formatted.')
    year_semester, courses_grades = student.split(';')
    if not re.match("20[0-9]{2}-20[0-9]{2}/[1-3]", year_semester.replace(' ', '')):
        raise Exception('Year/Semester is not following the format.')
    #if ',' not in courses_grades: recheck
    #   raise Exception('Courses')
    courses_grades = courses_grades.split(',')
    if not all(re.match("ENCS|ENEE[2-5][1-4][0-9]{2} [0-9]{2}", course_grade) for course_grade in courses_grades):
        raise Exception('Course ID/grade is not formatted.')
    year, semester_number = year_semester.split('/')
    start_year, end_year = year.split('-')
    if semester_number.isdigit() and int(semester_number) not in range(1, 3):
        raise Exception('There are three semesters only (1, 2, 3).')
    if int(end_year) - int(start_year) != 1:
        raise Exception('The end year of the semester and the start must differ at one only.')
    courses, grades = map(list, zip(*(course_grade.split() for course_grade in courses_grades)))
    i = 0
    for course, grade in zip(courses, grades):  # not done
        if course not in courses_list or grade < 0:
            courses.pop(i)
            grades.pop(i)
            i -= 1
        i += 1
    student_courses = [Course(courses[i], grades[i]) for i in range(len(courses))]
    remaining_courses = set(courses_list).difference(courses)
    taken_hours = 0
    for course in student_courses:
        taken_hours += course.get_course_hours()
    np.array(grades, dtype=int)
    semester_average = sum(grades)/len(grades)
    semester = Semester(year, int(semester_number), student_courses)
    return semester, taken_hours, remaining_courses, semester_average


courses_list = []
students = []
with open('courses') as f:
    for course in f:
        courses_list.append(course.replace('\n', ''))

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for file in files:
    if file.isdigit() and len(file) == 7:
        lines = open(str(file), 'r').readlines()
        semesters = []
        taken_hours = 0
        remaining_courses = deepcopy(courses_list)
        average_per_semester = []
        overall_average = 0
        for line in lines:
            try:
                semester, s_taken_hours, s_remaining_courses, s_semester_average = student_semester(line, courses_list)
                semesters.append(semester)
                taken_hours += s_taken_hours
                remaining_courses = set(remaining_courses).intersection(s_remaining_courses)
                average_per_semester.append(s_semester_average)
            except Exception as e:
                print(str(e))
        overall_average = sum(average_per_semester) / len(average_per_semester)
        students.append(Student(int(file), semesters, taken_hours, remaining_courses, average_per_semester, overall_average))


# print('|-----------------------------------|'
#       + '\n|--------Login to the system--------|'
#       + '\n|-----------------------------------|'
#       + '\n'
#       + '\n|---------------Admin---------------|'
#       + '\n|---------------User----------------|\n')
# login_type = input("Login: ")
#
# print(files)

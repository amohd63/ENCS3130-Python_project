import os, re
import numpy as np
from copy import deepcopy
from Student import *
import matplotlib.pyplot as plt


def student_id_validation(student_id):
    if student_id.isdigit() and len(student_id) == 7:
        if re.match("1[0-2][0-9]{4}", student_id):
            return True
    return False


def student_year_semester_validation(student_year, student_semester):
    if '-' in student_year:
        start, end = student_year.split('-')
        start = start.replace(' ', '')
        end = end.replace(' ', '')
        student_semester = student_semester.replace(' ', '')
        if start.isdigit() and end.isdigit() and student_semester.isdigit():
            return int(end) - int(start) == 1 and int(student_semester) in range(1, 4)
    return False


def student_course_grade_validation(course_list, student_course, student_grade):
    if student_course in course_list and student_grade.isdigit() and -1 < int(student_grade) < 100:
        return True
    return False


def admin_menu():
    print('1. Add a new record file')
    print('2. Add new semester with student course and grades')
    print('3. Update')
    print('4. Student statistics')
    print('5. Global statistics')
    print('6. Searching\n')


def student_menu():
    print('1. Student statistics')
    print('2. Global statistics\n')


def add_new_record(new_student_id: int):
    if student_id_validation(str(new_student_id)):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        if str(new_student_id) in files:
            raise Exception('Student already exists in the system!')
        f = open(str(new_student_id), 'w+')
        f.close()
    else:
        raise Exception('Student ID is invalid!')


def add_student_information(courses_list: List[str], students: List[Student]):
    student_info = ''
    student_id = input('Student ID: ')
    if student_id_validation(str(student_id)):
        try:
            add_new_record(int(student_id))
        except Exception as e:
            if 'invalid' in str(e):
                raise Exception(str(e))
        student_file = open(str(student_id), 'a')
        year = input('Year (start-end): ')
        semester_number = input('Semester (1, 2, 3): ')
        if student_year_semester_validation(year, semester_number):
            current_student = next((student for student in students if student.get_student_id() == int(student_id)), None)
            if current_student is not None:
                flag = False
                for semester in current_student.get_semesters():
                    if semester.get_year() == year and semester.get_semester() == int(semester_number):
                        flag = True
                if flag:
                    raise Exception('Semester already exists!')
            student_info += str(year) + '/' + str(semester_number) + ' ; '
            courses_grades = []
            print('\nYou will be asked to enter courses and grades for each student.' +
                  '\n' + 'Enter s or stop to end entering courses.\n')
            while True:
                course = input('Course ID: ')
                if course.lower() == 's' or course.lower() == 'stop':
                    break
                grade = input('Grade: ')
                if student_course_grade_validation(courses_list, course, grade):
                    courses_grades.append(str(course) + ' ' + str(grade))
                else:
                    print('Course: ' + str(course) + ', grade: ' + str(grade) + ' are invalid')
                    continue
            for i in range(len(courses_grades)):
                student_info += courses_grades[i]
                if i != len(courses_grades) - 1:
                    student_info += ', '
            semesters = []
            average_per_semester = []
            overall_average = 0
            try:
                s_semester, s_taken_hours, s_remaining_courses, s_semester_average = student_semester(student_info, courses_list)
                if current_student is None:
                    semesters.append(s_semester)
                    average_per_semester.append(s_semester_average)
                    overall_average = s_semester_average
                    students.append(Student(int(student_id), semesters, s_taken_hours, s_remaining_courses, average_per_semester, overall_average))
                else:
                    semesters = current_student.get_semesters()
                    average_per_semester = current_student.get_average_per_semester()
                    taken_hours = current_student.get_taken_hours()
                    remaining_courses = current_student.get_remaining_courses()
                    overall_average = current_student.get_overall_average()

                    sum_of_averages = (overall_average * taken_hours) + (s_semester_average * s_taken_hours)
                    semesters.append(s_semester)
                    average_per_semester.append(s_semester_average)
                    taken_hours += s_taken_hours
                    overall_average = sum_of_averages / taken_hours
                    remaining_courses = set(remaining_courses).intersection(s_remaining_courses)

                    current_student.set_semesters(semesters)
                    current_student.set_average_per_semester(average_per_semester)
                    current_student.set_taken_hours(taken_hours)
                    current_student.set_remaining_courses(list(remaining_courses))
                    current_student.set_overall_average(overall_average)
                student_file.write('\n' + str(student_info))
            except Exception as e:
                raise Exception(str(e))
            finally:
                student_file.close()
        else:
            raise Exception('Student Year/semester are invalid!')
    else:
        raise Exception('Student ID is invalid!')


def update(course_list, students):
    student_id = input('Enter student ID: ')
    student_course = input('Enter course ID: ')
    new_grade = input('Enter grade: ')
    if student_id_validation(student_id) and student_course_grade_validation(course_list, student_course, new_grade):
        student = None
        for std in students:
            if std.get_student_id() == int(student_id):
                student = std
                break
        if student is not None:
            semesters = student.get_semesters()
            ave_per_semester = student.get_average_per_semester()
            index = 0
            for i in range(len(semesters)):
                for course in semesters[i].get_courses():
                    if course.get_course_id() == student_course:
                        index = i
                        course.set_grade(int(new_grade))
            grades_sum = 0
            courses = semesters[index].get_courses()
            for course in courses:
                grades_sum += int(course.get_grade())
            ave_per_semester[index] = grades_sum / len(courses)
            overall_average = sum(ave_per_semester) / len(ave_per_semester)
            student.set_average_per_semester(ave_per_semester)
            student.set_overall_average(overall_average)
            f = open(str(student_id), 'r+')
            lines = f.readlines()
            year_semester = str(semesters[index].get_year()) + '/' + str(semesters[index].get_semester())
            index = 0
            for i in range(len(lines)):
                if year_semester in lines[i]:
                    index = i
                    break
            new_line = re.sub(str(student_course) + ' [0-9]{1,2}', str(student_course) + ' ' + str(new_grade),
                              lines[index])
            lines[index] = new_line
            f.close()
            f = open(str(student_id), 'w')
            f.writelines(lines)


def student_statistics(students):
    student_id = input('Enter student ID: ')
    if student_id.isdigit() and len(student_id) == 7:
        student_id = int(student_id)
        std = None
        for student in students:
            if student.get_student_id() == student_id:
                std = student
        print('Taken hours: ' + str(std.get_taken_hours()))
        print('Remaining courses: ' + str(std.get_remaining_courses()))
        print('Average per semester: ' + str(std.get_average_per_semester()))
        print('Overall average: ' + str(std.get_overall_average()))


def global_statistics(students):
    averages_sum = 0
    hours_sum = 0
    num_of_semesters = 0
    for student in students:
        averages_sum += student.get_overall_average()
        hours_sum += student.get_taken_hours()
        num_of_semesters += len(student.get_semesters())
    overall_students_average = averages_sum / len(students)
    average_hours_per_semester = hours_sum / num_of_semesters
    print('Overall students average: ' + str(overall_students_average))
    print('Average hours per semester: ' + str(average_hours_per_semester))
    data = []
    for student in students:
        for semester in student.get_semesters():
            for course in semester.get_courses():
                data.append(course.get_grade())
    plt.title('Histogram Grades')
    plt.hist(data, rwidth=.8, bins=np.arange(min(data), max(data) + 2) - 0.5)
    plt.xticks(np.arange(min(data), max(data) + 1, 1.0))
    plt.ylabel('Count')
    plt.grid()
    plt.show()


def searching(students):
    print('|1. Search Based On Average.|' +
          '\n |2. Search Based On Taken Hours.|' +
          '\n |else. Back.|')
    searching_option = input('Enter option: ')
    if searching_option.isdigit() and int(searching_option) in range(4):
        searching_option = int(searching_option)
    if searching_option == 1:
        avg = input("Please Enter the average: ")
        print('|1. above the Average.|' +
              '\n |2. below the Average.|' +
              '\n |3. equal the Average.|' +
              '\n |else. Back.|')
        avgOption = input("Please Enter the average option: ")
        above = []
        below = []
        equal = []
        for student in students:
            if int(student.get_overall_average()) > int(avg):
                above.append(student.get_student_id())
            elif int(student.get_overall_average()) < int(avg):
                below.append(student.get_student_id())
            else:
                equal.append(student.get_student_id())
        if avgOption.isdigit() and int(avgOption) in range(4):
            avgOption = int(avgOption)
            if avgOption == 1:
                print(above)
            elif avgOption == 2:
                print(below)
            elif avgOption == 3:
                print(equal)
    elif searching_option == 2:
        takingHours = input("Please Enter the number of taking Hours: ")
        print('|1. above the number of taking Hours.|' +
              '\n |2. below the number of taking Hours.|' +
              '\n |3. equal the number of taking Hours.|' +
              '\n |else. Back.|')
        takingHoursOption = input("Please Enter the option: ")
        aboveHours = []
        belowHours = []
        equalHours = []
        for student in students:
            if int(student.get_taken_hours()) > int(takingHours):
                aboveHours.append(student.get_student_id())
            elif int(student.get_taken_hours()) < int(takingHours):
                belowHours.append(student.get_student_id())
            else:
                equalHours.append(student.get_student_id())
        if takingHoursOption.isdigit() and int(takingHoursOption) in range(4):
            avgOption = int(takingHoursOption)
            if avgOption == 1:
                print(aboveHours)
            elif avgOption == 2:
                print(belowHours)
            elif avgOption == 3:
                print(equalHours)


def student_semester(student, courses_list):
    if (';' or '-' or '/') not in student:
        raise Exception('Student information is not formatted.')
    year_semester, courses_grades = student.split(';')
    courses_grades = courses_grades.split(',')
    year, semester_number = year_semester.split('/')
    if not student_year_semester_validation(year, semester_number):
        raise Exception('Year/Semester is not following the format.')
    courses, grades = map(list, zip(*(course_grade.split() for course_grade in courses_grades)))
    i = 0
    for course, grade in zip(courses, grades):  # not done
        if not student_course_grade_validation(courses_list, course, grade):
            courses_grades.pop(i)
            i -= 1
        i += 1
    courses, grades = map(list, zip(*(course_grade.split() for course_grade in courses_grades)))
    grades = np.array(grades, dtype=float)
    student_courses = [Course(courses[i], grades[i]) for i in range(len(courses))]
    remaining_courses = set(courses_list).difference(courses)
    taken_hours = 0
    grades_sum = 0
    for course in student_courses:
        taken_hours += int(course.get_course_hours())
        grades_sum += (int(course.get_grade()) * int(course.get_course_hours()))
    semester_average = grades_sum / taken_hours
    semester = Semester(year, int(semester_number), student_courses)
    return semester, taken_hours, list(remaining_courses), semester_average


courses_list = []
students = []

with open('courses') as f:
    for course in f:
        courses_list.append(course.replace('\n', ''))

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for file in files:
    if student_id_validation(file) and os.stat(file).st_size != 0:
        lines = open(str(file), 'r').readlines()
        semesters = []
        taken_hours = 0
        remaining_courses = deepcopy(courses_list)
        average_per_semester = []
        overall_average = 0
        sum_of_averages = 0
        for line in lines:
            try:
                semester, s_taken_hours, s_remaining_courses, s_semester_average = student_semester(line, courses_list)
                semesters.append(semester)
                taken_hours += s_taken_hours
                remaining_courses = set(remaining_courses).intersection(s_remaining_courses)
                average_per_semester.append(s_semester_average)
                sum_of_averages += (s_semester_average * s_taken_hours)
            except Exception as e:
                print(str(e))
        overall_average = sum_of_averages/taken_hours
        students.append(
            Student(int(file), semesters, taken_hours, remaining_courses, average_per_semester, overall_average))

print('|-----------------------------------|'
      + '\n|--------Login to the system--------|'
      + '\n|-----------------------------------|'
      + '\n'
      + '\n|---------------Admin---------------|'
      + '\n|---------------Student-------------|\n')
login_type = input("Login: ")
print('\n')
try:
    if login_type.lower() == 'admin':
        admin_menu()
        option = input('Enter option: ')
        if option.isdigit() and int(option) in range(7):
            option = int(option)
            if option == 1:
                new_student_id = int(input('Enter student ID: '))
                add_new_record(new_student_id)
            elif option == 2:
                add_student_information(courses_list, students)
            elif option == 3:
                update(courses_list, students)
            elif option == 4:
                student_statistics(students)
            elif option == 5:
                global_statistics(students)
            elif option == 6:
                searching(students)
        else:
            exit(1)
    elif login_type.lower() == 'student':
        student_menu()
    else:
        'Not supported.'
except Exception as e:
    print('Exception: ' + str(e))

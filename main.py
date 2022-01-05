import os, re
import numpy as np
from copy import deepcopy
from Student import *
import matplotlib.pyplot as plt


# checks if student id is valid
def student_id_validation(student_id):
    # student id must be numeric and consisting of 7 digits only
    if student_id.isdigit() and len(student_id) == 7:
        # student class is in range 100 - 121
        if re.match("1[0-2][0-9]{4}", student_id) or re.match("1[0-2][0-1]{4}", student_id):
            return True
    return False


# checks if year of the semester is valid and the semester is one of 1,2,3
def student_year_semester_validation(student_year, student_semester):
    # years must be split by -
    if '-' in student_year:
        start, end = student_year.split('-')
        start = start.replace(' ', '')
        end = end.replace(' ', '')
        student_semester = student_semester.replace(' ', '')
        # both must be numeric
        if start.isdigit() and end.isdigit() and student_semester.isdigit():
            # semester year must defer by one only, and semester is 1,2, or 3
            return int(end) - int(start) == 1 and int(student_semester) in range(1, 4)
    return False


# checks if course is provided or not and grade is valid
def student_course_grade_validation(course_list, student_course, student_grade):
    # course must be provided by computer engineering department and grade in range 0 - 99
    if student_course in course_list and student_grade.isdigit() and -1 < int(student_grade) < 100:
        return True
    return False


# admin menu
def admin_menu():
    print('\n1. Add a new record file')
    print('2. Add new semester with student course and grades')
    print('3. Update')
    print('4. Student statistics')
    print('5. Global statistics')
    print('6. Search')
    print('7. Exit')


# student menu
def student_menu():
    print('\n1. Student statistics')
    print('2. Global statistics')
    print('3. Exit')


# creates new file for new student
def add_new_record(new_student_id: int):
    # student's id must be valid
    if student_id_validation(str(new_student_id)):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        # if student is in the system, error is raised
        if str(new_student_id) in files:
            raise Exception('Student already exists in the system!')
        f = open(str(new_student_id), 'w+')
        f.close()
    # if id is invalid, error is raised
    else:
        raise Exception('Student ID is invalid!')


# adds new semester to an existing student
def add_student_information(courses_list: List[str], students: List[Student]):
    student_info = ''
    student_id = input('Student ID: ')
    # checks if the entered id is valid
    if student_id_validation(str(student_id)):
        # checks if student exists before or not, if not it will be created
        try:
            add_new_record(int(student_id))
            print('Student with ID (' + str(student_id) + ') is added to the system, add his information.')
        except Exception as e:
            if 'invalid' in str(e):
                raise Exception(str(e))
        student_file = open(str(student_id), 'a')
        year = input('Year (start-end): ')
        semester_number = input('Semester (1, 2, 3): ')
        # checks if entered year and semester are valid
        if student_year_semester_validation(year, semester_number):
            # gets the student's object with the entered id
            current_student = next((student for student in students if student.get_student_id() == int(student_id)),
                                   None)
            # checks if the entered year and semester doesn't exist
            if current_student is not None:
                flag = False
                # iterates over all student's semesters
                for semester in current_student.get_semesters():
                    if semester.get_year() == year and semester.get_semester() == int(semester_number):
                        flag = True
                # if year and semester are found, error is raised
                if flag:
                    raise Exception('Semester already exists!')
            student_info += str(year) + '/' + str(semester_number) + ' ; '
            courses_grades = []
            print('\nYou will be asked to enter courses and grades for each student.' +
                  '\n' + 'Enter exit to end entering courses.\n')
            total_hours = 0
            # student must register at least 12 hours or 18 hours per semester
            # so the system asks the user to enter courses within 12-18 hours
            while total_hours < 18:
                course = input('Course ID: ')
                # if user finishes entering courses
                if course.lower() == 'exit' and 12 < total_hours < 18:
                    break
                elif course.lower() == 'exit' and total_hours < 12:
                    print('You must add at least 12 hours')
                grade = input('Grade: ')
                # to check the course and grade are valid
                if student_course_grade_validation(courses_list, course, grade):
                    total_hours += int(course[5])
                    if total_hours > 18:
                        print('You cant register more than 18 hours')
                        break
                    courses_grades.append(str(course) + ' ' + str(grade))
                # if they are not valid, the course will not be registered
                else:
                    print('Course: ' + str(course) + ', grade: ' + str(grade) + ' are invalid')
                    continue
            # converts all entered courses to string
            for i in range(len(courses_grades)):
                student_info += courses_grades[i]
                # if it reaches the end of the courses, not comma is added
                if i != len(courses_grades) - 1:
                    student_info += ', '
            semesters = []
            average_per_semester = []
            overall_average = 0
            # adds the new semester to the student's object
            try:
                # gets semester as object, calculates taken hours and semester average, and finds remaining course
                s_semester, s_taken_hours, s_remaining_courses, s_semester_average = student_semester(student_info,
                                                                                                      courses_list)
                # if student is newly created or doesn't have  any semesters before
                if current_student is None:
                    semesters.append(s_semester)
                    average_per_semester.append(s_semester_average)
                    overall_average = s_semester_average
                    students.append(
                        Student(int(student_id), semesters, s_taken_hours, s_remaining_courses, average_per_semester,
                                overall_average))
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
                    overall_average = round(sum_of_averages / taken_hours, 2)
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


# updates student's semester
def update(course_list, students):
    student_id = input('Enter student ID: ')
    student_course = input('Enter course ID: ')
    new_grade = input('Enter grade: ')
    # checks if entered id, course id and grade are valid
    if student_id_validation(student_id) and student_course_grade_validation(course_list, student_course, new_grade):
        student = None
        # finds student with given id
        for std in students:
            if std.get_student_id() == int(student_id):
                student = std
                break
        # in case student with entered id exists
        if student is not None:
            semesters = student.get_semesters()
            ave_per_semester = student.get_average_per_semester()
            index = 0
            flag = False
            current_course = None
            # finds the student's course and updates the old grade
            for i in range(len(semesters)):
                for course in semesters[i].get_courses():
                    if course.get_course_id() == student_course:
                        index = i
                        current_course = course
                        flag = True
            # if entered course is not taken previously
            if flag:
                current_course.set_grade(int(new_grade))
                grades_sum = 0
                courses = semesters[index].get_courses()
                # finds new semester grades summation
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
                # finds the line that contains the grade
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
            else:
                raise Exception('Entered course is not registered by student, you cant update')
        else:
            raise Exception('Entered information is invalid')


# finds student statistics
def student_statistics(students, student_id):
    # checks student id
    if student_id_validation(student_id):
        student_id = int(student_id)
        std = None
        # finds student with current id
        for student in students:
            if student.get_student_id() == student_id:
                std = student
        # in case there are not students
        if std is not None:
            print('Taken hours: ' + str(std.get_taken_hours()))
            print('Remaining courses: ' + str(std.get_remaining_courses()))
            print('Average per semester: ' + str(std.get_average_per_semester()))
            print('Overall average: ' + str(std.get_overall_average()))
        else:
            print('Student with ID (' + str(student_id) + ') is not in the system')


# finds global statistics
def global_statistics(students):
    averages_sum = 0
    hours_sum = 0
    num_of_semesters = 0
    # iterates over all students to find summation of averages, hours, and number of semesters
    for student in students:
        averages_sum += student.get_overall_average()
        hours_sum += student.get_taken_hours()
        num_of_semesters += len(student.get_semesters())
    overall_students_average = round(averages_sum / len(students), 2)
    average_hours_per_semester = round(hours_sum / num_of_semesters, 2)
    print('Overall students average: ' + str(overall_students_average))
    print('Average hours per semester: ' + str(average_hours_per_semester))
    data = []
    # finds all grades in order to plot them
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
          '\n|2. Search Based On Taken Hours.|' +
          '\n|else. Back.|')
    searching_option = input('Enter option: ')
    if searching_option.isdigit() and int(searching_option) in range(1, 3):
        searching_option = int(searching_option)
    if searching_option == 1:
        avg = input("Please Enter the average: ")
        print('|1. above the Average.|' +
              '\n|2. below the Average.|' +
              '\n|3. equal the Average.|' +
              '\n|else. Back.|')
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
              '\n|2. below the number of taking Hours.|' +
              '\n|3. equal the number of taking Hours.|' +
              '\n|else. Back.|')
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


# creates semester object, calculates average and taken hours, and finds remaining courses
def student_semester(student, courses_list):
    # each course line must have three splitters (- between years), (/ between years and semester)
    # (; between grades and year/semester)
    if (';' or '-' or '/') not in student:
        raise Exception('Student information is not formatted.')
    year_semester, courses_grades = student.split(';')
    courses_grades = courses_grades.split(',')
    year, semester_number = year_semester.split('/')
    # in case year or semester are not valid
    if not student_year_semester_validation(year, semester_number):
        raise Exception('Year/Semester is not following the format.')
    courses, grades = map(list, zip(*(course_grade.split() for course_grade in courses_grades)))
    i = 0
    # drops all courses which are not provided by computer engineering department
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
    # finds number of taken hours and summation of grades to find the average
    for course in student_courses:
        taken_hours += int(course.get_course_hours())
        grades_sum += (int(course.get_grade()) * int(course.get_course_hours()))
    semester_average = round(grades_sum / taken_hours, 2)
    semester = Semester(year, int(semester_number), student_courses)
    return semester, taken_hours, list(remaining_courses), semester_average


courses_list = ['ENCS2340', 'ENEE2307', 'ENCS2110', 'ENCS211', 'ENCS238', 'ENCS311', 'ENCS338', 'ENEE3302', 'ENCS533',
                'ENCS339', 'ENCS411', 'ENCS431', 'ENCS434', 'ENCS436', 'ENCS438', 'ENCS401', 'ENCS412', 'ENCS413',
                'ENCS437', 'ENCS531', 'ENEE4103', 'ENCS330', 'ENCS532', 'ENCS524', 'ENCS520', 'ENCS521', 'ENCS515',
                'ENCS530', 'ENEE339', 'ENEE236', 'ENEE2302', 'ENCS2380', 'ENEE2304', 'ENEE2312', 'ENCS3130', 'ENCS3310',
                'ENCS3390', 'ENCS4110', 'ENEE2360', 'ENEE3309', 'ENCS3320', 'ENCS3330', 'ENCS3340', 'ENCS4370',
                'ENEE2103', 'ENEE4113', 'ENCS4130', 'ENCS4210', 'ENCS4310', 'ENCS4320', 'ENCS4380', 'ENCS4330',
                'ENCS4300', 'ENCS5140', 'ENCS5200', 'ENCS5150', 'ENCS5300', 'ENCS5321', 'ENCS5322', 'ENCS5323',
                'ENCS5331', 'ENCS5332', 'ENCS5333', 'ENCS5341', 'ENCS5342', 'ENCS5343', 'ENCS5321', 'ENCS5121',
                'ENCS5131', 'ENCS5141', 'ENCS5324', 'ENCS5325', 'ENCS5326', 'ENCS5327', 'ENCS5334', 'ENCS5335',
                'ENCS5336', 'ENCS5344', 'ENCS5345', 'ENCS5346', 'ENCS5347', 'ENCS5348', 'ENCS5349', 'ENCS5399']
students = []
# gets all files in the project directory
files = [f for f in os.listdir('.') if os.path.isfile(f)]
# iterates over all files to find the students
for file in files:
    # checks if file represents a student or not and it's not empty
    if student_id_validation(file) and os.stat(file).st_size != 0:
        lines = open(str(file), 'r').readlines()
        semesters = []
        taken_hours = 0
        remaining_courses = deepcopy(courses_list)
        average_per_semester = []
        overall_average = 0
        sum_of_averages = 0
        # takes all semesters
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
        overall_average = round(sum_of_averages / taken_hours, 2)
        students.append(
            Student(int(file), semesters, taken_hours, remaining_courses, average_per_semester, overall_average))

print('|-----------------------------------|'
      + '\n|--------Login to the system--------|'
      + '\n|-----------------------------------|'
      + '\n'
      + '\n|---------------Admin---------------|'
      + '\n|---------------Student-------------|\n')
login_type = input("Login: ")
print('')
# if admin logins
if login_type.lower() == 'admin':
    while True:
        try:
            admin_menu()
            option = input('Enter option: ')
            print('')
            # checks if option is valid
            if option.isdigit() and int(option) in range(1, 8):
                option = int(option)
                # add new record option
                if option == 1:
                    new_student_id = int(input('Enter student ID: '))
                    add_new_record(new_student_id)
                # add student information option
                elif option == 2:
                    add_student_information(courses_list, students)
                # update option
                elif option == 3:
                    update(courses_list, students)
                # student statistics option
                elif option == 4:
                    student_id = input('Enter your ID: ')
                    student_statistics(students, student_id)
                # global statistics option
                elif option == 5:
                    global_statistics(students)
                # searching option
                elif option == 6:
                    searching(students)
                elif option == 7:
                    exit(1)
                else:
                    print('Not supported!')
            else:
                exit(1)
        except Exception as e:
            print('Exception: ' + str(e))
# if student logins
elif login_type.lower() == 'student':
    # student must login by his id
    student_id = input('Enter your ID: ')
    while True:
        try:
            student_menu()
            option = input('Enter option: ')
            print('')
            if option.isdigit() and int(option) in range(1, 4):
                option = int(option)
                # student statistics option
                if option == 1:
                    student_statistics(students, student_id)
                # global statistics option
                elif option == 2:
                    global_statistics(students)
                elif option == 3:
                    exit(1)
                else:
                    print('Not supported!')
            else:
                exit(1)
        except Exception as e:
            print('Exception: ' + str(e))
else:
    'Not supported.'

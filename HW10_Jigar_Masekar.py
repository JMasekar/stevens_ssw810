"""
@author- Jigar Masekar

   HW10 Code containing classes Student, Instructor, Major and Repository for the second iteration of project

"""

import os
from collections import defaultdict
from prettytable import PrettyTable
from Reader import file_reading_gen


class Repository:
    """ class Repository containing information of students, instructors, grades and majors of a single university"""

    def __init__(self, dir_path, pt=True):

        self._dir_path = dir_path
        self._students = dict()
        self._instructors = dict()
        self._majors = dict()

        try:

            self.read_instructors(os.path.join(dir_path, 'instructors.txt'))
            self.read_majors(os.path.join(dir_path, 'majors.txt'))
            self.read_students(os.path.join(dir_path, 'students.txt'))
            self.read_grades(os.path.join(dir_path, 'grades.txt'))

        except ValueError as ve:
            print(ve)
        except FileNotFoundError as e:
            print(e)

        if pt:
            print("\nMajor Summary")
            self.major_ptable()

            print("\nStudent Summary")
            self.student_ptable()

            print("\nInstructor Summary")
            self.instructor_ptable()

    def read_students(self, path):
        """ read student data """

        try:
            for cwid, name, major in file_reading_gen(path, 3, sep=';', header=True):
                if cwid in self._students:
                    print(f"{cwid} is already there")
                else:
                    self._students[cwid] = Student(cwid, name, major, self._majors[major])
        except ValueError as e:
            print(e)

    def read_instructors(self, path):
        """ read instructor data """

        try:
            for cwid, name, dept in file_reading_gen(path, 3, sep='|', header=True):
                if cwid in self._instructors:
                    print(f"{cwid} present already.")
                else:
                    self._instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as e:
            print(e)

    def read_grades(self, path):
        """ read grades """

        try:

            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='|', header=True):

                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade)
                else:
                    print(f"Found grade for an unknown student '{student_cwid}'.")

                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_student(course)
                else:
                    print(f"Error! Instructor CWID '{instructor_cwid}' does not exist.")

        except ValueError as e:
            print(e)

    def read_majors(self, path):
        """ read majors """

        try:

            for major, flag, course in file_reading_gen(path, 3, sep='\t', header=True):

                if major in self._majors:
                    self._majors[major].add_course(flag, course)
                else:
                    self._majors[major] = Major(major)
                    self._majors[major].add_course(flag, course)

        except ValueError as e:
            print(e)

    def student_ptable(self):
        """ print student pretty table """

        pt = PrettyTable(field_names=Student.pt_hdr)
        for student in self._students.values():
            pt.add_row(student.student_summary())

        print(pt)

    def instructor_ptable(self):
        """ print instructor pretty table """

        pt = PrettyTable(field_names=Instructor.pt_hdr)
        for instructor in self._instructors.values():
            for row in instructor.instructor_summary():
                pt.add_row(row)

        print(pt)

    def major_ptable(self):
        """ print majors pretty table """

        pt = PrettyTable(field_names=Major.pt_hdr)
        for major in self._majors.values():
            pt.add_row(major.major_summary())

        print(pt)


class Student:
    """ class Student containing information for students """

    pt_hdr = ["CWID", "NAME", "MAJOR", "COMPLETED COURSES", "REQUIRED COURSES", "REQUIRED ELECTIVES"]

    def __init__(self, cwid, name, major, majors):

        self._cwid = cwid
        self._name = name
        self._major = major
        self._majors = majors

        self._courses = dict()

    def add_course(self, course, grade):
        """ adding course for a student """

        passing_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        if grade in passing_grades:
            self._courses[course] = grade

    def student_summary(self):
        """ summarising student details that will go in pretty tables"""

        completed_courses, req_courses, req_electives = self._majors.course_checking(self._courses)
        return [self._cwid, self._name, self._major, completed_courses, req_courses, req_electives]


class Instructor:
    """ class Instructor containing information for instructors """

    pt_hdr = ["CWID", "NAME", "DEPT", "COURSE", "NUMBER OF STUDENTS"]

    def __init__(self, cwid, name, dept):

        self._cwid = cwid
        self._name = name
        self._dept = dept

        self._courses = defaultdict(int)

    def add_student(self, course):
        """ adding a student undertaking course from a professor """

        self._courses[course] += 1

    def instructor_summary(self):
        """ summarising instructor details that will go in pretty tables"""

        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]


class Major:
    """ class Major containing information regarding required courses and electives """

    pt_hdr = ["DEPT", "REQUIRED COURSES", "REQUIRED ELECTIVES"]

    def __init__(self, dept, pc=None):

        self._dept = dept
        self._required = set()
        self._electives = set()

        if pc is None:
            self._passing_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}
        else:
            self._passing_grades = pc

    def add_course(self, flag, course):
        """ separating courses into Required and Electives """

        if flag == 'E':
            self._electives.add(course)
        elif flag == 'R':
            self._required.add(course)
        else:
            raise ValueError(f"No such '{course}' course found.")

    def course_checking(self, courses):
        """ taken and pending course calculation """

        completed_courses = {course for course, grade in courses.items() if grade in self._passing_grades}

        if completed_courses == "{}":
            return [completed_courses, self._required, self._electives]
        else:
            req_courses = self._required - completed_courses

            if self._electives.intersection(completed_courses):
                req_electives = None
            else:
                req_electives = self._electives

            return [completed_courses, req_courses, req_electives]

    def major_summary(self):
        """ summarising majors details that will go in pretty tables"""

        return [self._dept, self._required, self._electives]


def main():

    stevens = r"/Users/jigar/Documents/SSW 810/Project/PHW10"

    Repository(stevens)


if __name__ == '__main__':
    main()

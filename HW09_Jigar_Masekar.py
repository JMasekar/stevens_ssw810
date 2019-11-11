"""
@author- Jigar Masekar

   HW09 Codes containing classes Student, Instructor and Repository for first iteration of project

"""

import os
from collections import defaultdict
from prettytable import PrettyTable
from Reader import file_reading_gen


class Student:
    """ class Student containing information for students """

    pt_hdr = ["CWID", "Name", "Completed Courses"]

    def __init__(self, cwid, name, major):

        self.cwid = cwid
        self.name = name
        self.major = major

        self.courses = dict()

    def add_course(self, course, grade):
        """ adding course for a student """
        self.courses[course] = grade

    def student_summary(self):
        """ summarising student details that will go in pretty tables"""
        return [self.cwid, self.name, sorted(self.courses.keys())]


class Instructor:
    """ class Instructor containing information for instructors """

    pt_hdr = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid, name, dept):

        self.cwid = cwid
        self.name = name
        self.dept = dept

        self.courses = defaultdict(int)

    def add_student(self, course):
        """ adding a student undertaking course from a professor """

        self.courses[course] += 1

    def instructor_summary(self):
        """ summarising instructor details that will go in pretty tables"""

        for course, count in self.courses.items():
            yield [self.cwid, self.name, self.dept, course, count]


class Repository:
    """ class Repository containing information of students, instructors and grades of a single university"""

    def __init__(self, dir_path, pt=True):

        self.dir_path = dir_path
        self.students = dict()
        self.instructors = dict()

        try:
            self.read_students(os.path.join(dir_path, 'students.txt'))
            self.read_instructors(os.path.join(dir_path, 'instructors.txt'))
            self.read_grades(os.path.join(dir_path, 'grades.txt'))
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as e:
            print(e)

        if pt:
            print("\nStudent Summary")
            self.student_ptable()

            print("\nInstructor Summary")
            self.instructor_ptable()

    def read_students(self, path):
        """ read student data """

        for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=False):
            self.students[cwid] = Student(cwid, name, major)

    def read_instructors(self, path):
        """ read instructor data """

        for cwid, name, dept in file_reading_gen(path, 3, sep='\t', header=False):
            self.instructors[cwid] = Instructor(cwid, name, dept)

    def read_grades(self, path):
        """ read grades """

        for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='\t', header=False):

            if student_cwid in self.students:
                self.students[student_cwid].add_course(course, grade)
            else:
                print(f"Found grade for unknown student '{student_cwid}")

            if instructor_cwid in self.instructors:
                self.instructors[instructor_cwid].add_student(course)
            else:
                print("Error!")

    def student_ptable(self):
        """ print student pretty table """

        pt = PrettyTable(field_names=Student.pt_hdr)
        for student in self.students.values():
            pt.add_row(student.student_summary())

        print(pt)

    def instructor_ptable(self):
        """ print instructor pretty table """

        pt = PrettyTable(field_names=Instructor.pt_hdr)
        for instructor in self.instructors.values():
            for row in instructor.instructor_summary():
                pt.add_row(row)

        print(pt)


def main():

    stevens = "/Users/jigar/Documents/SSW 810/Project/Text Files"

    Repository(stevens)


if __name__ == '__main__':
    main()

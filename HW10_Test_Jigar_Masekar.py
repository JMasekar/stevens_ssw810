""" Test Cases for HW10_Jigar_Masekar.py """

import unittest

from HW10_Jigar_Masekar import Repository


class TestRep(unittest.TestCase):

    def test_rep(self):
        test_path = "/Users/jigar/Documents/SSW 810/Project/PHW10"
        self.rep = Repository(test_path, False)

    def test_student_data(self):
        """ testing data in student pretty table """

        test_path = "/Users/jigar/Documents/SSW 810/Project/PHW10"
        self.rep = Repository(test_path, False)

        expected = [['10103', 'Baldwin, C', 'SFEN', {'SSW 564', 'CS 501', 'SSW 567', 'SSW 687'}, {'SSW 555', 'SSW 540'}, None],
                    ['10115', 'Wyatt, X', 'SFEN', {'SSW 564', 'CS 545', 'SSW 567', 'SSW 687'}, {'SSW 555', 'SSW 540'}, None],
                    ['10172', 'Forbes, I', 'SFEN', {'SSW 555', 'SSW 567'}, {'SSW 564', 'SSW 540'}, {'CS 501', 'CS 513', 'CS 545'}],
                    ['10175', 'Erickson, D', 'SFEN', {'SSW 564', 'SSW 567', 'SSW 687'}, {'SSW 555', 'SSW 540'}, {'CS 501', 'CS 513', 'CS 545'}],
                    ['10183', 'Chapman, O', 'SFEN', {'SSW 689'}, {'SSW 564', 'SSW 555', 'SSW 540', 'SSW 567'}, {'CS 501', 'CS 513', 'CS 545'}],
                    ['11399', 'Cordova, I', 'SYEN', {'SSW 540'}, {'SYS 612', 'SYS 671', 'SYS 800'}, None],
                    ['11461', 'Wright, U', 'SYEN', {'SYS 750', 'SYS 800', 'SYS 611'}, {'SYS 612', 'SYS 671'}, {'SSW 565', 'SSW 540', 'SSW 810'}],
                    ['11658', 'Kelly, P', 'SYEN', set(), {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 540', 'SSW 810'}],
                    ['11714', 'Morton, A', 'SYEN', {'SYS 645', 'SYS 611'}, {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 540', 'SSW 810'}],
                    ['11788', 'Fuller, E', 'SYEN', {'SSW 540'}, {'SYS 612', 'SYS 671', 'SYS 800'}, None]]

        reality = [s.student_summary() for s in self.rep._students.values()]

        self.assertEqual(expected, reality)

    def test_instructor_data(self):
        """ testing data in instructor pretty table """

        test_path = "/Users/jigar/Documents/SSW 810/Project/PHW10"
        self.rep = Repository(test_path, False)

        expected = {('98765', 'Einstein, A', 'SFEN', 'SSW 576', 4),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}

        reality = [row for instructor in self.rep._instructors.values() for row in instructor.instructor_summary()]

        self.assertEqual(expected, reality)

    def test_majors_data(self):
        """ test data in majors pretty table """

        test_path = "/Users/jigar/Documents/SSW 810/Project/PHW10"
        self.rep = Repository(test_path, False)

        expected = [["SFEN", {'SSW 555', 'SSW 540', 'SSW 564', 'SSW 567'}, {'CS 501', 'CS 545', 'CS 513'}],
                    ["SYEN", {'SYS 612', 'SYS 671', 'SYS 800'}, {'SSW 565', 'SSW 540', 'SSW 810'}]]

        reality = [m.major_summary() for m in self.rep._majors.values()]

        self.assertEqual(expected, reality)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)

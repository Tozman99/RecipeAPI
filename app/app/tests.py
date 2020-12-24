from django.test import TestCase
from .calc import add_num


class TestCalc(TestCase):

    def add_num_test(self):

        self.assertEqual(add_num(2, 3), 5)


from django.test import TestCase
from .classes import Generator
from test.classes import AbstractTest

class GeneratorTest(AbstractTest):
    def setUp(self):
        pass

    def test_proper_init(self):
        gen = Generator(100, 1500, 50, 23, 10000)
        gen.update_prize_pool()
        gen.print_each_position()


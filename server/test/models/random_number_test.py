from django.test import TestCase
from server.models import *

class RandomNumberDrawTestCase(TestCase):
    def setUp(self):
        pass

    def build_random_number_test(self):
        """RandomNumberDraw: Basic construction"""
        RandomNumberDraw()

    def default_constructor_test(self):
        """RandomNumberDraw: Default constructor"""
        tested_item = RandomNumberDraw()
        self.assertEqual(tested_item.range_min,0)
        self.assertEqual(tested_item.range_max,None)
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,False)

    def parametrized_constructor_test(self):
        """RandomNumberDraw: Full parametrized constructor"""
        tested_item = RandomNumberDraw(range_min=2,range_max = 5,allow_repeat=True, number_of_results = 1)
        self.assertEqual(tested_item.range_min,2)
        self.assertEqual(tested_item.range_max,5)
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,True)

    def is_feasible_default_test(self):
        """RandomNumberDraw: Default constructor is not feasible"""
        self.assertFalse(RandomNumberDraw().is_feasible())

    def is_feasible_simple_test(self):
        """RandomNumberDraw: Simple parametrized constructor is feasible"""
        tested_item = RandomNumberDraw(range_max=5)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_and_results_ok_test(self):
        """RandomNumberDraw: Acceptable range and number of results is feasible"""
        tested_item = RandomNumberDraw(range_min=2,range_max=5,number_of_results=3,allow_repeat=False)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_ko_test(self):
        """RandomNumberDraw: Range requested is not feasible"""
        tested_item = RandomNumberDraw(range_max=2,range_min=4)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_too_many_results_ko_test(self):
        """RandomNumberDraw: Too many results requested is not feasible"""
        tested_item = RandomNumberDraw(range_min=2,range_max=5,number_of_results=4,allow_repeat=False)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_many_results_with_repeat_ok_test(self):
        """RandomNumberDraw: Many results requested with repeat is feasible"""
        tested_item = RandomNumberDraw(range_max=5,range_min=2,number_of_results=4,allow_repeat=True)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_with_repeat_ko_test(self):
        """RandomNumberDraw: Invalid range requested with repeat is not feasible"""
        tested_item = RandomNumberDraw(range_max=2,range_min=4, allow_repeat=True)
        self.assertFalse(tested_item.is_feasible())

    '''def draw_poll_relationship_after_save_test(self):
        """Validates the relation ship from draw to poll"""
        t_poll = RandomNumberPoll(range_max=10)
        t_poll.save()
        t_draw1 = RandomNumberDraw(value=10)
        t_draw2 = RandomNumberDraw(value=10)
        self.assertEqual(0, t_poll.draws.count())
        t_draw1.poll = t_poll
        self.assertEqual(0, t_poll.draws.count())
        t_draw1.save()
        self.assertEqual(1, t_poll.draws.count())
        t_draw2.poll = t_poll
        t_draw2.save()
        self.assertEqual(2, t_poll.draws.count())'''

from django.test import TestCase
from server.models import *
import django


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

    def draw_rasult_relationship_after_save_test(self):
        """RandomNumberDraw: Validates the relationship Draw-Result"""
        django.setup() # to access to t_draw.draw_results
        t_draw = RandomNumberDraw(range_max=10)
        t_draw.save()
        t_result1 = RandomNumberResult()
        t_result2 = RandomNumberResult()
        self.assertEqual(0, t_draw.draw_results.count())
        t_result1.draw = t_draw
        self.assertEqual(0, t_draw.draw_results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.draw_results.count())
        t_result2.draw = t_draw
        t_result2.save()
        self.assertEqual(2, t_draw.draw_results.count())


    def result_number_relationship_after_save_test(self):
        """RandomNumberDraw: Validates the relationship Result-Number"""
        #django.setup() # to access to t_draw.draw_results
        t_number1 = RandomNumberResultNumber(value=2)
        t_number2 = RandomNumberResultNumber(value=5)
        t_draw = RandomNumberDraw(range_max=10)
        t_draw.save()
        t_result = RandomNumberResult()
        t_result.draw = t_draw
        t_result.save()
        self.assertEqual(0, t_result.result_numbers.count())
        t_number1.result = t_result
        t_number2.result = t_result
        self.assertEqual(0, t_result.result_numbers.count())
        t_number1.save()
        self.assertEqual(1, t_result.result_numbers.count())
        t_number2.save()
        self.assertEqual(2, t_result.result_numbers.count())


    def toss_several_results_test(self):
        """RandomNumberDraw: Several tosses store several results"""
        t_draw = RandomNumberDraw(range_max=10)
        t_draw.save()
        self.assertEqual(0,t_draw.draw_results.count())
        t_draw.toss()
        self.assertEqual(1,t_draw.draw_results.count())
        t_draw.toss()
        self.assertEqual(2,t_draw.draw_results.count())


    def toss_multiple_numbers_test(self):
        """RandomNumberDraw: a toss generates a result with several numbers"""
        t_draw1 = RandomNumberDraw(range_max=10,number_of_results=2)
        t_draw1.save()
        t_draw1.toss()
        result = t_draw1.draw_results.order_by("-id")[0]
        self.assertEqual(2,result.result_numbers.count())
        t_draw1.toss()

        t_draw2 = RandomNumberDraw(range_max=10,number_of_results=7)
        t_draw2.save()
        t_draw2.toss()
        result2 = t_draw2.draw_results.order_by("-id")[0]
        self.assertEqual(7,result2.result_numbers.count())
        t_draw2.toss()


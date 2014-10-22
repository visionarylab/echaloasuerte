from django.db import models
from django.utils.translation import ugettext_lazy as _

class RandonNumberDraw(models.Model):
    pass


class RandomNumberPoll(models.Model):
    """
    Class that represents a poll with the details to produce random numbers.
    """

    range_min = models.BigIntegerField(_("Range start"), blank=False, null=False, default=0)
    """"Minimun value to be generated. Inclusive."""

    range_max = models.BigIntegerField(_("Range End"), blank=False, null=False)
    """"Maximun value to be generated. Exclusive."""

    number_of_results = models.PositiveIntegerField(_("Number of results"), blank=False, null=False, default=1)
    """Number of Random numbers to generate"""

    allow_repeat = models.BooleanField(_("Allow Repetitions"), blank=False, null=False, default=False)
    """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""

    def is_feasible(self):
        if self.range_max is None:
            return False
        if self.allow_repeat == True:
            return  self.range_min < self.range_max
        else:
            return self.range_max - self.range_min >= self.number_of_results


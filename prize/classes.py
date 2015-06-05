import math
from .exceptions import PrizeGenerationException
from collections import OrderedDict

class Generator(object):
    """
    Generate a prize structure, given some basic information about its size and prizepool, etc...
    """
    def __init__(self, buyin, first_place, round_payouts, payout_spots, prize_pool):
        self.buyin                  = buyin
        self.first_place            = first_place
        self.round_payouts          = round_payouts
        self.payout_spots           = payout_spots
        self.prize_pool             = prize_pool
        self.modified_prize_pool    = prize_pool
        self.multiplier             = 0
        self.final_x                = 0.0
        self.update_prize_pool()

        self.prize_list = None
        self.range_list = None
        self.__build_prize_list()         # so every time we get it we dont have to build it

        self.print_each_position()

    def update_prize_pool(self):
        best_x          = None
        best_multiplier = None
        best_prize_pool = None
        top_range = 100
        for x in range(1, top_range):
            x = x/top_range
            temp_prize_pool = self.get_sum_equation(x)
            if temp_prize_pool > self.prize_pool:
                remainder = temp_prize_pool - self.prize_pool
                if remainder == 0:
                    best_x          = x
                    best_multiplier = 0
                    best_prize_pool = self.prize_pool
                    break
                if (remainder % self.buyin) == 0 :
                    m = remainder / self.buyin
                    if(best_x == None or best_multiplier > m):
                        best_x          = x
                        best_multiplier = m
                        best_prize_pool = self.prize_pool + (self.buyin * best_multiplier)


        if(best_x == None):
            raise PrizeGenerationException()

        self.final_x = best_x
        self.multiplier = best_multiplier
        self.modified_prize_pool = best_prize_pool

    def __build_prize_list(self):
        """
        Internal list to hold all the prize information so we dont have to regenerate it.
        :return:
        """
        self.prize_list = []
        for i in range(1, self.payout_spots+1):
            self.prize_list.append( (i, self.equation(i, self.final_x) ) )

        data = {}
        for prize in self.prize_list:
            try:
                data[ prize[1] ].append( prize[0] )
            except KeyError:
                data[ prize[1] ] = [ prize[0] ]
        ordered_data = OrderedDict( sorted(data.items(), key=lambda t: t[1]) )
        self.range_list = list( ordered_data.items() )

    def get_prize_list(self):
        """
        The list of tuples, where each tuple represents a rank and payout.
        For example: [ (1, 100), (2, 50) ]   # represents a prize
        structure in which there are two payouts, 1st -> $100, 2nd -> $50

        :return:
        """
        return self.prize_list

    def get_range_list(self):
        return self.range_list

    def get_sum_equation(self, x):
        sum = 0
        for i in range(1, self.payout_spots+1):
            sum += self.equation(i, x)
        print("x:"+str(x)+"  sum:"+str(sum))

        return sum

    def equation(self, i , x):
        return self.roundup((self.first_place * (math.pow(i, -x))))

    def roundup(self,x):
        return int(math.ceil(x / self.round_payouts)) * self.round_payouts

    def print_each_position(self):

        for i in range(1, self.payout_spots+1):
            print(str(i)+":"+str(self.equation(i, self.final_x)))

        print("new prize pool            :"+str(self.modified_prize_pool))
        print("additional buyins required:"+str(self.multiplier))



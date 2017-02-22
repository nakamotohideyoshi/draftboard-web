import math
from collections import OrderedDict

from django.db.transaction import atomic

from cash.models import CashAmount
from mysite.exceptions import InvalidArgumentException
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException
from prize.models import PrizeStructure, Rank, GeneratorSettings
from ticket.models import TicketAmount
from transaction.models import AbstractAmount
from .exceptions import (
    PrizeGenerationException,
    InvalidBuyinAndPrizePoolException,
    RakeIsNot10PercentException,
    NoMatchingTicketException,
    NumberPrizesNotDivisibleBy9Exception,
    BuyinNotLessThanEachTicketException,
)


class Generator(object):
    """
    Generate a prize structure, given some basic information about its size and prizepool, etc...

    """

    def __init__(self, buyin, first_place, round_payouts, payout_spots, prize_pool, exact=True,
                 verbose=False):
        self.buyin = buyin
        self.first_place = first_place
        if prize_pool % self.buyin != 0:
            raise InvalidBuyinAndPrizePoolException()
        if round_payouts < self.buyin or round_payouts % buyin != 0:
            raise InvalidArgumentException(type(self).__name__,
                                           'round_payouts must be greater than or equal to, and a also a multiple of the buyin')
        self.round_payouts = round_payouts
        self.payout_spots = payout_spots
        self.prize_pool = prize_pool
        self.modified_prize_pool = prize_pool

        self.exact = exact

        self.multiplier = 0
        self.final_x = 0.0
        self.update_prize_pool()

        self.prize_list = None
        self.range_list = None
        self.__build_prize_list()  # so every time we get it we dont have to build it

        if verbose:
            self.print_each_position()

    def update_prize_pool(self):
        best_x = None
        best_multiplier = None
        best_prize_pool = None
        top_range = 100
        for x in range(1, top_range):
            x = x / top_range
            temp_prize_pool = self.get_sum_equation(x)
            if temp_prize_pool > self.prize_pool:
                remainder = temp_prize_pool - self.prize_pool
                if remainder == 0:
                    best_x = x
                    best_multiplier = 0
                    best_prize_pool = self.prize_pool
                    break
                if (remainder % self.buyin) == 0:
                    m = remainder / self.buyin
                    if (best_x == None or best_multiplier > m):
                        best_x = x
                        best_multiplier = m
                        best_prize_pool = self.prize_pool + (self.buyin * best_multiplier)

        if (best_x == None):
            raise PrizeGenerationException()

        self.final_x = best_x
        self.multiplier = best_multiplier
        self.modified_prize_pool = best_prize_pool

    def __build_prize_list(self):
        """
        Internal list to hold all the prize information so we dont have to regenerate it.
        :return:
        """

        # print('__build_prize_list')
        self.prize_list = []
        for i in range(1, self.payout_spots + 1):
            self.prize_list.append((i, self.equation(i, self.final_x)))

        if self.exact:
            # print('exact')
            # take buyins off the end until we have the original
            # prize pool specified (no added buyins from alogrithm)
            prize_list_with_extra_buyins = list(self.prize_list)
            # print('prize_list_with_extra_buyins', prize_list_with_extra_buyins)
            self.prize_list = []
            original_prize_pool_remaining = self.prize_pool
            # print('original_prize_pool_remaining', original_prize_pool_remaining)
            for rank, value in prize_list_with_extra_buyins:
                if original_prize_pool_remaining <= 0:
                    break
                elif original_prize_pool_remaining >= value:
                    original_prize_pool_remaining -= value
                    new_prize = value
                else:
                    new_prize = original_prize_pool_remaining  # the difference
                    original_prize_pool_remaining -= value

                self.prize_list.append((rank, new_prize))
        else:
            print('not exact - prizes modified potentially')
            pass

        data = {}
        # total = 0
        for prize in self.prize_list:
            # total += prize[1]
            try:
                data[prize[1]].append(prize[0])
            except KeyError:
                data[prize[1]] = [prize[0]]

        # print('total:', total)
        ordered_data = OrderedDict(sorted(data.items(), key=lambda t: t[1]))
        self.range_list = list(ordered_data.items())

    def get_buyin(self):
        """ return the 'buyin' seed value  """
        return self.buyin

    def get_first_place(self):
        """ return the 'first_place' seed value  """
        return self.first_place

    def get_round_payouts(self):
        """ return the 'round_payouts' seed value  """
        return self.round_payouts

    def get_payout_spots(self):
        """ return the 'payout_spots' seed value  """
        return self.payout_spots

    def get_prize_pool(self):
        """ return the 'prize_pool' seed value  """
        return self.prize_pool

    def get_max_entries(self):
        return self.prize_pool / self.buyin

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
        for i in range(1, self.payout_spots + 1):
            sum += self.equation(i, x)
        # print("x:"+str(x)+"  sum:"+str(sum))

        return sum

    def equation(self, i, x):
        return self.roundup((self.first_place * (math.pow(i, -x))))

    def roundup(self, x):
        return int(math.ceil(x / self.round_payouts)) * self.round_payouts

    def print_each_position(self):

        # for i in range(1, self.payout_spots+1):
        #     print(str(i)+":"+str(self.equation(i, self.final_x)))


        total = 0
        for rank, value in self.get_prize_list():
            total += value
            print(str(rank) + ':' + str(value))
        print('original prize pool       :' + str(self.prize_pool))
        print("modified prize pool       :" + str(self.modified_prize_pool))
        print("additional buyins required:" + str(self.multiplier))
        print('total after exact fix     :', total)

    def get_generator_settings_instance(self):
        """
        Return a newly save()'ed GeneratorSettings model based on this Generator's settings
        """
        gs = GeneratorSettings()
        gs.buyin = self.get_buyin()
        gs.first_place = self.get_first_place()
        gs.round_payouts = self.get_round_payouts()
        gs.payout_spots = self.get_payout_spots()
        gs.prize_pool = self.get_prize_pool()
        gs.save()
        return gs


class AbstractPrizeStructureCreator(object):
    """
    A "prize structure", in general, is a list of (rank, value) pairs where
    the rank is 1st, 2nd, 3rd place, etc... and the value is a cash($), or Ticket amount.

    AbstractPrizeManager contains functionality common to all prize structures, but
    the programmer should use CashPrizeStructure or TicketPrizeStructure, etc...

    """

    class InvalidSettingsException(Exception):
        pass

    DEFAULT_NAME = 'new prize structure'

    def __init__(self, amount_model, name='default'):
        self.prize_structure = None
        self.buyin = None
        self.prize_structure_model = PrizeStructure
        self.rank_model = Rank
        self.ranks = None  # list of the rank instances once generated
        self.added_ranks = []  # if ranks are added to this class, add them as (rank, value) tuples here

        if not amount_model:
            raise VariableNotSetException(type(self).__name__, 'amount_model')
        if not issubclass(amount_model, AbstractAmount):
            raise IncorrectVariableTypeException(type(self).__name__, 'amount_model')
        self.amount_model = amount_model

        self.name = self.get_unique_name(
            name)  # return a name based on the one specified that is unique

    def get_unique_name(self, name):
        """
        If name is non-empty string, try to use it -- just add a number on it if it exists.
        """
        if name:
            n_similar_names = len(self.prize_structure_model.objects.filter(name__istartswith=name))
            if n_similar_names > 0:
                return name + str(n_similar_names)
            return name

        else:
            # generate a random name
            n_similar_names = len(
                self.prize_structure_model.objects.filter(name__istartswith=self.DEFAULT_NAME))
            if n_similar_names:
                return '%s %s' % (self.DEFAULT_NAME, str(n_similar_names))
            return self.DEFAULT_NAME

    def set_buyin(self, value):
        """
        associate a buyin value which will be set to the prize_structure
        when save() is called.

        :param value:
        :return:
        """
        self.buyin = value

    def add(self, rank, value):
        """
        Add a rank, value pair to this object. if this object has not yet been saved,
        this action will succeed as many times as you want until you call save() to create
        the whole prize structure.
        """
        if self.ranks:
            raise Exception(
                'You can not add rank/values to this object, because it has already been created.')
        self.added_ranks.append((rank, value))

    def __str__(self):
        """
        returns a readable string version of this object
        """
        s = '%s\n' % self.prize_structure
        # if self.prize_structure.generator_settings:
        #     s += '    %s\n' % str(self.prize_structure.generator_settings)
        for r in self.ranks:
            s += '    %s\n' % str(r)
        return s.strip()  # strip off leading & trailing whitespace/newlines

    @atomic
    def save(self):
        """
        Commit this prize structure and associated ranks to the database.

        The @atomic decorator ensures a bulk save behaviour which can be quite
        useful for speed and also if there are any problems
        we wont get partial saves...

        Returns the newly created PrizeStructure model
        """

        # create the PrizeStructure
        self.prize_structure = self.prize_structure_model()
        self.prize_structure.name = self.name
        self.prize_structure.save()

        # create the ranks
        total_prize_value = 0
        if self.ranks is None:
            self.ranks = []
        for rank_number, prize_value in self.added_ranks:
            # use the internal amount_model to get the right type of amount
            r = self.rank_model()
            r.prize_structure = self.prize_structure
            r.rank = rank_number
            r.amount = self.get_amount_instance(prize_value)
            r.save()

            # sum all the values
            total_prize_value += float(r.value)

            # if that worked, add it to the list of rank instances
            self.ranks.append(r)

            # try:
            settings = GeneratorSettings()
            settings.buyin = self.buyin
            settings.first_place = self.ranks[0].value
            settings.round_payouts = 0
            settings.payout_spots = len(self.ranks)
            settings.prize_pool = total_prize_value
            settings.save()
        # except:
        #     raise self.InvalidSettingsException('buy, first_place, payout_spots, or prize_pool not set, or calculated improperly')

        self.prize_structure.generator = settings
        self.prize_structure.save()

        return self.prize_structure

    def get_amount_instance(self, amount):
        """
        Get a NEW instance of the type of AbstractAmount.

        NOTE: for Ticket related Amounts - you should get an existing and never create,
                (so the TicketPrizeStructureCreator should override this method.)
        """
        # print(self.amount_model)
        amount_instance, created = self.amount_model.objects.get_or_create(amount=amount)
        # 'created' is a boolean which indicates if the object was created, or simply retrieved
        return amount_instance


class CashPrizeStructureCreator(AbstractPrizeStructureCreator):
    """
    Used to create a prize structure (with a prize.classes.Generator) for cash.
    """

    def __init__(self, generator=None, name=''):
        """
        Create a cash PrizeStructure given a prize.classes.Generator instance
        which contains the list of payouts and some seed values from which
        the list of prizes was created.

        :param generator:
        :param name:
        :return:
        """
        super().__init__(CashAmount, name)

        self.generator = generator  # an instance of the class
        if self.generator:
            self.buyin = generator.buyin
            for rank, value in self.generator.get_prize_list():
                self.add(rank, value)

    def get_generator_settings(self):
        """
        If a generator exists, save return an instance of
        its seed values as a GeneratorSettings model.
        """

        if not self.generator:
            return None
        else:
            # create an instance of the GeneratorSettings model using the Generator passed in.
            return self.generator.get_generator_settings_instance()

    def add(self, rank, value):
        """
        Overrides AbstractPrizeStructureCreator.add() to prevent the programmer
        from calling add() if the cash structure was created with a Generator
        """
        if self.generator and len(self.added_ranks) >= len(self.generator.get_prize_list()):
            raise Exception(
                'You may not call add(rank,value) if the prize structure was created with a generator')

        super().add(rank, value)

    @atomic
    def save(self):
        """
        Overrirdes parent save() to be able to set the generator settings
        """

        # MUST call super to save the main stuff
        super().save()

        # set the generator settings and save it again.
        self.prize_structure.generator_settings = self.get_generator_settings()
        self.prize_structure.save()

    def __str__(self):
        """
        returns a readable string version of this object
        """

        s = super().__str__()
        if self.prize_structure.generator_settings:
            s += '\n    %s' % str(self.prize_structure.generator_settings)
        return s  # strip off leading & trailing whitespace/newlines


class AbstractFlatPrizeStructureCreator(AbstractPrizeStructureCreator):
    """
    Create a prize structure whos payouts are of the type 'amount_model_class'
    which would be like a CashAmount, or a TicketAmount.

    The prize pool created will be for any prize structure where all payout
    spots receive the same payout value (ie: 50/50, Triple-Up, 4x, etc...

    after successfully creating an instance of this class (in an inheriting child class),
    you must call save() to actually create the prize structure in the database!

    """

    # class InvalidFlatPrizeStructureException(Exception): pass

    def __init__(self, buyin, amount_model_class, payout_value, number_of_prizes, name=''):
        super().__init__(amount_model_class, name=name)

        # set values
        self.set_buyin(buyin)
        self.number_of_prizes = number_of_prizes
        self.payout_value = payout_value  # the value of each payout spot
        self.prize_pool = number_of_prizes * payout_value

        # validate these settings will work
        self.validate_params()

    def validate_params(self):
        """
        inheriting classes should override this method to provide specific validation.

        ideally want to do exactly 10% rake, whch may be tricky for small TicketAmount structures

        :param buyin:
        :param payout_value:
        :param number_of_prizes:
        :return:
        """
        pass

    @atomic
    def save(self):
        """
        override parent save()

        :return:
        """

        # since it a flat structure, just add all the ranks
        for i in range(self.number_of_prizes):
            self.add(i + 1, self.payout_value)

        # create the PrizeStructure
        self.prize_structure = self.prize_structure_model()
        self.prize_structure.name = self.name
        self.prize_structure.generator = self.create_flat_structure_generator_settings()
        self.prize_structure.save()

        # create the ranks
        if self.ranks is None:
            self.ranks = []
        for rank_number, prize_value in self.added_ranks:
            # use the internal amount_model to get the right type of amount
            r = self.rank_model()
            r.prize_structure = self.prize_structure
            r.rank = rank_number
            r.amount = self.get_amount_instance(prize_value)
            r.save()
            # if that worked, add it to the list of rank instances
            self.ranks.append(r)

        return self.prize_structure

    def create_flat_structure_generator_settings(self):
        """
        return a new instance of GeneratorSettings, created
        with flat payout structure in mind.

        the generator class itself isnt actually used for the algorithm
        which creates a curved prize structure!

        however, we still need the GeneratorSettings to hold
        some of the values for this Flat prize structure
        """
        gs = GeneratorSettings()
        gs.buyin = self.buyin
        gs.first_place = self.payout_value
        gs.round_payouts = self.buyin  # just use the buyin
        gs.payout_spots = self.number_of_prizes
        gs.prize_pool = self.payout_value * self.number_of_prizes
        gs.save()
        return gs


class TicketPrizeStructureCreator(AbstractFlatPrizeStructureCreator):
    """
    Used to create a prize structure based on TicketAmount's
    where all payout spots receive the same payout value!
    """

    def __init__(self, buyin, ticket_value, number_of_prizes, name=''):
        super().__init__(buyin, TicketAmount, ticket_value, number_of_prizes, name=name)


class FlatCashPrizeStructureCreator(AbstractFlatPrizeStructureCreator):
    """
    Used to create a prize structure based on CashAmount's where
    all paid spots receive the same payout value!
    """

    def __init__(self, buyin, ticket_value, number_of_prizes, name=''):
        super().__init__(buyin, CashAmount, ticket_value, number_of_prizes, name=name)


class FlatTicketPrizeStructureCreator(AbstractFlatPrizeStructureCreator):
    """
    Used to create a prize structure based on TicketAmount's
    where all payout spots receive the same payout value!
    """

    def __init__(self, buyin, ticket_value, number_of_prizes, entries=None, name=''):
        super().__init__(buyin, TicketAmount, ticket_value, number_of_prizes, name=name)

        # we can infer the # of entries for FLAT ticket structures!
        self.entries = (self.payout_value * number_of_prizes) / 0.9
        if entries is not None:
            self.entries = entries  # not positive why we would want to force it

        # given a flat 10% rake across the board,
        # the number of prizes actually MUST be
        # a multiple of 9 !
        self.validate_number_prizes()

        # ensure the payout ticket value is valid
        self.validate_payout_ticket_amount()

        # raise an exception if the total rake for this prize structure is not 10 percent
        self.validate_rake_amount()

    def validate_number_prizes(self):
        """
        :raises NumberPrizesNotDivisibleBy9Exception:
        """
        if self.number_of_prizes % 9 != 0:
            raise NumberPrizesNotDivisibleBy9Exception(str(self.number_of_prizes))

    def validate_payout_ticket_amount(self):
        """
        :raises BuyinNotLessThanEachTicketException:
        :raises NoMatchingTicketException:
        """
        if self.buyin >= self.payout_value:
            err_msg = '%s buyin, %s each prize' % (str(self.buyin), str(self.payout_value))
            raise BuyinNotLessThanEachTicketException(err_msg)

        try:
            ta = TicketAmount.objects.get(amount=self.payout_value)
        except TicketAmount.DoesNotExist:
            raise NoMatchingTicketException(str(self.payout_value))

    def validate_rake_amount(self):
        """
        :raises RakeIsNot10PercentException: if the total rake is not an even 10 percent.
        """

        # prizepool is # entries * buyin * (1.0 - rake)
        prize_pool = float(self.entries) * float(self.buyin) * 0.9
        # tickets may have a remainder, but it is the number
        # of tickets we can pay out for the given number of entries and the buyin
        tickets = float(prize_pool) / float(self.payout_value)
        # get the decimal remainder of 'tickets'
        fraction = tickets % 1
        if fraction >= 0.0001:
            # a significant decimal remainder means we dont
            # have settings that result in 10% rake overall
            err_msg = 'invalid settings: $%s buyin, $%s tickets, %s prizes, %s entries' % \
                      (self.buyin, self.payout_value, self.number_of_prizes, self.entries)
            raise RakeIsNot10PercentException(err_msg)

    @staticmethod
    def print_all(max_entries):
        """
        print all possible FlatTicketPrizeStructures where the
        total number of entries in each structure is <= 'max_entries'
        """
        ticket_amounts = [float(ta.amount) for ta in TicketAmount.objects.all()]
        buyin_amounts = list(ticket_amounts)
        print('ticket_amounts %s' % str(ticket_amounts))

        for buyin in buyin_amounts:
            print('$%s buyin' % str(buyin))
            for ticket in ticket_amounts:
                if ticket <= buyin:
                    continue
                print('    $%s ticket' % str(ticket))
                entries = 5
                while entries <= max_entries:
                    prize_pool = entries * buyin * 0.9  # prizepool is # entries * buyin * (1.0 - rake)
                    tickets = float(prize_pool) / float(ticket)
                    fraction = tickets % 1
                    if fraction < 0.0001:
                        # this could be a good structure! print the values
                        print('        %s payouts, %s entries' % (
                        str(int(tickets)), str(int(entries))))
                    entries += 1
        print('... showing all the possible FlatTicketPrizeStructures (entries <= %s)' % str(
            max_entries))

import math
from .exceptions import PrizeGenerationException
from collections import OrderedDict
from mysite.exceptions import VariableNotSetException, IncorrectVariableTypeException
from ticket.exceptions import InvalidTicketAmountException
from mysite.exceptions import InvalidArgumentException
from prize.models import PrizeStructure, Rank, GeneratorSettings
from transaction.models import AbstractAmount
from cash.models import CashAmount
from ticket.models import TicketAmount
from django.db.transaction import atomic

class Generator(object):
    """
    Generate a prize structure, given some basic information about its size and prizepool, etc...

    # TODO - Generator only works for integers
    """
    def __init__(self, buyin, first_place, round_payouts, payout_spots, prize_pool, exact=True):
        self.buyin                  = buyin
        self.first_place            = first_place

        if round_payouts < self.buyin or round_payouts % buyin != 0:
            raise InvalidArgumentException(type(self).__name__,
                    'round_payouts must be greater than or equal to, and a also a multiple of the buyin')
        self.round_payouts          = round_payouts
        self.payout_spots           = payout_spots
        self.prize_pool             = prize_pool
        self.modified_prize_pool    = prize_pool

        self.exact                  = exact

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

        print('__build_prize_list')
        self.prize_list = []
        for i in range(1, self.payout_spots+1):
            self.prize_list.append( (i, self.equation(i, self.final_x) ) )

        if self.exact:
            print('exact')
            # take buyins off the end until we have the original
            # prize pool specified (no added buyins from alogrithm)
            prize_list_with_extra_buyins = list(self.prize_list)
            print('prize_list_with_extra_buyins', prize_list_with_extra_buyins)
            self.prize_list = []
            original_prize_pool_remaining = self.prize_pool
            print('original_prize_pool_remaining', original_prize_pool_remaining)
            for rank, value in prize_list_with_extra_buyins:
                if original_prize_pool_remaining <= 0:
                    break
                elif original_prize_pool_remaining >= value:
                    original_prize_pool_remaining -= value
                    new_prize = value
                else:
                    new_prize = original_prize_pool_remaining # the difference
                    original_prize_pool_remaining -= value

                self.prize_list.append( (rank, new_prize) )
        else:
            print('not exact - modified potentially')

        data = {}
        #total = 0
        for prize in self.prize_list:
            #total += prize[1]
            try:
                data[ prize[1] ].append( prize[0] )
            except KeyError:
                data[ prize[1] ] = [ prize[0] ]

        # print('total:', total)
        ordered_data = OrderedDict( sorted(data.items(), key=lambda t: t[1]) )
        self.range_list = list( ordered_data.items() )

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
        for i in range(1, self.payout_spots+1):
            sum += self.equation(i, x)
        print("x:"+str(x)+"  sum:"+str(sum))

        return sum

    def equation(self, i , x):
        return self.roundup((self.first_place * (math.pow(i, -x))))

    def roundup(self,x):
        return int(math.ceil(x / self.round_payouts)) * self.round_payouts

    def print_each_position(self):

        # for i in range(1, self.payout_spots+1):
        #     print(str(i)+":"+str(self.equation(i, self.final_x)))


        total = 0
        for rank,value in self.get_prize_list():
            total += value
            print( str(rank) + ':' + str(value) )
        print('original prize pool       :'+str(self.prize_pool))
        print("modified prize pool       :"+str(self.modified_prize_pool))
        print("additional buyins required:"+str(self.multiplier))
        print('total after exact fix     :', total)

    def get_generator_settings_instance(self):
        """
        Return a newly save()'ed GeneratorSettings model based on this Generator's settings
        """
        gs = GeneratorSettings()
        gs.buyin            = self.get_buyin()
        gs.first_place      = self.get_first_place()
        gs.round_payouts    = self.get_round_payouts()
        gs.payout_spots     = self.get_payout_spots()
        gs.prize_pool       = self.get_prize_pool()
        gs.save()
        return gs

class AbstractPrizeStructureCreator(object):
    """
    A "prize structure", in general, is a list of (rank, value) pairs where
    the rank is 1st, 2nd, 3rd place, etc... and the value is a cash($), or Ticket amount.

    AbstractPrizeManager contains functionality common to all prize structures, but
    the programmer should use CashPrizeStructure or TicketPrizeStructure, etc...
    """

    DEFAULT_NAME = 'new prize structure'

    def __init__(self, amount_model, name='default'):
        self.prize_structure = None
        self.prize_structure_model  = PrizeStructure
        self.rank_model             = Rank
        self.ranks                  = None  # list of the rank instances once generated
        self.added_ranks            = []    # if ranks are added to this class, add them as (rank, value) tuples here

        if not amount_model:
            raise VariableNotSetException(type(self).__name__, 'amount_model')
        if not issubclass(amount_model, AbstractAmount):
            raise IncorrectVariableTypeException(type(self).__name__, 'amount_model')
        self.amount_model = amount_model

        self.name = self.get_unique_name( name ) # return a name based on the one specified that is unique

    def get_unique_name(self, name):
        """
        If name is non-empty string, try to use it -- just add a number on it if it exists.
        """
        if name:
            n_similar_names = len( self.prize_structure_model.objects.filter( name__istartswith=name ) )
            if n_similar_names > 0:
                return name + str(n_similar_names)
            return name

        else:
            # generate a random name
            n_similar_names = len( self.prize_structure_model.objects.filter( name__istartswith=self.DEFAULT_NAME ) )
            if n_similar_names:
                return '%s %s' % ( self.DEFAULT_NAME, str(n_similar_names) )
            return self.DEFAULT_NAME

    def add(self, rank, value):
        """
        Add a rank, value pair to this object. if this object has not yet been saved,
        this action will succeed as many times as you want until you call save() to create
        the whole prize structure.
        """
        if self.ranks:
            raise Exception('You can not add rank/values to this object, because it has already been created.')
        self.added_ranks.append( (rank, value) )

    def __str__(self):
        """
        returns a readable string version of this object
        """
        s = '%s\n' % self.prize_structure
        # if self.prize_structure.generator_settings:
        #     s += '    %s\n' % str(self.prize_structure.generator_settings)
        for r in self.ranks:
            s += '    %s\n' % str(r)
        return s.strip() # strip off leading & trailing whitespace/newlines

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
        self.prize_structure        = self.prize_structure_model()
        self.prize_structure.name   = self.name
        self.prize_structure.save()

        # create the ranks
        if self.ranks is None:
            self.ranks = []
        for rank_number, prize_value in self.added_ranks:
            # use the internal amount_model to get the right type of amount
            r                   = self.rank_model()
            r.prize_structure   = self.prize_structure
            r.rank              = rank_number
            r.amount            = self.get_amount_instance( prize_value )
            r.save()

            # if that worked, add it to the list of rank instances
            self.ranks.append( r )
        return self.prize_structure

    def get_amount_instance(self, amount):
        """
        Get a NEW instance of the type of AbstractAmount.

        NOTE: for Ticket related Amounts - you should get an existing and never create,
                (so the TicketPrizeStructureCreator should override this method.)
        """
        print( self.amount_model )
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
        super().__init__( CashAmount, name )

        self.generator          = generator     # an instance of the class
        if self.generator:
            for rank, value in self.generator.get_prize_list():
                self.add( rank, value )

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
            raise Exception('You may not call add(rank,value) if the prize structure was created with a generator')

        super().add( rank, value )

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
        return s # strip off leading & trailing whitespace/newlines

class TicketPrizeStructureCreator(AbstractPrizeStructureCreator):
    # TODO should set the buyin
    """
    Used to create a prize structure based on tickets
    """

    def __init__(self, ticket_value, number_of_prizes, name=''):
        """
        Create a ticketed PrizeStructure given a ticket_value and the
        number of prizes to be paid.

        :param ticket_value:
        :param name:
        :return:
        """
        super().__init__( TicketAmount, name )
        self.ticket_amount = self.get_ticket_amount( ticket_value )

        if number_of_prizes <= 0:
            raise VariableNotSetException(type(self).__name__, 'number_of_prizes')
        self.number_of_prizes = number_of_prizes

        # since we know the ticket value and the number of prizes,
        # we can add all the ranks right here. Dont forget to call save() though.
        for rnk in range(1, self.number_of_prizes + 1 ):
            self.add( rnk, ticket_value )

    def get_ticket_amount(self, ticket_value):
        try:
            return TicketAmount.objects.get( amount=ticket_value )
        except TicketAmount.DoesNotExist:
            raise InvalidTicketAmountException(
                type(self).__name__,
                ticket_value
            )

    def get_amount_instance(self, amount):
        """
        Overrides AbstractPrizeStructureCreator.get_amount_instance()

        Ignores the amount parameter, and simply returns the self.ticket_amount instance

        :param amount:
        :return:
        """
        return self.ticket_amount

class FlatCashPrizeStructureCreator( AbstractPrizeStructureCreator ):
    """
    Used to create a cash prize strucutre with flat payouts.
    Flat payouts are like 50/50s or Triple ups
    """

    def __init__(self):
        pass # TODO finish this
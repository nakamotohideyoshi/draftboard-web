#
#

class AbstractDataDenParser(object):

    game_model = None

    def __init__(self):
        self.validate_models()

    def validate_models(self):
        if self.game_model is None:
            raise Exception('game_model is not set')

    def name(self):
        """
        helper method to get the class name of the instance, mainly for logging
        :return:
        """
        return self.__class__.__name__
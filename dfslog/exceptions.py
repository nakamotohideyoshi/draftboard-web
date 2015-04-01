class ErrorCodeException(Exception):
    def __init__(self):
       super(ErrorCodeException, self).__init__(\
           "error_code value passed has invalid type. Should be type ErrorCode.")

class ActionException(Exception):
    def __init__(self):
       super(ActionException, self).__init__(\
           "action value passed has invalid type. Should be type str.")

class MessageException(Exception):
    def __init__(self):
       super(MessageException, self).__init__(\
           "message value passed has invalid type. Should be type str.")



class ModelNotImplementedException(Exception):
    def __init__(self, class_name):
       super(ModelNotImplementedException, self).__init__(\
           "The model "+class_name+" does not implement the AbstractLog. This is "\
                +"required to send the model to be logged.")


class LogMethodException(Exception):
    def __init__(self, class_name):
       super(LogMethodException, self).__init__(\
           "The method in AbstractLog 'log()' was not implemented in the class "+class_name)

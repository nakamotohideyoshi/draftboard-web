class RotowireDownException(Exception):
    def __init__(self, msg):
        self.response = msg
        super().__init__(msg)
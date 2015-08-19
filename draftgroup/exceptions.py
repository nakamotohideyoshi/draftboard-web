#
# draftgroup/exceptions.py

class EmptySalaryPoolException(Exception):
    def __init__(self):
       super().__init__('There are no players in the salary pool.')


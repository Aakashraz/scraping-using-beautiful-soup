import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formating = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
file_handler = logging.FileHandler('employee.log')
file_handler.setFormatter(formating)
file_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)

# logging.basicConfig(filename='employee.log', level=logging.INFO,
#                     format='%(asctime)s: %(levelname)s: %(name)s: %(message)s')


class Employee:
    """A sample employee class to demonstrate logging"""

    def __init__(self, first, last):
        self._first = first
        self._last = last
        logger.info('Employee object created: {} - {}'.format(self.fullname, self.email))

    @property
    def email(self):
        return '{}.{}@logmail.com'.format(self._first, self._last)

    @property
    def fullname(self):
        return '{} {}'.format(self._first, self._last)


emp1 = Employee('Hero', 'Honda')
emp2 = Employee('Mary', 'Smith')
print(emp1.fullname)
print(emp2.fullname)
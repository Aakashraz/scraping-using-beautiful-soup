import logging
# import employee_log
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s: %(funcName)s')
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# logging.basicConfig(filename='test.log', level=logging.DEBUG,
#                     format='%(asctime)s-%(name)s-%(levelname)s-%(message)s-%(funcName)s')


def divide(x, y):
    return x / y


num1 = 4375
num2 = 545


if __name__ == "__main__":
    value = divide(num1, num2)
    logger.debug(f"Value: {value}")

    print(f'this is inside the log.py: {value}')
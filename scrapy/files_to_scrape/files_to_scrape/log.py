import logging
# import employee_log
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s: %(funcName)s')
file_handler = logging.FileHandler('test.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)

# to display the logging on console, using stream_handler
# the stream_handler uses the 'logger.setLevel(logging.DEBUG)' from the top
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# logging.basicConfig(filename='test.log', level=logging.DEBUG,
#                     format='%(asctime)s-%(name)s-%(levelname)s-%(message)s-%(funcName)s')


def divide(x, y):
    try:
        result = x/y
        return result
    except ZeroDivisionError:
        # to traceback the error, we use logger.exception()
        logger.exception('Cannot divide by zero')


def multiply(x, y):
    return x*y


num1 = 4375
num2 = 703


if __name__ == "__main__":
    value = divide(num1, num2)
    value_2 = multiply(num1, num2)
    logger.debug(f"INSIDE LOG.DEBUG --> Division Value: {value} \n multiplied value: {value_2}")

    print(f'this is inside the log.py\n division result: {value} \n multiplied result: {value_2}')
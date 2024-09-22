import logging


def divide(x, y):
    return x / y


num1 = 43
num2 = 54

logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s -%(funcName)s')
if __name__ == "__main__":
    value = divide(num1, num2)
    logging.debug(f"Value: {value}")
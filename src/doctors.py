import threading
import time
from functools import wraps
from loguru import logger


def Loger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        logger.info(f"function start: ({func.__name__}) with parameters: {args} :\n")
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            logger.info(f"The function ({func.__name__}) ended with the result: {result}")
            logger.info(f"The function ({func.__name__}) has been completed for {(time.perf_counter() - start):.4f}\n")
        except Exception:
            logger.exception(f"the function ({func.__name__}) ended with an error\n")
        return result

    return wrapper


class Screwdrivers(object):
    def __init__(self):
        self.thread_lock = threading.Lock()


class TimeLord(threading.Thread):
    def __init__(self, number, first_driver, second_driver):
        threading.Thread.__init__(self)
        self.id: int = number
        self.his_driver = first_driver
        self.neighbour_driver = second_driver

    def acquire_screwdrivers(self):
        self.his_driver.thread_lock.acquire()
        self.neighbour_driver.thread_lock.acquire()

    def realise_screwdrivers(self):
        self.his_driver.thread_lock.release()
        self.neighbour_driver.thread_lock.release()

    def blast(self):
        print(f"Doctor {self.id}: BLAST!")

    def run(self):
        time.sleep(0.005)
        self.acquire_screwdrivers()
        self.blast()
        self.realise_screwdrivers()


@Loger
def main():
    screwdrivers = [Screwdrivers() for _ in range(5)]
    time_lords = [TimeLord(id, screwdrivers[id - 10], screwdrivers[id - 9]) for id in range(9, 14)]
    for time_lord in time_lords:
        time_lord.start()
    for time_lord in time_lords:
        time_lord.join()


if __name__ == "__main__":
    main()

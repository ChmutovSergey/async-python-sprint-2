import heapq
import threading

from job import Job
from logger import logger


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self._pool_size: int = pool_size
        self._tasks = []

    def schedule(self, task: Job):
        logger.info("Try add task")
        heapq.heappush(self._tasks, task)

    def run(self):
        logger.info("Scheduler run")

        while True:
            print(100)
            task = heapq.heappop(self._tasks)
            _ = threading.Timer(0.3, task)

    def restart(self):
        logger.info("Scheduler restart")

    def stop(self):
        logger.info("Scheduler stop")

import datetime
import random
import time

from job import Job
from logger import logger

pause = 0


def task_for_test_0():
    logger.info(f"Started task_for_test_0")
    time.sleep(pause * 1)
    return "task_for_test_0"


def task_for_test_1():
    logger.info(f"Started task_for_test_1")
    time.sleep(pause * 2)
    return "task_for_test_1"


def task_for_test_2():
    logger.info(f"Started task_for_test_2")
    time.sleep(pause * 3)
    return "task_for_test_2"


def task_for_test_3():
    logger.info(f"Started task_for_test_3")
    time.sleep(pause * 4)
    return "task_for_test_3"


def task_for_test_inner():
    logger.info(f"Started task_for_test_3")
    time.sleep(pause * 4)
    return "task_for_test_3"


worker_tasks = {
    "task_for_test_0": task_for_test_0,
    "task_for_test_1": task_for_test_1,
    "task_for_test_2": task_for_test_2,
    "task_for_test_3": task_for_test_3,
    "task_for_test_inner": task_for_test_inner,
}


def add_task(scheduler):
    job_inner = Job(
        fn=worker_tasks["task_for_test_inner"], kwargs={},
    )
    scheduler.schedule(task=job_inner)

    for i in range(1):
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=(random.randrange(10) + 10))
        job0 = Job(
            fn=worker_tasks[f"task_for_test_{i%4}"],
            args=[],
            kwargs={},
            start_at=start_at,
            max_working_time=0,
            tries=5,
            dependencies=[job_inner]
        )
        scheduler.schedule(task=job0)

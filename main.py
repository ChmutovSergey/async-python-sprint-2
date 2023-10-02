import concurrent
from concurrent.futures import ThreadPoolExecutor

from scheduler import Scheduler

from tasks.tasks import add_task


def main():
    scheduler = Scheduler()
    scheduler_stop(scheduler)

    scheduler = Scheduler()
    scheduler_restart(scheduler)

    with ThreadPoolExecutor(max_workers=2) as pool:
        pool.submit(scheduler.run)
        pool.submit(add_task(scheduler))


def scheduler_restart(scheduler):
    scheduler.restart()


def scheduler_stop(scheduler):
    add_task(scheduler)
    scheduler.stop()


_ = concurrent.futures.Future

if __name__ == "__main__":
    main()

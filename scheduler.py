import datetime
import heapq
import json
from concurrent.futures import ThreadPoolExecutor

from job import Job
from logger import logger
from schemas import TaskSchema
from tasks.tasks import worker_tasks


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self._pool_size: int = pool_size
        self._tasks = []
        self.work_response = []

    def schedule(self, task: Job):
        heapq.heappush(self._tasks, task)
        logger.info("Task is added in Scheduler")
        if task.dependencies:
            logger.info(f"Check dependencies tasks")
            for dependencies_task in task.dependencies:
                if dependencies_task not in self._tasks:
                    self.schedule(dependencies_task)

    def get_task(self):
        logger.info("Init get_task")
        while True:
            # добавление новых потоков
            if self._tasks:
                if self._tasks[0].check_dependencies_task_is_complite() is False:
                    task = heapq.heappop(self._tasks)
                    task.set_next_start_datetime_stamp()
                    self.schedule(task)

                now_datetime_stamp = datetime.datetime.now()
                if self._tasks[0].start_datetime_stamp < now_datetime_stamp:
                    logger.info("Geting task")
                    yield heapq.heappop(self._tasks)

    @staticmethod
    def scheduler_thread(pool):
        logger.info("Init scheduler_thread")
        while True:
            task = (yield)
            logger.info("Add task in thread")
            yield pool.submit(task.run)

    def result_iterator(self):
        while True:
            task = (yield)
            logger.info("Add result task in work_response")
            task.result = task.response_future.result(timeout=task.max_working_time)

            if task.response_future.done() is False and task.tries:
                task.set_next_start_datetime_stamp()
                task.tries -= 1
                self.schedule(task)

            yield

    def run(self):
        logger.info("Scheduler run")
        with ThreadPoolExecutor(max_workers=self._pool_size) as pool:
            thread = self.scheduler_thread(pool=pool)
            next(thread)

            result_iterator = self.result_iterator()
            next(result_iterator)

            while True:
                task = next(self.get_task())
                print(f"{len(self._tasks)=}")
                task.response_future = thread.send(task)
                result_iterator.send(task)

    def restart(self):
        try:
            with open("data.json") as f:
                tasks_json = json.load(f)
        except Exception as ex:
            logger.exception(f"Error. Can't open file. {ex}")

        for task in tasks_json:
            try:
                valid_task = TaskSchema.model_validate_json(task)
            except TypeError as ex:
                logger.error(f"Error. Row is invalid. Row skip. {ex=}")
                continue

            dependencies = []

            for dependence in valid_task.dependencies:
                dependencies.append(
                    Job(
                        fn=worker_tasks.get(dependence.fn_name),
                        args=dependence.args,
                        kwargs=dependence.kwargs,
                        start_datetime_stamp=dependence.start_datetime_stamp,
                        max_working_time=dependence.max_working_time,
                        tries=dependence.tries,
                        dependencies=dependence.dependencies
                    )
                )

            task_job = Job(
                fn=worker_tasks.get(valid_task.fn_name),
                args=valid_task.args,
                kwargs=valid_task.kwargs,
                start_datetime_stamp=valid_task.start_datetime_stamp,
                max_working_time=valid_task.max_working_time,
                tries=valid_task.tries,
                dependencies=dependencies
            )
            self.schedule(task=task_job)
        logger.info("Scheduler restart")

    def stop(self):
        tasks_json = []
        for task in self._tasks:
            task_dict = task.__dict__
            task_dict["dependencies"] = [x.__dict__ for x in task_dict["dependencies"]]
            tasks_json.append(TaskSchema.model_validate(task.__dict__).model_dump_json())
        with open("data.json", "w") as f:
            json.dump(tasks_json, f)
        # здесь очередь с джобами сохраняется в файл
        logger.info("Scheduler stop")

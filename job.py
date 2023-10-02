import uuid
import datetime

from logger import logger


class Job:
    def __init__(
            self,
            fn,
            args=None,
            kwargs=None,
            start_at=None,
            start_datetime_stamp=None,
            max_working_time=None,
            tries=0,
            dependencies=None
    ):
        self._fn = fn
        self.fn_name = fn.__name__
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.start_at = start_at
        self.start_datetime_stamp = start_datetime_stamp or self.get_start_datetime_stamp(start_at)
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies if dependencies is not None else []
        self.job_id = uuid.uuid4()
        self.time_step = datetime.timedelta(minutes=10)
        self.response_future = None
        self.successfully_completed = False
        self.result = None

        self.check_dependencies_task_start_datetime()

    def set_next_start_datetime_stamp(self):
        self.start_datetime_stamp += self.time_step

    def run(self):
        try:
            return self._fn(*self.args, **self.kwargs)
        except Exception as ex:
            logger.error(f"Error. Job fail with error. {ex}")

    def pause(self):
        pass

    def stop(self):
        pass

    def check_dependencies_task_is_complite(self):
        for dependencies_task in self.dependencies:
            if dependencies_task.response_future and dependencies_task.response_future.done():
                continue
            else:
                return False
        return True

    def check_dependencies_task_start_datetime(self):
        for dependencies_task in self.dependencies:
            if dependencies_task.start_datetime_stamp > self.start_datetime_stamp:
                self.start_datetime_stamp = dependencies_task.start_datetime_stamp + datetime.timedelta(minutes=1)

    def __lt__(self, other) -> bool:
        return other.start_datetime_stamp > self.start_datetime_stamp

    def __str__(self):
        return self.start_at

    def __repr__(self):
        return f"{self.start_at}"

    @staticmethod
    def get_start_datetime_stamp(start_at: datetime.datetime):
        now = datetime.datetime.now()
        if start_at:
            if now > start_at:
                return start_at + datetime.timedelta(days=1)
            return start_at
        return now

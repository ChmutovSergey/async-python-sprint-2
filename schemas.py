import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from job import JobStatus


class TaskSchemaInner(BaseModel):
    id: UUID
    fn_name: str
    args: list
    kwargs: dict
    start_datetime: datetime.datetime
    max_working_time: Optional[int]
    tries: int
    status: JobStatus
    dependencies: list


class TaskSchema(TaskSchemaInner):
    dependencies: list[TaskSchemaInner]

from typing import Any

from app.core.utils import queue
from app.schemas.job import Job
from arq.jobs import Job as ArqJob
from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    "",
    response_model=Job,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(message: str):
    """Создать новую фоновую задачу.

    Параметры
    ----------
    message: str
        Сообщение или данные, которые будут обработаны задачей.

    Возвращает
    -------
    dict[str, str]
        Словарь, содержащий ID созданной задачи.
    """
    job = await queue.pool.enqueue_job("sample_background_task", message)  # type: ignore
    return {"id": job.job_id}


@router.get("/{task_id}")
async def get_task(task_id: str) -> dict[str, Any] | None:
    """Получить информацию о конкретной фоновой задаче.

    Параметры
    ----------
    task_id: str
        ID задачи.

    Возвращает
    -------
    Optional[dict[str, Any]]
        Словарь, содержащий информацию о задаче, если она найдена, или None в противном случае.
    """
    job = ArqJob(task_id, queue.pool)
    job_info: dict = await job.info()
    return vars(job_info)

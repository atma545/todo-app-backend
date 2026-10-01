from app.api.dependencies import get_task_service
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from app.services.task import TaskService
from fastapi import APIRouter, status, Depends

router = APIRouter(prefix='/tasks')


@router.get("", response_model=list[TaskSchema])
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()


@router.post("", status_code = status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(
    payload: TaskCreateSchema,
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.create_task(payload=payload)




@router.patch('/{task_id}', response_model=TaskSchema)
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
        return task_service.update_task(task_id=task_id, payload=payload)

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service)
) -> None:
    task_service.delete_task(task_id=task_id)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task import TaskService
from app.services.category import CategoryService
from fastapi import Depends


def get_task_service(db :Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

def get_category_service(db :Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
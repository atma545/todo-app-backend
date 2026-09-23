from uuid import uuid4



from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default= lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = 'tasks'

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default = False)


class CategoryORM(Base):
    __tablename__ = 'categories'

    name: Mapped[str]



@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None=None




def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()



@app.get("/tasks", response_model=list[TaskSchema])
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return tasks_from_db


@app.post("/tasks", status_code = status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(payload: TaskCreateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)

    db.commit()
    return new_task


@app.patch('/tasks/{task_id}', response_model=TaskSchema)
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()


@app.get('/categories', response_model=list[CategorySchema])
def read_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return categories_from_db


@app.post('/categories', response_model=CategorySchema)
def create_category(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name = payload.name)
    db.add(new_category)
    db.commit()
    return new_category


@app.patch('/categories/{category_id}', response_model=CategorySchema)
def update_category(category_id:str, payload:CategoryUpdateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    category_for_update = db.get(CategoryORM, category_id)
    if payload.name:
        category_for_update.name = payload.name

    db.commit()
    return category_for_update


@app.delete("/categories/{category_id}")
def delete_category(category_id, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM, category_id)
    db.delete(category_for_delete)
    db.commit()
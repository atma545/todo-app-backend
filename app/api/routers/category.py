from app.api.dependencies import get_category_service
from app.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from app.services.category import CategoryService
from fastapi import APIRouter, status, Depends

router = APIRouter(prefix='/categories')


@router.get('', response_model=list[CategorySchema])
def read_categories(category_service: CategoryService = Depends(get_category_service)) -> list[CategorySchema]:
    return category_service.list_category()


@router.post('', response_model=CategorySchema)
def create_category(payload: CategoryCreateSchema, category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    return category_service.create_category(payload=payload)


@router.patch('/{category_id}', response_model=CategorySchema)
def update_category(category_id:str, payload:CategoryUpdateSchema, category_service: CategoryService = Depends(get_category_service)) -> CategorySchema:
    return category_service.update_category(category_id=category_id, payload=payload)


@router.delete("/{category_id}")
def delete_category(category_id, category_service: CategoryService = Depends(get_category_service)):
    category_service.delete_category(category_id=category_id)
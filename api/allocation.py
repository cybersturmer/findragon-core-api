from typing import List

from fastapi import APIRouter
from fastapi import Depends

from models.schemas import AllocatedPieItemSchema
from services.allocation import AllocatedPieItemService

router = APIRouter(
    prefix='/allocations'
)


@router.get('/', response_model=List[AllocatedPieItemSchema])
def get_allocations(service: AllocatedPieItemService = Depends()):
    return service.get_list()

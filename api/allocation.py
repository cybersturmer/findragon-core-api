from typing import List

from fastapi import APIRouter
from fastapi import Depends

from models.allocation import AllocatedPieItemModel
from services.allocation import AllocatedPieItemService

router = APIRouter(
    prefix='/allocation'
)


@router.get('/', response_model=List[AllocatedPieItemModel])
def get_allocations(service: AllocatedPieItemService = Depends()):
    return service.get_list()

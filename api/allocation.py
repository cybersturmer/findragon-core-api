from typing import List

from fastapi import APIRouter
from fastapi import Depends

from models.schemas import PortfolioAllocatedPieItemModel
from services.allocation import AllocatedPieItemService

router = APIRouter(
    prefix='/allocation'
)


@router.get('/', response_model=List[PortfolioAllocatedPieItemModel])
def get_allocations(service: AllocatedPieItemService = Depends()):
    return service.get_list()

from fastapi import APIRouter, Depends

from models import schemas
from services.eod import EOD

router = APIRouter(
    prefix='/eod'
)


@router.get('/')
async def get(
        service: EOD = Depends()
):
    return service.get_end_of_day_data(
        exchange='MCX',
        symbol='SBER'
    )

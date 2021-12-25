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
    ticker_list = [
        'SBER.MCX',
        'GMKN.MCX'
    ]

    return service.get_live_data(
        ticker_list
    )

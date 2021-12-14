from typing import List

from fastapi import APIRouter
from fastapi import Depends

from models import schemas
from services.allocation import AllocatedPieSlice

router = APIRouter(
    prefix='/allocations'
)


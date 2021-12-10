from fastapi import APIRouter
from .allocation import router as allocation_router

router = APIRouter()
router.include_router(allocation_router)

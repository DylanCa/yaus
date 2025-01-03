from fastapi import APIRouter

from .shortener import router as shortener_router


router = APIRouter()
router.include_router(shortener_router, prefix="/short")

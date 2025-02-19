from app.core.config import settings
from fastapi import APIRouter

from .login import router as login_router
from .logout import router as logout_router

router = APIRouter(
    prefix=settings.api.auth,
)

router.include_router(
    login_router,
    tags=["Auth"],
)
router.include_router(
    logout_router,
    tags=["Auth"],
)

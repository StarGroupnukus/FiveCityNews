from app.core.auth import dependencies
from app.core.config import settings
from fastapi import APIRouter, Depends

from .post import router as post_router
from .rate_limit import router as rate_limit_router
from .tasks import router as tasks_router
from .tier import router as tier_router
from .user import router as user_router

router = APIRouter(
    prefix=settings.api_v1.prefix,
)
router.include_router(
    tasks_router,
    tags=["Task"],
    prefix=settings.api_v1.task_prefix,
    dependencies=[
        Depends(dependencies.get_current_superadmin_user),
    ],
)
router.include_router(
    user_router,
    prefix=settings.api_v1.user_prefix,
    tags=["User"],
)
router.include_router(
    post_router,
    prefix=settings.api_v1.post_prefix,
    tags=["Post"],
)
router.include_router(
    rate_limit_router,
    prefix=settings.api_v1.rate_limit_prefix,
    tags=["Rate Limit"],
    dependencies=[
        Depends(dependencies.get_current_superadmin_user),
    ],
)
router.include_router(
    tier_router,
    tags=["Tier"],
    prefix=settings.api_v1.tier_prefix,
    dependencies=[
        Depends(dependencies.get_current_superadmin_user),
    ],
)

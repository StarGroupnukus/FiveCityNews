from app.models.rate_limit import RateLimit
from app.schemas.rate_limit import (
    RateLimitCreateInternal,
    RateLimitDelete,
    RateLimitFilter,
    RateLimitUpdate,
    RateLimitUpdateInternal,
)
from fastcrud import FastCRUD

CRUDRateLimit = FastCRUD[
    RateLimit,
    RateLimitCreateInternal,
    RateLimitUpdate,
    RateLimitUpdateInternal,
    RateLimitDelete,
    RateLimitFilter,
]
crud_rate_limits = CRUDRateLimit(RateLimit)

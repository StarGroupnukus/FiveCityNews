from app.models.tier import Tier
from app.schemas.tier import (
    TierCreateInternal,
    TierDelete,
    TierFilter,
    TierUpdate,
    TierUpdateInternal,
)
from fastcrud import FastCRUD

CRUDTier = FastCRUD[
    Tier,
    TierCreateInternal,
    TierUpdate,
    TierUpdateInternal,
    TierDelete,
    TierFilter,
]
crud_tiers = CRUDTier(Tier)

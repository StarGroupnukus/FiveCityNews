import asyncio

from app.core import db_helper
from app.core.config import config
from app.core.logger import logging
from app.models.tier import Tier
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def create_first_tier(session: AsyncSession) -> None:
    try:
        tier_name = config("TIER_NAME", default="free")

        query = select(Tier).where(Tier.name == tier_name)
        result = await session.execute(query)
        tier = result.scalar_one_or_none()

        if tier is None:
            session.add(Tier(name=tier_name))
            await session.commit()
            logger.info(f"Tier '{tier_name}' created successfully.")

        else:
            logger.info(f"Tier '{tier_name}' already exists.")

    except Exception as e:
        logger.error(f"Error creating tier: {e}")


async def main():
    async with db_helper.session_factory() as session:
        await create_first_tier(session)


if __name__ == "__main__":
    asyncio.run(main())

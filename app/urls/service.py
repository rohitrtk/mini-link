from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.urls.base62 import generate_base62_code
from app.urls.model import ShortUrl
from app.urls.schemas import ShortUrlCreate

MAX_GENERATION_ATTEMPTS = 10
UNIQUE_VIOLATION_SQLSTATE = '23505'


def is_unique_violation(error: IntegrityError) -> bool:
    sqlstate = getattr(error.orig, 'sqlstate', None) or getattr(error.orig, 'pgcode', None)

    return sqlstate == UNIQUE_VIOLATION_SQLSTATE


async def create_or_get_short_url(session: AsyncSession, data: ShortUrlCreate) -> ShortUrl:
    target_url = str(data.url)
    last_error: IntegrityError | None = None

    for _ in range(MAX_GENERATION_ATTEMPTS):
        statement = (
            insert(ShortUrl)
            .values(
                short_code=generate_base62_code(),
                target_url=target_url,
                number_of_creations=1
            )
            .on_conflict_do_update(
                constraint='uq_short_urls_target_url',
                set_={
                    'number_of_creations': ShortUrl.number_of_creations + 1,
                    'last_created_at': func.now()
                }
            )
            .returning(ShortUrl)
        )

        try:
            result = await session.scalars(
                statement,
                execution_options={'populate_existing': True}
            )
            short_url = result.one()

            await session.commit()

            return short_url
        except IntegrityError as error:
            await session.rollback()
            if not is_unique_violation(error):
                raise

            last_error = error

    raise RuntimeError('Could not generate a unique short code') from last_error


async def get_short_url(session: AsyncSession, short_code: str) -> ShortUrl | None:
    statement = select(ShortUrl).where(ShortUrl.short_code == short_code)

    return await session.scalar(statement)
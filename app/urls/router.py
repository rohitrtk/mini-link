from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.urls.schemas import ShortUrlCreate, ShortUrlRead
from app.urls.service import create_or_get_short_url, get_short_url

router = APIRouter(tags=['URLs'])

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


@router.post('/shorten', response_model=ShortUrlRead, status_code=status.HTTP_200_OK)
async def shorten_url(data: ShortUrlCreate, session: SessionDependency) -> ShortUrlRead:
    short_url = await create_or_get_short_url(session, data)
    return ShortUrlRead.model_validate(short_url)

@router.get(
    '/{short_code}',
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def resolve_short_url(short_code: str, session: SessionDependency) -> RedirectResponse:
    short_url = await get_short_url(session, short_code)

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Short URL not found')

    return RedirectResponse(url=short_url.target_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

from app.core.auth import dependencies
from app.core.exceptions.http_exceptions import UnauthorizedException
from fastapi import APIRouter, Depends, Response
from jwt import InvalidTokenError

router = APIRouter()


@router.post(
    "/logout",
    dependencies=[Depends(dependencies.get_current_auth_user)],
)
async def logout(
    response: Response,
):
    try:
        response.delete_cookie(key="refresh_token")

        # todo: add token to  blacklist

        return {"message": "Logged out successfully"}

    except InvalidTokenError:
        raise UnauthorizedException("Invalid token.")

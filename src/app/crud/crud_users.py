from app.models.user import User
from app.schemas.user import (
    UserCreateInternal,
    UserDelete,
    UserFilter,
    UserUpdate,
    UserUpdateInternal,
)
from fastcrud import FastCRUD

CRUDUser = FastCRUD[
    User,
    UserCreateInternal,
    UserUpdate,
    UserUpdateInternal,
    UserDelete,
    UserFilter,
]
crud_users = CRUDUser(User)

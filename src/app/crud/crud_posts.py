from app.models.post import Post
from app.schemas.post import (
    PostCreateInternal,
    PostDelete,
    PostFilter,
    PostUpdate,
    PostUpdateInternal,
)
from fastcrud import FastCRUD

CRUDPost = FastCRUD[
    Post,
    PostCreateInternal,
    PostUpdate,
    PostUpdateInternal,
    PostDelete,
    PostFilter,
]
crud_posts = CRUDPost(Post)

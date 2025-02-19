<h1 align="center"> My FastAPI template </h1>
<p align="center" markdown=1>
  <span>Yet another template to speed your FastAPI development up. <br>Made with ❤️ by <a href="https://github.com/al1enn">AL1EN</a>.</span>
</p>

<p align="center">
  <a href="https://github.com/igormagalhaesr/FastAPI-boilerplate">
    <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI logo" width="50%" height="auto">
  </a>
</p>

<p align="center">
<a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white"
      alt="Python">
  </a>
  <a href="https://fastapi.tiangolo.com">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  </a>
  <a href="https://docs.pydantic.dev/2.4/">
      <img src="https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=for-the-badge" alt="Pydantic">
  </a>
  <a href="https://www.postgresql.org">
      <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
  <a href="https://redis.io">
      <img src="https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=fff&style=for-the-badge" alt="Redis">
  </a>
  <a href="https://docs.docker.com/compose/">
      <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge" alt="Docker">
  </a>
  <a href="https://nginx.org/en/">
      <img src="https://img.shields.io/badge/NGINX-009639?logo=nginx&logoColor=fff&style=for-the-badge" alt=NGINX>
  </a>
</p>

## Todo

- [ ] Add tests
- [ ] Add caching
- [ ] Add monitoring (Grafana)
- [ ] Add running with nginx
- [ ] Add version with DAO
- [ ] Add CI/CD

## 0. About

- [`FastAPI`](https://fastapi.tiangolo.com): modern Python web framework for building APIs
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/): the most widely used data Python validation library, rewritten in Rust [`(5x-50x faster)`](https://docs.pydantic.dev/latest/blog/pydantic-v2-alpha/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html): Python SQL toolkit and Object Relational Mapper
- [`PostgreSQL`](https://www.postgresql.org): The World's Most Advanced Open Source Relational Database
- [`Redis`](https://redis.io): Open source, in-memory data store used by millions as a cache, message broker and more.
- [`ARQ`](https://arq-docs.helpmanual.io) Job queues and RPC in python with asyncio and redis.
- [`Docker Compose`](https://docs.docker.com/compose/) With a single command, create and start all the services from your configuration.
- [`NGINX`](https://nginx.org/en/) High-performance low resource consumption web server used for Reverse Proxy and Load Balancing.

> If you want the `DAO` version instead, head to [dao branch](https://github.com/al1enn/my-fastapi-base-app/tree/dao).

## 1. Contents

0. [About](#0-about)
1. [Contents](#1-contents)
1. [Prerequisites](#2-prerequisites)
   1. [Environment Variables (.env)](#21-environment-variables-env)
1. [Usage](#3-usage)
   1. [Docker Compose](#31-docker-compose)
   1. [From Scratch](#32-from-scratch)
      1. [Packages](#321-packages)
      1. [Running PostgreSQL With Docker](#322-running-postgresql-with-docker)
      1. [Running Redis with Docker](#323-running-redis-with-docker)
      1. [Running the API](#324-running-the-api)
   1. [Creating the first superuser](#33-creating-the-first-superuser)
   1. [Database Migrations](#34-database-migrations)
1. [Extending](#4-extending)
   1. [Database Model](#41-database-model)
   1. [Token Blacklist](#42-token-blacklist)
   1. [SQLAlchemy Models](#43-sqlalchemy-models)
   1. [Pydantic Schemas](#44-pydantic-schemas)
   1. [Alembic Migrations](#45-alembic-migrations)
   1. [CRUD](#46-crud)
      1. [Get](#461-get)
      1. [Get Multi](#462-get-multi)
      1. [Create](#463-create)
      1. [Exists](#464-exists)
      1. [Count](#465-count)
      1. [Update](#466-update)
      1. [Delete](#467-delete)
      1. [Get Joined](#468-get-joined)
      1. [Get Multi Joined](#469-get-multi-joined)
   1. [Routes](#47-routes)
      1. [Paginated Responses](#471-paginated-responses)
      1. [HTTP Exceptions](#472-http-exceptions)
   1. [Caching](#48-caching)
   1. [More Advanced Caching](#49-more-advanced-caching)
   1. [ARQ Job Queues](#410-arq-job-queues)
   1. [Rate Limiting](#411-rate-limiting)
   1. [JWT Authentication](#412-jwt-authentication)
      1. [Details](#4121-details)
      1. [Usage](#4122-usage)
      1. [Running](#413-running)
   1. [Create Application](#414-create-application)
   1. [Logging](#415-logging)
   1. [Redis, Queue, Rate Limiter](#416-redis-queue-rate-limiter)
1. [Running in Production](#5-running-in-production)
   1. [Uvicorn Workers with Gunicorn](#51-uvicorn-workers-with-gunicorn)
   1. [Running with NGINX](#52-running-with-nginx)
1. [Testing](#6-testing)
   1. [Docker Compose](#61-docker-compose)
1. [References](#7-references)
1. [Resources](#8-resources)

## 2. Prerequisites

### 2.0 Start

Start by using the template, and naming the repository to what you want.

![alt text](./images/image.png)

Then clone your created repository (I'm using the base for the example)

```sh
git clone https://github.com/al1enn/my-fastapi-base-app
```

### 2.1 Environment Variables (.env)

Then create a `.env` file inside `src` directory:

```sh
touch .env
```

Inside of `.env`, create the following app settings variables:

```
# ------------- app settings -------------
APP_NAME="Your app name here"
APP_DESCRIPTION="Your app description here"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="The license you picked"

# ------------- run -------------
RUN__HOST=0.0.0.0
RUN__PORT=8000

# ------------- gunicorn -------------
GUNICORN__WORKERS=1
GUNICORN__TIMEOUT=900
```

For the database ([`if you don't have a database yet, click here`](#322-running-postgresql-with-docker)), create:

```
# ------------- database -------------
DB__ECHO=1
DB__CREATE_TABLES_ON_START=False

# ------------- postgres -------------
POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_password"
POSTGRES_SERVER="your_server" # default "localhost", if using docker compose you should use "db"
POSTGRES_PORT=5432 # default "5432", if using docker compose you should use "5432"
POSTGRES_DB="your_db"

# ------------- pgadmin -------------
PGADMIN_DEFAULT_EMAIL="your_email_address"
PGADMIN_DEFAULT_PASSWORD="your_password"
PGADMIN_LISTEN_PORT=80
```

For jwt-keys runn commands in the certs directory [`README.md`](./src/certs/README.md).

```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

```
# ------------- jwt -------------
ALGORITHM= # pick an algorithm, default RS256
ACCESS_TOKEN_EXPIRE_MINUTES= # minutes until token expires, default 30
REFRESH_TOKEN_EXPIRE_DAYS= # days until token expires, default 7
TOKEN_TYPE_FIELD="type"
ACCESS_TOKEN_TYPE="access"
REFRESH_TOKEN_TYPE="refresh"
```

For redis:

```
# ------------- redis-------------
REDIS_CLIENT_HOST="your_host" # default "localhost", if using docker compose you should use "redis"
REDIS_CLIENT_PORT=6379 # default "6379", if using docker compose you should use "6379"

# ------------- redis cache-------------
REDIS_CACHE_HOST="your_host" # default "localhost", if using docker compose you should use "redis"
REDIS_CACHE_PORT=6379 # default "6379", if using docker compose you should use "6379"

# ------------- redis queue -------------
REDIS_QUEUE_HOST="your_host" # default "localhost", if using docker compose you should use "redis"
REDIS_QUEUE_PORT=6379 # default "6379", if using docker compose you should use "6379"

# ------------- redis rate limit -------------
REDIS_RATE_LIMIT_HOST="localhost"   # default="localhost", if using docker compose you should use "redis"
REDIS_RATE_LIMIT_PORT=6379          # default=6379, if using docker compose you should use "6379"

# ------------- default rate limit settings -------------
DEFAULT_RATE_LIMIT_LIMIT=1
DEFAULT_RATE_LIMIT_PERIOD=60

# ------------- client-side cache -------------
CLIENT_CACHE_MAX_AGE=30 # default "30"
```

> You may use the same redis for both caching and queue while developing, but the recommendation is using two separate containers for production.

To create the first admin and tier:

```
# ------------- admin -------------
ADMIN_NAME="your_name"
ADMIN_EMAIL="your_email"
ADMIN_USERNAME="your_username"
ADMIN_PASSWORD="your_password"

# ------------- first tier -------------
TIER_NAME="free"
```

And Finally the environment:

```
# ------------- environment -------------
ENVIRONMENT="local"
```

`ENVIRONMENT` can be one of `local`, `staging` and `production`, defaults to local, and changes the behavior of api `docs` endpoints:

- **local:** `/docs`, `/redoc` and `/openapi.json` available
- **staging:** `/docs`, `/redoc` and `/openapi.json` available for superusers
- **production:** `/docs`, `/redoc` and `/openapi.json` not available

## 3. Usage

### 3.1 Docker Compose

```sh
make build
```

You should have a `web` container, `postgres` container, a `worker` container and a `redis` container running.

### 3.2 From Scratch

#### 3.2.1. Packages

In the `root` directory, run to install required packages:

```sh
poetry install
```

#### 3.2.2. Running PostgreSQL With Docker

Install docker if you don't have it yet, then run:

```sh
docker pull postgres
```

And pick the port, name, user and password, replacing the fields:

```sh
docker run -d \
    -p {PORT}:{PORT} \
    --name {NAME} \
    -e POSTGRES_PASSWORD={PASSWORD} \
    -e POSTGRES_USER={USER} \
    postgres
```

Such as:

```sh
docker run -d \
    -p 5432:5432 \
    --name postgres \
    -e POSTGRES_PASSWORD=1234 \
    -e POSTGRES_USER=postgres \
    postgres
```

#### 3.2.3. Running redis With Docker

Install docker if you don't have it yet, then run:

```sh
docker pull redis:alpine
```

And pick the name and port, replacing the fields:

```sh
docker run -d \
  --name {NAME}  \
  -p {PORT}:{PORT} \
redis:alpine
```

Such as

```sh
docker run -d \
  --name redis  \
  -p 6379:6379 \
redis:alpine
```

#### 3.2.4. Running the API

While in the `root` folder, run to start the application with uvicorn server:

```sh
poetry run uvicorn src.app.main:app --reload
```

### 3.3 Creating the first superuser

#### 3.3.1 Docker Compose

> Make sure DB and tables are created before running create_superuser (db should be running and the api should run at least once before)

If you are using docker compose, you should uncomment this part of the docker-compose.yml:

```
  #-------- uncomment to create first superuser --------
  # create_superuser:
  #   build:
  #     context: .
  #     dockerfile: Dockerfile
  #   env_file:
  #     - ./src/.env
  #   depends_on:
  #     - db
  #   command: python -m src.scripts.create_first_superuser
  #   volumes:
  #     - ./src:/code/src
```

Getting:

```
  #-------- uncomment to create first superuser --------
  create_superuser:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - ./src/.env
    depends_on:
      - db
    command: python -m src.scripts.create_first_superuser
    volumes:
      - ./src:/code/src
```

While in the base project folder run to start the services:

```sh
make start
```

It will automatically run the create_superuser script as well, but if you want to rerun eventually:

```sh
docker-compose run --rm create_superuser
```

to stop the create_superuser service:

```sh
docker-compose stop create_superuser
```

#### 3.3.2 From Scratch

While in the `root` folder, run (after you started the application at least once to create the tables):

```sh
poetry run python -m src.scripts.create_first_superuser
```

### 3.3.3 Creating the first tier

> Make sure DB and tables are created before running create_tier (db should be running and the api should run at least once before)

To create the first tier it's similar, you just replace `create_superuser` for `create_tier` service or `create_first_superuser` to `create_first_tier` for scripts. If using `docker compose`, do not forget to uncomment the `create_tier` service in `docker-compose.yml`.

### 3.4 Database Migrations

> To create the tables if you did not create the endpoints, ensure that you import the models in src/app/models/__init__.py. This step is crucial to create the new tables.

If you are using the db in docker, you need to change this in `docker-compose.yml` to run migrations:

```sh
  db:
    image: postgres:13
    env_file:
      - ./src/.env
    volumes:
      - postgres-data:/var/lib/postgresql/data
    # -------- replace with comment to run migrations with docker --------
    expose:
      - "5432"
    # ports:
    #  - 5432:5432
```

Getting:

```sh
  db:
    ...
    # expose:
    #  - "5432"
    ports:
      - 5432:5432
```

While in the `src` folder, run Alembic migrations:

```sh
poetry run alembic revision --autogenerate
```

And to apply the migration

```sh
poetry run alembic upgrade head
```

## 4. Extending

### 4.1 Database Model

Create the new entities and relationships and add them to the model <br>
![diagram](./images/image2.png)

#### 4.2.1 Token Blacklist

Note that this table is used to blacklist the `JWT` tokens (it's how you log a user out) <br>
![diagram](./images/image3.png)

### 4.3 SQLAlchemy Models

Inside `app/models`, create a new `entity.py` for each new entity (replacing entity with the name) and define the attributes according to [SQLAlchemy 2.0 standards](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-styles):

```python
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base
from .mixins import IntIdPkMixin


class Entity(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(String(30))
    ...
```

### 4.4 Pydantic Schemas

Inside `app/schemas`, create a new `entity.py` for each new entity (replacing entity with the name) and create the schemas according to [Pydantic V2](https://docs.pydantic.dev/latest/#pydantic-examples) standards:

```python
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, HttpUrl, ConfigDict


class EntityBase(BaseModel):
    name: Annotated[
        str,
        Field(min_length=2, max_length=30, examples=["Entity Name"]),
    ]


class Entity(EntityBase):
    ...


class EntityRead(EntityBase):
    ...


class EntityCreate(EntityBase):
    ...


class EntityCreateInternal(EntityCreate):
    ...


class EntityUpdate(BaseModel):
    ...


class EntityUpdateInternal(BaseModel):
    ...


class EntityDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
```

### 4.5 Alembic Migrations

> To create the tables if you did not create the endpoints, ensure that you import the models in src/app/models/__init__.py. This step is crucial to create the new models.

Then, while in the `src` folder, run Alembic migrations:

```sh
poetry run alembic revision --autogenerate
```

And to apply the migration

```sh
poetry run alembic upgrade head
```

### 4.6 CRUD

Inside `app/crud`, create a new `crud_entities.py` inheriting from `FastCRUD` for each new entity:

```python
from fastcrud import FastCRUD

from app.models.entity import Entity
from app.schemas.entity import (
  EntityCreateInternal,
  EntityUpdate,
  EntityUpdateInternal,
  EntityDelete,
  EntitySelect,
)

CRUDEntity = FastCRUD[
  Entity,
  EntityCreateInternal,
  EntityUpdate,
  EntityUpdateInternal,
  EntityDelete,
  EntitySelect,
]
crud_entity = CRUDEntity(Entity)
```

So, for users:

```python
# crud_users.py
from app.model.user import User
from app.schemas.user import (
  UserCreateInternal,
  UserUpdate,
  UserUpdateInternal,
  UserDelete,
  UserSelect,
)

CRUDUser = FastCRUD[
  User,
  UserCreateInternal,
  UserUpdate,
  UserUpdateInternal,
  UserDelete,
  UserSelect,
]
crud_users = CRUDUser(User)
```

#### 4.6.1 Get

When actually using the crud in an endpoint, to get data you just pass the database connection and the attributes as kwargs:

```python
# Here I'm getting the first user with email == user.email (email is unique in this case)
user = await crud_users.get(
  db=session,
  email=user.email,
)
```

#### 4.6.2 Get Multi

To get a list of objects with the attributes, you should use the get_multi:

```python
# Here I'm getting at most 10 users with the name 'User Userson' except for the first 3
user = await crud_users.get_multi(
  db=session,
  offset=3,
  limit=10,
  name="User Userson"
)
```

> Note that get_multi returns a python `dict`.

Which will return a python dict with the following structure:

```javascript
{
  "data": [
    {
      "id": 4,
      "name": "User Userson",
      "username": "userson4",
      "email": "user.userson4@example.com",
      "profile_image_url": "https://profileimageurl.com"
    },
    {
      "id": 5,
      "name": "User Userson",
      "username": "userson5",
      "email": "user.userson5@example.com",
      "profile_image_url": "https://profileimageurl.com"
    }
  ],
  "total_count": 2,
  "has_more": false,
  "page": 1,
  "items_per_page": 10
}
```

#### 4.6.3 Create

To create, you pass a `CreateSchemaType` object with the attributes, such as a `UserCreate` pydantic schema:

```python
from app.schemas.user import UserCreate

# Creating the object
user_internal = UserCreate(
  name="user",
  username="myusername",
  email="user@example.com",
)

# Passing the object to be created
crud_users.create(
  db=session,
  object=user_internal,
)
```

#### 4.6.4 Exists

To just check if there is at least one row that matches a certain set of attributes, you should use `exists`

```python
# This queries only the email variable
# It returns True if there's at least one or False if there is none
crud_users.exists(
  db=session,
  email="user@example.com",
)
```

#### 4.6.5 Count

You can also get the count of a certain object with the specified filter:

```python
# Here I'm getting the count of users with the name 'User Userson'
user = await crud_users.count(
  db=session,
  name="User Userson",
)
```

#### 4.6.6 Update

To update you pass an `object` which may be a `pydantic schema` or just a regular `dict`, and the kwargs.
You will update with `objects` the rows that match your `kwargs`.

```python
# Here I'm updating the user with username == "myusername".
# #I'll change his name to "Updated Name"
crud_users.update(
  db=session,
  object={"name": "Updated Name"},
  username="myusername",
)
```

#### 4.6.7 Delete

To delete we have two options:

- db_delete: actually deletes the row from the database
- delete:
  - adds `"is_deleted": True` and `deleted_at: datetime.now(UTC)` if the model inherits from `PersistentDeletion` (performs a soft delete), but keeps the object in the database.
  - actually deletes the row from the database if the model does not inherit from `PersistentDeletion`

```python
# Here I'll just change is_deleted to True
crud_users.delete(
  db=session,
  username="myusername",
)

# Here I actually delete it from the database
crud_users.db_delete(
  db=session,
  username="myusername",
)
```

#### 4.6.8 Get Joined

To retrieve data with a join operation, you can use the get_joined method from your CRUD module. Here's how to do it:

```python
# Fetch a single record with a join on another model (e.g., User and Tier).
result = await crud_users.get_joined(
    db=session,  # The SQLAlchemy async session.
    join_model=Tier,  # The model to join with (e.g., Tier).
    schema_to_select=UserSchema,  # Pydantic schema for selecting User model columns (optional).
    join_schema_to_select=TierSchema,  # Pydantic schema for selecting Tier model columns (optional).
)
```

**Relevant Parameters:**

- `join_model`: The model you want to join with (e.g., Tier).
- `join_prefix`: Optional prefix to be added to all columns of the joined model. If None, no prefix is added.
- `join_on`: SQLAlchemy Join object for specifying the ON clause of the join. If None, the join condition is auto-detected based on foreign keys.
- `schema_to_select`: A Pydantic schema to select specific columns from the primary model (e.g., UserSchema).
- `join_schema_to_select`: A Pydantic schema to select specific columns from the joined model (e.g., TierSchema).
- `join_type`: pecifies the type of join operation to perform. Can be "left" for a left outer join or "inner" for an inner join. Default "left".
- `kwargs`: Filters to apply to the primary query.

This method allows you to perform a join operation, selecting columns from both models, and retrieve a single record.

#### 4.6.9 Get Multi Joined

Similarly, to retrieve multiple records with a join operation, you can use the get_multi_joined method. Here's how:

```python
# Retrieve a list of objects with a join on another model (e.g., User and Tier).
result = await crud_users.get_multi_joined(
    db=session,  # The SQLAlchemy async session.
    join_model=Tier,  # The model to join with (e.g., Tier).
    join_prefix="tier_",  # Optional prefix for joined model columns.
    join_on=and_(User.tier_id == Tier.id, User.is_superuser == True),  # Custom join condition.
    schema_to_select=UserSchema,  # Pydantic schema for selecting User model columns.
    join_schema_to_select=TierSchema,  # Pydantic schema for selecting Tier model columns.
    username="john_doe",  # Additional filter parameters.
)
```

**Relevant Parameters:**

- `join_model`: The model you want to join with (e.g., Tier).
- `join_prefix`: Optional prefix to be added to all columns of the joined model. If None, no prefix is added.
- `join_on`: SQLAlchemy Join object for specifying the ON clause of the join. If None, the join condition is auto-detected based on foreign keys.
- `schema_to_select`: A Pydantic schema to select specific columns from the primary model (e.g., UserSchema).
- `join_schema_to_select`: A Pydantic schema to select specific columns from the joined model (e.g., TierSchema).
- `join_type`: pecifies the type of join operation to perform. Can be "left" for a left outer join or "inner" for an inner join. Default "left".
- `kwargs`: Filters to apply to the primary query.
- `offset`: The offset (number of records to skip) for pagination. Default 0.
- `limit`: The limit (maximum number of records to return) for pagination. Default 100.
- `kwargs`: Filters to apply to the primary query.

#### More Efficient Selecting

For the `get` and `get_multi` methods we have the option to define a `schema_to_select` attribute, which is what actually makes the queries more efficient. When you pass a `pydantic schema` (preferred) or a list of the names of the attributes in `schema_to_select` to the `get` or `get_multi` methods, only the attributes in the schema will be selected.

```python
from app.schemas.user import UserRead

# Here it's selecting all of the user's data
crud_user.get(
  db=session,
  username="myusername",
)

# Now it's only selecting the data that is in UserRead.
# Since that's my response_model, it's all I need
crud_user.get(
  db=session,
  username="myusername",
  schema_to_select=UserRead,
)
```

### 4.7 Routes

Inside `app/api/v1`, create a new `entities.py` file and create the desired routes

```python
from typing import Annotated

from fastapi import Depends

from app.schemas.entity import EntityRead
from app.core import db_helper
...

router = fastapi.APIRouter()


@router.get("/{id}", response_model=EntityRead)
async def get_entity(
  request: Request,
  id: int,
  session: Annotated[AsyncSession, Depends(db_helper.get_session)]
):
    entity = await crud_entities.get(db=session, id=id)

    return entity


...
```

Then in `app/api/v1/__init__.py` add the router such as:

```python
from fastapi import APIRouter
from app.api.v1.entity import router as entity_router

...

router = APIRouter(prefix="/v1")  # this should be there already
...
router.include_router(
  entity_router,
  prefix="/entity",
  tags=["entity"],
)
```

#### 4.7.1 Paginated Responses

With the `get_multi` method we get a python `dict` with full suport for pagination:

```javascript
{
  "data": [
    {
      "id": 4,
      "name": "User Userson",
      "username": "userson4",
      "email": "user.userson4@example.com",
      "profile_image_url": "https://profileimageurl.com"
    },
    {
      "id": 5,
      "name": "User Userson",
      "username": "userson5",
      "email": "user.userson5@example.com",
      "profile_image_url": "https://profileimageurl.com"
    }
  ],
  "total_count": 2,
  "has_more": false,
  "page": 1,
  "items_per_page": 10
}
```

And in the endpoint, we can import from `fastcrud.paginated` the following functions and Pydantic Schema:

```python
from fastcrud.paginated import (
    PaginatedListResponse,  # What you'll use as a response_model to validate
    paginated_response,  # Creates a paginated response based on the parameters
    compute_offset,  # Calculate the offset for pagination ((page - 1) * items_per_page)
)
```

Then let's create the endpoint:

```python
import fastapi

from app.schemas.entity import EntityRead

...


@router.get("/entities", response_model=PaginatedListResponse[EntityRead])
async def read_entities(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
):
    entities_data = await crud_entity.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead,
        is_deleted=False,
    )

    return paginated_response(
      crud_data=entities_data,
      page=page,
      items_per_page=items_per_page,
    )
```

#### 4.7.2 HTTP Exceptions

To add exceptions you may just import from `app/core/exceptions/http_exceptions` and optionally add a detail:

```python
from app.core.exceptions.http_exceptions import NotFoundException

# If you want to specify the detail, just add the message
if not user:
    raise NotFoundException("User not found")

# Or you may just use the default message
if not post:
    raise NotFoundException()
```

**The predefined possibilities in http_exceptions are the following:**

- `CustomException`: 500 internal error
- `BadRequestException`: 400 bad request
- `NotFoundException`: 404 not found
- `ForbiddenException`: 403 forbidden
- `UnauthorizedException`: 401 unauthorized
- `UnprocessableEntityException`: 422 unprocessable entity
- `DuplicateValueException`: 422 unprocessable entity
- `RateLimitException`: 429 too many requests

### 4.8 Caching

Soon

### 4.9 More Advanced Caching

The behaviour of the `cache` decorator changes based on the request method of your endpoint.
It caches the result if you are passing it to a **GET** endpoint, and it invalidates the cache with this key_prefix and id if passed to other endpoints (**PATCH**, **DELETE**).

#### Invalidating Extra Keys

Soon

#### Invalidate Extra By Pattern

Soon

#### Client-side Caching

For `client-side caching`, all you have to do is let the `Settings` class defined in `app/core/config.py` inherit from the `ClientSideCacheSettings` class. You can set the `CLIENT_CACHE_MAX_AGE` value in `.env,` it defaults to 60 (seconds).

In `main.py`:

```python
from app.core.middleware import ClientCacheMiddleware
from app.core.config import settings

main_app.add_middleware(
            ClientCacheMiddleware,
            max_age=settings.client_side_cache.CLIENT_CACHE_MAX_AGE
        )
```

### 4.10 ARQ Job Queues

Depending on the problem your API is solving, you might want to implement a job queue. A job queue allows you to run tasks in the background, and is usually aimed at functions that require longer run times and don't directly impact user response in your frontend. As a rule of thumb, if a task takes more than 2 seconds to run, can be executed asynchronously, and its result is not needed for the next step of the user's interaction, then it is a good candidate for the job queue.

#### Background task creation

For simple background tasks, you can just create a function in the `app/core/worker/functions.py` file. For more complex tasks, we recommend you to create a new file in the `app/core/worker` directory.

```python
async def sample_background_task(ctx, name: str) -> str:
    await asyncio.sleep(5)
    return f"Task {name} is complete!"
```

Then add the function to the `WorkerSettings` class `functions` variable in `app/core/worker/settings.py` to make it available to the worker. If you created a new file in the `app/core/worker` directory, then simply import this function in the `app/core/worker/settings.py` file:

```python
from .functions import sample_background_task
from .your_module import sample_complex_background_task

class WorkerSettings:
    functions = [
        sample_background_task,
        sample_complex_background_task,
    ]
    ...
```

#### Add the task to an endpoint

Once you have created the background task, you can add it to any endpoint of your choice to be enqueued. The best practice is to enqueue the task in a **POST** endpoint, while having a **GET** endpoint to get more information on the task. For more details on how job results are handled, check the [ARQ docs](https://arq-docs.helpmanual.io/#job-results).

In `app/api/v1/tasks.py`:

```python
@router.post("/", response_model=Job, status_code=201)
async def create_task(message: str):
    job = await queue.pool.enqueue_job("sample_background_task", message)
    return {"id": job.job_id}


@router.get("/{task_id}")
async def get_task(task_id: str):
    job = ArqJob(task_id, queue.pool)
    return await job.info()

```

And finally run the worker in parallel to your fastapi application.

> For any change to the `sample_background_task` to be reflected in the worker, you need to restart the worker (e.g. the docker container).

If you are using `docker compose`, the worker is already running.
If you are doing it from scratch, run while in the `root` folder:

```sh
poetry run arq src.app.core.worker.settings.WorkerSettings
```

#### Database session with background tasks

With time your background functions will become 'workflows' increasing in complexity and requirements. Probably, you will need to use a database session to get, create, update, or delete data as part of this workflow.

To do this, you can add the database session to the `ctx` object in the `startup` and `shutdown` functions in `app/core/worker/functions.py`, like in the example below:

```python
from arq.worker import Worker
from ...core.db.database import async_get_db

async def startup(ctx: Worker) -> None:
    ctx["db"] = await anext(async_get_db())
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    await ctx["db"].close()
    logging.info("Worker end")
```

This will allow you to have the async database session always available in any background function and automatically close it on worker shutdown. Once you have this database session, you can use it as follows:

```python
from arq.worker import Worker

async def your_background_function(
    ctx: Worker,
    post_id: int,
    ...
) -> Any:
    session = ctx["db"]
    post = crud_posts.get(
        db=session,
        schema_to_select=PostRead,
        id=post_id,
    )
    ...
```

> When using database sessions, you will want to use Pydantic objects. However, these objects don't mingle well with the seralization required by ARQ tasks and will be retrieved as a dictionary.

### 4.11 Rate Limiting

To limit how many times a user can make a request in a certain interval of time (very useful to create subscription plans or just to protect your API against DDOS), you may just use the `rate_limiter` dependency:

```python
from fastapi import Depends, status

from ..dependencies import rate_limiter
from app.schemas.post import PostRead


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter)],
)
...
```

By default, if no token is passed in the header (that is - the user is not authenticated), the user will be limited by his IP address with the default `limit` (how many times the user can make this request every period) and `period` (time in seconds) defined in `.env`.

Even though this is useful, real power comes from creating `tiers` (categories of users) and standard `rate_limits` (`limits` and `periods` defined for specific `paths` - that is - endpoints) for these tiers.

All of the `tier` and `rate_limit` models, schemas, and endpoints are already created in the respective folders (and usable only by superusers). You may use the `create_tier` script to create the first tier (it uses the `.env` variable `TIER_NAME`, which is all you need to create a tier) or just use the api:

Now, whenever an authenticated user makes a `POST` request to the `api/v1/post/`, they'll use the quota that is defined by their tier.
You may check this getting the token from the `api/v1/login` endpoint, then passing it in the request header:

> Since the `rate_limiter` dependency uses the `get_optional_user` dependency instead of `get_current_user`, it will not require authentication to be used, but will behave accordingly if the user is authenticated (and token is passed in header). If you want to ensure authentication, also use `get_current_user` if you need.

To change a user's tier, you may just use the `PATCH api/v1/user/{username}/tier` endpoint.
Note that for flexibility (since this is a boilerplate), it's not necessary to previously inform a tier_id to create a user, but you probably should set every user to a certain tier (let's say `free`) once they are created.

> If a user does not have a `tier` or the tier does not have a defined `rate limit` for the path and the token is still passed to the request, the default `limit` and `period` will be used, this will be saved in `app/logs`.

### 4.12 JWT Authentication

#### 4.12.1 Details

The `access token` is short lived (default 30 minutes) to reduce the damage of a potential leak. The `refresh token`, on the other hand, is long lived (default 30 days), and you use it to renew your `access token` without the need to provide username and password every time it expires.

Since the `refresh token` lasts for a longer time, it's stored as a cookie in a secure way:

```python
# app/api/auth/login

...
response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,  # Prevent access through JavaScript
    secure=True,  # Ensure cookie is sent over HTTPS only
    samesite="Lax",  # Default to Lax for reasonable balance between security and usability
    max_age=number_of_seconds,  # Set a max age for the cookie
)
...
```

You may change it to suit your needs. The possible options for `samesite` are:

- `Lax`: Cookies will be sent in top-level navigations (like clicking on a link to go to another site), but not in API requests or images loaded from other sites.
- `Strict`: Cookies are sent only on top-level navigations from the same site that set the cookie, enhancing privacy but potentially disrupting user sessions.
- `None`: Cookies will be sent with both same-site and cross-site requests.

#### 4.12.2 Usage

What you should do with the client is:

- `Login`: Send credentials to `/api/auth/login`. Store the returned access token in memory for subsequent requests.
- `Accessing Protected Routes`: Include the access token in the Authorization header.
- `Token Renewal`: On access token expiry, the front end should automatically call `/api/auth/refresh` for a new token.
- `Login Again`: If refresh token is expired, credentials should be sent to `/api/auth/login` again, storing the new access token in memory.
- `Logout`: Call `/api/auth/logout` to end the session securely.

### 4.13 Running

If you are using docker compose, just running the following command should ensure everything is working:

```sh
make start
```

If you are doing it from scratch, ensure your postgres and your redis are running, then
while in the `root` folder, run to start the application with uvicorn server:

```sh
poetry run uvicorn src.app.main:app --reload
```

And for the worker:

```sh
poetry run arq src.app.core.worker.settings.WorkerSettings
```

### 4.14 Create Application

If you want to stop tables from being created every time you run the api, you should disable this here:

```python
# app/main.py

from app.api.v1 import router as api_v1_router
from app.core.config import settings
from app.create_fastapi_app import create_app

# create_tables_on_start defaults to True
main_app = create_app()
main_app.include_router(
    api_v1_router,
    prefix=settings.api.prefix,
)
```

This `create_app` function is defined in `app/create_fastapi_app.py`, and it's a flexible way to configure the behavior of your application.

A few examples:

- Deactivate or password protect /docs
- Create tables on start
- Add Startup and Shutdown event handlers for cache, queue and rate limit

### 4.15 Logging

If you want to save the all logs in one file, you import logging from `app/core/logger.py`. Default log file is `app/logs/app.log`.

```python
from app.core.logger import logging

logger = logging.getLogger(__name__)
# Пример логирования
logger.debug("Это отладочное сообщение.")
logger.info("Это информационное сообщение.")
logger.warning("Это предупреждение.")
logger.error("Это сообщение об ошибке.")
logger.critical("Это критическое сообщение.")

```

### 4.16 Redis, Queue, Rate Limiter

If you want to use separated redis server for each service (like `Redis`, `Queue`, `Rate Limiter`), head to the `src/app/create_fastapi_app.py` file and uncomment the corresponding functions.

> Do not forget to set the correct settings in `.env` file.

```python
# -------------- cache --------------
async def create_redis_cache_pool() -> None:
    cache.pool = ConnectionPool.from_url(settings.redis_cache.REDIS_CACHE_URL)
    cache.client = Redis(connection_pool=cache.pool)


async def close_redis_cache_pool() -> None:
    await cache.client.aclose()


# -------------- queue --------------
async def create_redis_queue_pool() -> None:
    queue.pool = await create_pool(
        RedisSettings(
            host=settings.redis_queue.REDIS_QUEUE_HOST,
            port=settings.redis_queue.REDIS_QUEUE_PORT,
        )
    )


async def close_redis_queue_pool() -> None:
    await queue.pool.aclose()


# -------------- rate limit --------------
async def create_redis_rate_limit_pool() -> None:
    rate_limit.pool = ConnectionPool.from_url(
        settings.redis_rate_limiter.REDIS_RATE_LIMIT_URL
    )
    rate_limit.client = Redis.from_pool(rate_limit.pool)


async def close_redis_rate_limit_pool() -> None:
    await rate_limit.client.aclose()

```

## 5. Running in Production

### 5.1 Uvicorn Workers with Gunicorn

In production you may want to run using gunicorn to manage uvicorn workers:

change workers number in `.env` file:

```
GUNICORN_WORKERS=1 #number of cores
```

Then run:

```sh
python src/app/run.py
```

Here it's running with 1 worker, but you should test it depending on how many cores your machine has.

> Do not forget to set the `ENVIRONMENT` in `.env` to `production` unless you want the API docs to be public.

### 5.2 Running with NGINX

Soon

## 6. Testing

Soon

### 6.1  Docker Compose

Soon

## 7. References

This project was inspired by a few projects, it's based on them with things changed to the way I like (and pydantic, sqlalchemy updated)

- [Full Stack FastAPI and PostgreSQL](https://github.com/tiangolo/full-stack-fastapi-postgresql) by @tiangolo himself
- [FastAPI Microservices](https://github.com/Kludex/fastapi-microservices) by @kludex which heavily inspired this boilerplate
- [Async Web API with FastAPI + SQLAlchemy 2.0](https://github.com/rhoboro/async-fastapi-sqlalchemy) for sqlalchemy 2.0 ORM examples
- [FastaAPI Rocket Boilerplate](https://github.com/asacristani/fastapi-rocket-boilerplate/tree/main) for docker compose
- [Fullstack FastAPI template](https://github.com/fastapi/full-stack-fastapi-template) by @tiangolo

## 8. Resources

- [.gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore):

- [FastAPI events](https://fastapi.tiangolo.com/advanced/events/)

- [FastAPI lifespan events](https://fastapi.tiangolo.com/advanced/events/#lifespan-function)

- [SQLAlchemy create engine](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)

- [Python typing](https://docs.python.org/3/library/typing.html)

- [pydantic settings dotenv](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support)

- [pydantic settings env variables](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#parsing-environment-variable-values)

- [case converter](https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/ri_sdk_codegen/utils/case_converter.py)

- [SQLAlchemy constraint naming conventions](https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions)

- [Alembic cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html)

- [Alembic naming conventions](https://alembic.sqlalchemy.org/en/latest/naming.html#integration-of-naming-conventions-into-operations-autogenerate)

- [Alembic + asyncio recipe](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic)

- [orjson](https://github.com/ijl/orjson)

- [FastAPI ORJSONResponse](https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse)

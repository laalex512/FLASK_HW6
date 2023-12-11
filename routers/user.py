from sqlalchemy import select
from fastapi import APIRouter
from db import database, users
from models.user import UserIn


router = APIRouter()
ADMIN_PASS = '1'


@router.get('/fake_users/{count}')
async def create_users(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(
            firstname=f'Firstname{i}',
            lastname=f'Lastname{i}',
            email=f'mail{i}@gmail.com',
            password='123456'
        )
        await database.execute(query)
    return {"message": f"{count} fake users added"}


@router.get('/users/')
async def get_users():
    query = select(
        users.c.id,
        users.c.firstname,
        users.c.lastname,
        users.c.email
    )
    # result = []
    # users_dict = dict(database.fetch_all(query))
    # for user in users_dict:
    #     result.append(user[id])
    # print(result)
    return await database.fetch_all(query)


@router.get('/users/{user_id}')
async def get_user(user_id: int):
    query = select(
        users.c.id,
        users.c.firstname,
        users.c.lastname,
        users.c.email
    ).where(users.c.id == user_id)
    return await database.fetch_all(query)


@router.post('/users/')
async def post_user(user: UserIn):
    query = users.insert().values(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=user.password
    )
    await database.execute(query)
    return f'User {user} successfully added'


@router.put("/users/{user_id}")
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id ==
                                 user_id).values(**new_user.dict())
    await database.execute(query)
    return f'User {new_user} successfully updated'


@router.delete("/users/")
async def delete_all(admin_pass: str):
    if ADMIN_PASS == admin_pass:
        query = users.delete()
        await database.execute(query)
        return {"message": "All users deleted"}
    return 'Invalid admin password'


@router.delete("/users/{id}")
async def delete_user(admin_pass: str, user_id: int):
    if ADMIN_PASS == admin_pass:
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)
        return {"message": f"User {user_id} deleted"}
    return 'Invalid admin password'

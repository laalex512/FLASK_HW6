from sqlalchemy import select
from fastapi import APIRouter
from db import database, orders, users, products
from models.order import OrderIn
import random
from datetime import datetime, timedelta


router = APIRouter()
ADMIN_PASS = '1'


async def create_rnd_order():
    query = users.select().with_only_columns(users.c.id)
    users_id = await database.fetch_all(query)
    user_id = random.choice([user[0] for user in users_id])

    query = products.select().with_only_columns(products.c.id)
    products_id = await database.fetch_all(query)
    product_id = random.choice([product[0] for product in products_id])

    cur_date = datetime.now()
    rnd_date = cur_date - timedelta(days=random.randint(0, 365))
    rnd_date = rnd_date.date()

    rnd_bool = random.choice([True, False])

    return OrderIn(
        user_id=user_id,
        product_id=product_id,
        order_date=rnd_date,
        status=rnd_bool
    )


@router.get('/fake_orders/{count}')
async def create_orders(count: int):
    for i in range(1, count + 1):
        new_order = await create_rnd_order()
        query = orders.insert().values(**new_order.dict())
        await database.execute(query)
    return {"message": f"{count} fake orders added"}


@router.get('/orders/')
async def get_orders():
    query = select(
        orders.c.id,
        orders.c.order_date,
        users.c.firstname,
        users.c.lastname,
        products.c.title,
        orders.c.status
    ).join(users).join(products)
    return await database.fetch_all(query)


@router.get('/orders/{order_id}')
async def get_order(order_id: int):
    query = select(
        orders.c.id,
        orders.c.order_date,
        users.c.firstname,
        users.c.lastname,
        products.c.title,
        orders.c.status
    ).join(users).join(products).where(orders.c.id == order_id)
    return await database.fetch_all(query)


@router.post('/orders/')
async def post_order(order: OrderIn):
    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        order_date=order.order_date,
        status=order.status
    )
    await database.execute(query)
    return f'order {order} successfully added'


@router.put("/orders/{order_id}")
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id ==
                                  order_id).values(**new_order.dict())
    await database.execute(query)
    return f'order {new_order} successfully updated'


@router.delete("/orders/")
async def delete_all(admin_pass: str):
    if ADMIN_PASS == admin_pass:
        query = orders.delete()
        await database.execute(query)
        return {"message": "All orders deleted"}
    return 'Invalid admin password'


@router.delete("/orders/{id}")
async def delete_order(admin_pass: str, order_id: int):
    if ADMIN_PASS == admin_pass:
        query = orders.delete().where(orders.c.id == order_id)
        await database.execute(query)
        return {"message": f"order {order_id} deleted"}
    return 'Invalid admin password'

from sqlalchemy import select
from fastapi import APIRouter
from db import database, products
from models.product import ProductIn
import random


router = APIRouter()
ADMIN_PASS = '1'




@router.get('/fake_products/{count}')
async def create_products(count: int):
    for i in range(1, count + 1):
        query = products.insert().values(
            title=f'product{i}',
            description=f'Some description',
            price=round(random.uniform(0.01, 10000), 2)
        )
        await database.execute(query)
    return {"message": f"{count} fake products added"}


@router.get('/products/')
async def get_products():
    query = products.select()
    return await database.fetch_all(query)


@router.get('/products/{product_id}')
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_all(query)


@router.post('/products/')
async def post_product(product: ProductIn):
    query = products.insert().values(
        title=product.title,
        description=product.description,
        price=product.price,
    )
    await database.execute(query)
    return f'product {product} successfully added'


@router.put("/products/{product_id}")
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id ==
                                    product_id).values(**new_product.dict())
    await database.execute(query)
    return f'product {new_product} successfully updated'


@router.delete("/products/")
async def delete_all(admin_pass: str):
    if ADMIN_PASS == admin_pass:
        query = products.delete()
        await database.execute(query)
        return {"message": "All products deleted"}
    return 'Invalid admin password'


@router.delete("/products/{id}")
async def delete_product(admin_pass: str, product_id: int):
    if ADMIN_PASS == admin_pass:
        query = products.delete().where(products.c.id == product_id)
        await database.execute(query)
        return {"message": f"product {product_id} deleted"}
    return 'Invalid admin password'

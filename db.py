import databases
import sqlalchemy as sa
from settings import settings


DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)

metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("firstname", sa.String(32)),
    sa.Column("lastname", sa.String(32)),
    sa.Column("email", sa.String(128)),
    sa.Column("password", sa.String(50)),
)

products = sa.Table(
    'products',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(72)),
    sa.Column('description', sa.String),
    sa.Column('price', sa.Float),
)

orders = sa.Table(
    'orders',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
    sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
    sa.Column('order_date', sa.Date),
    sa.Column('status', sa.Boolean),
)


engine = sa.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

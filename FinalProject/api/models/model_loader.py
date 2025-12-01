from . import orders, order_details, customers, reviews, resource_management, menu, payments, promotions

from ..dependencies.database import engine


def index():
    customers.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    resource_management.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    menu.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
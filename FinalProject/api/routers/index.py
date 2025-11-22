from . import orders, order_details, reviews, analytics, payments, promotions, resource_management, menu


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(reviews.router)
    app.include_router(analytics.router)
    app.include_router(payments.router)
    app.include_router(promotions.router)
    app.include_router(resource_management.router)
    app.include_router(menu.router)
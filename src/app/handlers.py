from sqlalchemy import select

from src.app.models import confirm_order, courier, order


async def select_confirm_order_info_from_confirm_order(courier_id, session):
    stmt = select(confirm_order.c.Courier_id,
                  confirm_order.c.Order_id,
                  confirm_order.c.Time,
                  confirm_order.c.Status) \
        .select_from(confirm_order).where(confirm_order.c.Courier_id == int(courier_id))
    result = await session.execute(stmt)
    return result


async def select_courier_info_from_courier(current_courier_id, session):
    stmt = select(courier.c.Name, courier.c.Courier_type) \
        .select_from(courier). \
        where(courier.c.id == int(current_courier_id))
    result = await session.execute(stmt)
    return result


async def select_cost_from_order(current_order_id, session):
    stmt = select(order.c.Cost).select_from(order).where(order.c.id == int(current_order_id))
    result = await session.execute(stmt)
    return result

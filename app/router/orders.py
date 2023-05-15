from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

from app.models import courier, order
from app.schemas.couriers import *
from app.schemas.orders import *
router = APIRouter()


@router.post(
    "/orders",
    status_code=status.HTTP_200_OK,
    response_model=List
)
async def add_orders_info(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход список с данными о заказах в формате json.
    У заказа есть характеристики — вес, район, время доставки и цена.
    """
    try:
        response = list()
        for ordr in new_order:
            for elem in list(ordr)[1]:
                stmt = insert(order).values(**elem.dict())
                await session.execute(stmt)
                await session.commit()
                stmt = select(
                    order.c.cost,
                    order.c.delivery_hours,
                    order.c.order_id,
                    order.c.regions,
                    order.c.weight,
                    order.c.completed_time
                )\
                    .select_from(order)\
                    .order_by(order.c.order_id.desc())\
                    .limit(1)
                result = await session.execute(stmt)
                response.extend(result.mappings().all())
        return response
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK,
)
async def get_single_order_info(order_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о заказе по его идентификатору, а также дополнительную информацию: вес заказа, район доставки,
    промежутки времени, в которые удобно принять заказ.
    """
    try:
        stmt = select(
            order.c.cost,
            order.c.delivery_hours,
            order.c.order_id,
            order.c.regions,
            order.c.weight,
            order.c.completed_time
        ) \
            .select_from(order)\
            .where(order.c.order_id == order_id)
        result = await session.execute(stmt)
        return result.mappings().all()[0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/orders",
    status_code=status.HTTP_200_OK
)
async def get_all_orders_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о всех заказах, а также их дополнительную информацию: вес заказа, район доставки, промежутки времени, в которые удобно принять заказ.
    Имеет поля offset и limit
    """
    try:
        stmt = select(order).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return result.mappings().all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/orders/complete",
    status_code=status.HTTP_200_OK
)
async def add_confirm_order(new_confirm_order: RequestConfirmOrder, session: AsyncSession = Depends(get_async_session)):
    try:
        for elem in new_confirm_order.complete_info:
            dtm = elem.complete_time
            courier_id = elem.courier_id
            order_id = elem.order_id
            stmt = select(order.c.order_id, order.c.completed_time, order.c.courier_delivers_id).\
                select_from(order).\
                where(order.c.order_id == order_id)
            result = await session.execute(stmt)
            lst = result.mappings().all()[0]
            if lst["completed_time"] is None and lst["courier_delivers_id"] == courier_id:
                stmt = update(order).where(order.c.order_id == order_id).values(completed_time=dtm)
                await session.execute(stmt)
                await session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

from pydantic.types import List
from fastapi import APIRouter, Request, Depends
from sqlalchemy import select, insert
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.app.models import courier, order
from src.app.schemas import CourierCreate, Courier, OrderCreate, Order

router = APIRouter()


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def add_couriers_info(new_courier: CourierCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход список в формате json с данными о курьерах и графиком их работы
    Курьеры различаются по типу: пеший, велокурьер и курьер на автомобиле
    Районы задаются целыми положительными числами
    График работы задается списком строк формата `HH:MM-HH:MM`
    """
    stmt = insert(courier).values(**new_courier.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get(
    "/couriers/{courier_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[Courier]
)
async def get_single_courier_info(courier_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о курьере
    """
    stmt = select(courier).where(courier.c.id == courier_id)
    result = await session.execute(stmt)
    return result.all()


@router.get(
    "/couriers",
    status_code=status.HTTP_200_OK,
    response_model=List[Courier]
)
async def get_all_couriers_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход поле offset и limit
    Возвращает информацию о всех курьерах
    """
    stmt = select(courier).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.all()


@router.post(
    "/orders",
    status_code=status.HTTP_200_OK
)
async def add_orders_info(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход список с данными о заказах в формате json.
    У заказа есть характеристики — вес, район, время доставки и цена.
    """
    stmt = insert(order).values(**new_order.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[Order]
)
async def get_single_order_info(order_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о заказе по его идентификатору, а также дополнительную информацию: вес заказа, район доставки,
    промежутки времени, в которые удобно принять заказ.
    """
    stmt = select(order).where(order.c.id == order_id)
    result = await session.execute(stmt)
    return result.all()


@router.get(
    "/orders",
    status_code=status.HTTP_200_OK,
    response_model=List[Order]
)
async def get_all_orders_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о всех заказах, а также их дополнительную информацию: вес заказа, район доставки, промежутки времени, в которые удобно принять заказ.
    Имеет поля offset и limit
    """
    stmt = select(order).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.all()


@router.post(
    "/orders/complete",
    status_code=status.HTTP_200_OK
)
async def confirm_order():
    """
    Принимает массив объектов, состоящий из трех полей: id курьера, id заказа и время выполнения заказа, после отмечает, что заказ выполнен.
    """
    pass
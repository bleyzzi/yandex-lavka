from pydantic.types import List
from fastapi import APIRouter, Request, Depends
from sqlalchemy import select, insert
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.app.models import courier
from src.app.schemas import CourierCreate, Courier

router = APIRouter()


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def add_couriers_info(new_courier: CourierCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Обработчик принимает на вход список в формате json с данными о курьерах и графиком их работы.
    Курьеры работают только в заранее определенных районах, а также различаются по типу: пеший, велокурьер и
    курьер на автомобиле. От типа зависит объем заказов, которые перевозит курьер.
    Районы задаются целыми положительными числами. График работы задается списком строк формата `HH:MM-HH:MM`.
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
async def get_single_courier_info(id_user: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о курьере
    """
    stmt = select(courier).where(courier.c.id == id_user)
    result = await session.execute(stmt)
    return result.all()


@router.get(
    "/couriers",
    status_code = status.HTTP_200_OK,
    response_model=List[Courier]
)
async def get_all_couriers_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о всех курьерах
    Имеет поля offset и limit
    """
    query = select(courier).limit(limit).offset(offset)
    result = await session.execute(query)
    return result.all()


@router.post(
    "/orders",
    status_code = status.HTTP_200_OK
)
async def add_orders_info():
    """
    Принимает на вход список с данными о заказах в формате json. У заказа отображаются характеристики — вес, район,
    время доставки и цена.
    """
    pass


@router.get(
    "/orders/{order_id}",
    status_code = status.HTTP_200_OK
)
async def get_single_order_info():
    """
    Возвращает информацию о заказе по его идентификатору, а также дополнительную информацию: вес заказа, район доставки,
    промежутки времени, в которые удобно принять заказ.
    """
    pass


@router.get(
    "/orders",
    status_code = status.HTTP_200_OK
)
async def get_all_orders_info(offset: int = 0, limit: int = 0):
    """
    Возвращает информацию о всех заказах, а также их дополнительную информацию: вес заказа, район доставки, промежутки времени, в которые удобно принять заказ.
    Имеет поля offset и limit
    """
    pass


@router.post(
    "/orders/complete",
    status_code = status.HTTP_200_OK
)
async def confirm_order():
    """
    Принимает массив объектов, состоящий из трех полей: id курьера, id заказа и время выполнения заказа, после отмечает, что заказ выполнен.
    """
    pass
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.app.models import courier, order, confirm_order
from src.app.schemas import CourierCreate, OrderCreate, ResponseCourier, ResponseOrder, RequestConfirmOrderCreate, \
    ResponseConfirmOrder, ResponseRatingSalary, RatingSalary, RequestRatingSalary
from sqlalchemy.exc import DatabaseError, IntegrityError
from datetime import datetime

router = APIRouter()


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCourier
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
    ret = ResponseCourier(status=status.HTTP_200_OK, data=None, details=None)
    return ret


@router.get(
    "/couriers/{courier_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCourier
)
async def get_single_courier_info(courier_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о курьере
    """
    stmt = select(courier).where(courier.c.id == courier_id)
    result = await session.execute(stmt)
    ret = ResponseCourier(status=status.HTTP_200_OK, data=result.all(), details=None)
    return ret


@router.get(
    "/couriers",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCourier
)
async def get_all_couriers_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход поле offset и limit
    Возвращает информацию о всех курьерах
    """
    stmt = select(courier).limit(limit).offset(offset)
    result = await session.execute(stmt)
    ret = ResponseCourier(status=status.HTTP_200_OK, data=result.all(), details=None)
    return ret


@router.post(
    "/orders",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCourier
)
async def add_orders_info(new_order: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход список с данными о заказах в формате json.
    У заказа есть характеристики — вес, район, время доставки и цена.
    """
    stmt = insert(order).values(**new_order.dict())
    await session.execute(stmt)
    await session.commit()
    ret = ResponseOrder(status=status.HTTP_200_OK, data=None, details=None)
    return ret


@router.get(
    "/orders/{order_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseOrder
)
async def get_single_order_info(order_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о заказе по его идентификатору, а также дополнительную информацию: вес заказа, район доставки,
    промежутки времени, в которые удобно принять заказ.
    """
    stmt = select(order).where(order.c.id == order_id)
    result = await session.execute(stmt)
    ret = ResponseOrder(status=status.HTTP_200_OK, data=result.all(), details=None)
    return ret


@router.get(
    "/orders",
    status_code=status.HTTP_200_OK,
    response_model=ResponseOrder
)
async def get_all_orders_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о всех заказах, а также их дополнительную информацию: вес заказа, район доставки, промежутки времени, в которые удобно принять заказ.
    Имеет поля offset и limit
    """
    stmt = select(order).limit(limit).offset(offset)
    result = await session.execute(stmt)
    ret = ResponseOrder(status=status.HTTP_200_OK, data=result.all(), details=None)
    return ret


@router.post(
    "/orders/complete",
    status_code=status.HTTP_200_OK,
    response_model=ResponseConfirmOrder
)
async def add_confirm_order(new_order: RequestConfirmOrderCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(confirm_order).values(**new_order.dict())
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400)
    finally:
        await session.close()
    ret = ResponseConfirmOrder(status=status.HTTP_200_OK, data=None, details=None)
    return ret


@router.get(
    "/couriers/meta-info/{courier_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseRatingSalary
)
async def get_courier_rating(start_date: str, end_date: str, courier_id: int,
                             session: AsyncSession = Depends(get_async_session)):
    # try:
    # print(datetime.strptime(start_date, "%d/%m/%y %H:%M"))
    # print(datetime.strptime(end_date, "%d/%m/%y %H:%M"))
    # print(datetime.strptime(end_date, "%d/%m/%y %H:%M") - datetime.strptime(start_date, "%d/%m/%y %H:%M"))
    coefficient = {1: 2,
                   2: 3,
                   3: 4}
    stmt = select(confirm_order.c.Courier_id,
                  confirm_order.c.Order_id,
                  confirm_order.c.Time,
                  confirm_order.c.Status) \
        .select_from(confirm_order)
    result = await session.execute(stmt)
    lst = list(result.all()[0])
    print(lst)
    stmt = select(courier.c.Courier_type) \
        .select_from(courier). \
        where(courier.c.id == lst[0])
    result = await session.execute(stmt)
    courier_type = list(result.all()[0])
    print(courier_type)
    rating = None
    salary = None
    ret = ResponseRatingSalary(status=status.HTTP_200_OK, data=RatingSalary(rating=rating, salary=salary), details=None)
    return ret

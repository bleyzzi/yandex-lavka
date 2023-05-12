from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.handlers import select_courier_info_from_courier, \
    select_confirm_order_info_from_confirm_order, select_cost_from_order
from src.database import get_async_session
from src.app.models import courier, order, confirm_order
from src.app.schemas import CourierCreate, OrderCreate, ResponseCourier, ResponseOrder, RequestConfirmOrderCreate, \
    ResponseConfirmOrder, ResponseRatingSalary, RatingSalary
from sqlalchemy.exc import IntegrityError
from fastapi_limiter.depends import RateLimiter


def get_rate_limiter(requests: int, seconds: int):
    return RateLimiter(times=requests, seconds=seconds)


router = APIRouter()
rate_limiter = get_rate_limiter(requests=10, seconds=60)


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCourier,
    dependencies=[Depends(rate_limiter)]
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
async def getOrders(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о всех заказах, а также их дополнительную информацию: вес заказа, район доставки, промежутки времени, в которые удобно принять заказ.
    Имеет поля offset и limit
    """
    try:
        stmt = select(order).limit(limit).offset(offset)
        result = await session.execute(stmt)
        ret = ResponseOrder(status=status.HTTP_200_OK, data=result.all(), details=None)
        return ret
    except IntegrityError:
        return HTTPException(status_code=400)


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
    coefficient_salary = {1: 2,
                          2: 3,
                          3: 4}
    coefficient_rating = {1: 3,
                          2: 2,
                          3: 1}
    rating = None
    salary = 0
    result = await select_confirm_order_info_from_confirm_order(courier_id, session)
    for elem_list in result.all():
        order_info_list = list(elem_list)
        if order_info_list[3] == 'success':
            current_courier_id = int(order_info_list[0])
            result = await select_courier_info_from_courier(current_courier_id, session)
            courier_info = list(result.all()[0])
            courier_type = courier_info[1]
            current_order_id = int(order_info_list[1])
            result = await select_cost_from_order(current_order_id, session)
            cost = list(result.all()[0])[0]
            salary += coefficient_salary[courier_type] * cost

    ret = ResponseRatingSalary(status=status.HTTP_200_OK, data=RatingSalary(rating=rating, salary=salary), details=None)
    return ret

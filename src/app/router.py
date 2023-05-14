from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

# from src.app.handlers import select_courier_info_from_courier, \
#    select_confirm_order_info_from_confirm_order, select_cost_from_order
from src.database import get_async_session
from src.app.models import courier, order
from src.app.schemas import CourierCreate, OrderCreate, ResponseCourier, ResponseOrder, RequestConfirmOrder, \
    ResponseCourierWithId, ResponseCourierCreate
from sqlalchemy.exc import IntegrityError, ProgrammingError, InternalError, InvalidRequestError

router = APIRouter()


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK,
    response_model=ResponseCourierCreate
)
async def add_couriers_info(new_courier: CourierCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход список в формате json с данными о курьерах и графиком их работы
    Курьеры различаются по типу: пеший, велокурьер и курьер на автомобиле
    Районы задаются целыми положительными числами
    График работы задается списком строк формата `HH:MM-HH:MM`
    """
    try:
        response = ResponseCourierCreate(couriers=[])
        for cour in new_courier:
            for elem in list(cour)[1]:
                print(elem)
                stmt = insert(courier).values(**elem.dict())
                await session.execute(stmt)
                await session.commit()
                stmt = select(courier).order_by(courier.c.courier_id.desc()).limit(1)
                result = await session.execute(stmt)
                dct = result.mappings().all()[0]
                courier_id = dct["courier_id"]
                courier_type = dct["courier_type"]
                regions = dct["regions"]
                working_hours = dct["working_hours"]
                response.couriers.append(ResponseCourierWithId(courier_id=courier_id, courier_type=courier_type,
                                                               regions=regions, working_hours=working_hours))
        return response
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/couriers/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def get_single_courier_info(courier_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает информацию о курьере
    """
    try:
        stmt = select(courier).where(courier.c.courier_id == courier_id)
        result = await session.execute(stmt)
        return result.mappings().all()[0]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


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
    try:
        stmt = select(courier).limit(limit).offset(offset)
        result = await session.execute(stmt)
        return ResponseCourier(couriers=result.mappings().all(), limit=limit, offset=offset)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


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
                stmt = select(order).order_by(order.c.order_id.desc()).limit(1)
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
        stmt = select(order).where(order.c.order_id == order_id)
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
            stmt = select(order.c.order_id, order.c.completed_time).\
                select_from(order).\
                where(order.c.order_id == order_id)
            result = await session.execute(stmt)
            if result.mappings().all()[0]["completed_time"] is None:
                stmt = update(order).where(order.c.order_id == order_id).values(completed_time=dtm)
                await session.execute(stmt)
                await session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/couriers/meta-info/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def get_courier_salary_rating(start_date: str, end_date: str,
                                    session: AsyncSession = Depends(get_async_session)):
    coefficient_salary = {1: 2,
                          2: 3,
                          3: 4}
    coefficient_rating = {1: 3,
                          2: 2,
                          3: 1}
    rating = None
    salary = 0
    return None


'''
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
'''
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


@router.get(
    "/couriers/meta-info/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def get_courier_salary_rating(start_date: str, end_date: str, courier_id: int,
                                    session: AsyncSession = Depends(get_async_session)):
    start_date = datetime.strptime(start_date, "%d/%m/%y %H:%M")
    end_date = datetime.strptime(end_date, "%d/%m/%y %H:%M")
    coefficient_salary = {"FOOT": 2,
                          "BIKE": 3,
                          "AUTO": 4}
    coefficient_rating = {"FOOT": 3,
                          "BIKE": 2,
                          "AUTO": 1}
    rating = None
    earnings = 0
    stmt = select(order.c.cost, order.c.completed_time, order.c.courier_delivers_id).\
        select_from(order)\
        .where(order.c.courier_delivers_id == courier_id)
    result = await session.execute(stmt)
    for elem_list in result.all():
        order_info_list = list(elem_list)
        if order_info_list[1] is not None and (start_date <= order_info_list[1] < end_date):
            stmt = select(courier.c.courier_type).\
                select_from(courier).\
                where(courier.c.courier_id == int(order_info_list[2]))
            courier_type = (await session.execute(stmt)).mappings().all()[0]["courier_type"]
            earnings += order_info_list[0] * coefficient_salary[courier_type]
        if order_info_list[1] is not None and (start_date <= order_info_list[1] <= end_date):
            pass
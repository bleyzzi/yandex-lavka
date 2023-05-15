from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_async_session

from app.database.models import courier, order
from app.schemas.couriers import *

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
    # try:
    response = ResponseCourierCreate(couriers=[])
    for cour in new_courier:
        for elem in list(cour)[1]:
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
    # except Exception:
    #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


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
    status_code=status.HTTP_200_OK
)
async def get_all_couriers_info(offset: int = 0, limit: int = 1, session: AsyncSession = Depends(get_async_session)):
    """
    Принимает на вход поле offset и limit
    Возвращает информацию о всех курьерах
    """
    try:
        response = ResponseCourier(couriers=[], limit=limit, offset=offset)
        stmt = select(courier).limit(limit).offset(offset)
        result = await session.execute(stmt)
        for elem in result.mappings().all():
            response.couriers.append(elem)
        return response
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    "/couriers/meta-info/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def get_courier_salary_rating(start_date: Annotated[str, Query(description='Дата вида 23-01-20')],
                                    end_date: Annotated[str, Query(description='Дата вида 23-01-20')],
                                    courier_id: int,
                                    session: AsyncSession = Depends(get_async_session)):
    try:
        start_date = datetime.strptime(start_date, "%y-%m-%d")
        end_date = datetime.strptime(end_date, "%y-%m-%d")
        if start_date >= end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="end_date не может быть меньше, чем start_date")
        coefficient_salary = {"FOOT": 2,
                              "BIKE": 3,
                              "AUTO": 4}
        coefficient_rating = {"FOOT": 3,
                              "BIKE": 2,
                              "AUTO": 1}
        rating = None
        earnings = 0
        val_orders = 0
        stmt = select(courier).where(courier.c.courier_id == courier_id)
        iid, courier_type, regions, working_hours = (await session.execute(stmt)).mappings().all()[0].values()
        print(courier_type)
        stmt = select(order.c.cost, order.c.completed_time, order.c.courier_delivers_id). \
            select_from(order) \
            .where(order.c.courier_delivers_id == courier_id)
        result = await session.execute(stmt)
        for elem_list in result.all():
            order_info_list = list(elem_list)
            print(order_info_list)
            if order_info_list[1] is not None and (start_date <= order_info_list[1] < end_date):
                earnings += order_info_list[0] * coefficient_salary[courier_type]
            if order_info_list[1] is not None and (start_date <= order_info_list[1] <= end_date):
                val_orders += 1
                rating = (val_orders // int((end_date - start_date).days) * 24) * coefficient_rating[courier_type]
        return RequestMetaInfo(courier_id=courier_id, courier_type=courier_type, regions=regions,
                               working_hours=working_hours, earnings=earnings, rating=rating)
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Проверьте введенную дату")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

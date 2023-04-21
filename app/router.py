from fastapi import APIRouter, Request
from starlette import status
from app.models import Courier
from typing import List, Dict

router = APIRouter()
lst = List


@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def add_couriers_info(couriers: List[Courier]):
    """
    Обработчик принимает на вход список в формате json с данными о курьерах и графиком их работы.
    Курьеры работают только в заранее определенных районах, а также различаются по типу: пеший, велокурьер и
    курьер на автомобиле. От типа зависит объем заказов, которые перевозит курьер.
    Районы задаются целыми положительными числами. График работы задается списком строк формата `HH:MM-HH:MM`.
    """
    print(couriers)
    return {"message": "Couriers created successfully"}


@router.get(
    "/couriers/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def get_single_courier_info():
    """
    Возвращает информацию о курьере
    """
    return lst


@router.get(
    "/couriers",
    status_code = status.HTTP_200_OK
)
async def get_all_couriers_info(offset: int = 0, limit: int = 1):
    """
    Возвращает информацию о всех курьерах
    Имеет поля offset и limit
    """
    return lst


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
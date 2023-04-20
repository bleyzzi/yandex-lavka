from fastapi import APIRouter, Request
from starlette import status

router = APIRouter()
@router.post(
    "/couriers",
    status_code=status.HTTP_200_OK
)
async def couriers():
    """
    Обработчик принимает на вход список в формате json с данными о курьерах и графиком их работы.
    Курьеры работают только в заранее определенных районах, а также различаются по типу: пеший, велокурьер и
    курьер на автомобиле. От типа зависит объем заказов, которые перевозит курьер.
    Районы задаются целыми положительными числами. График работы задается списком строк формата `HH:MM-HH:MM`.
    """
    pass

@router.get(
    "/couriers/{courier_id}",
    status_code=status.HTTP_200_OK
)
async def courier_info():
    """
    Возвращает информацию о курьере
    """
    pass

@router.get(
    "/couriers",
    status_code = status.HTTP_200_OK
)
async def couriers_info(offset: int = 0, limit: int = 1):
    """
    Возвращает информацию о всех курьерах
    Имеет поля offset и limit
    """
    pass

@router.post(
    "/orders",
    status_code = status.HTTP_200_OK
)
async def orders_get():
    """
    Принимает на вход список с данными о заказах в формате json. У заказа отображаются характеристики — вес, район,
    время доставки и цена.
    """
    pass
import pytest
import allure
from methods.order_methods import OrderMethods
from methods.courier_methods import CourierMethods
from data import COURIER_PARAMS


@pytest.fixture()
@allure.step("Инициализация методов для работы с заказами")
def order_methods():
    return OrderMethods()


@pytest.fixture()
@allure.step("Инициализация методов для работы с курьерами")
def courier_methods():
    return CourierMethods()


@pytest.fixture()
@allure.step("Создание нового курьера перед тестом и удаление после")
def courier(courier_methods):
    courier_data = COURIER_PARAMS[0]
    response = courier_methods.create_courier(courier_data)
    response_data = response.json()
    courier_id = response_data.get('id') if response.status_code == 201 else None

    yield courier_id

    if courier_id:
        courier_methods.delete_courier(courier_id)

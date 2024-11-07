import allure
import pytest
from data import COLORS, generate_order_data


@pytest.mark.parametrize("color", [None, COLORS[0], COLORS[1], [COLORS[0], COLORS[1]]])
@allure.step("Тест создания заказа с цветом: {color}")
def test_create_order(order_methods, color, courier):
    metro_station = 1
    order_data = generate_order_data(metro_station, color)

    status_code, response = order_methods.create_order(metro_station=metro_station, color=color)

    assert status_code == 201
    assert "track" in response
    assert isinstance(response["track"], int)

    if color is not None:
        if isinstance(color, list):
            assert sorted(order_data.get("color", [])) == sorted(color)
        else:
            assert order_data.get("color") == [color]
    else:
        assert "color" not in order_data


@allure.feature("Получение списка заказов")
@allure.story("Получение списка всех заказов без указания courierId")
def test_get_orders_without_courier_id(order_methods):
    status_code, response = order_methods.get_orders()
    assert status_code == 200
    assert "availableStations" in response
    assert isinstance(response["availableStations"], list)

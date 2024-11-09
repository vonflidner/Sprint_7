import allure
from helper import COLORS, generate_order_data


@allure.suite("Тесты создания заказа")
class TestCreateOrder:

    @allure.title("Создание заказа без указания цвета")
    def test_create_order_without_color(self, order_methods, courier):
        metro_station = 1
        color = None
        order_data = generate_order_data(metro_station, color)

        status_code, response = order_methods.create_order(metro_station=metro_station, color=color)

        assert status_code == 201
        assert "track" in response
        assert isinstance(response["track"], int)
        assert "color" not in order_data

    @allure.title("Создание заказа с цветом: {COLORS[0]}")
    def test_create_order_with_color_one(self, order_methods, courier):
        metro_station = 1
        color = COLORS[0]
        order_data = generate_order_data(metro_station, color)

        status_code, response = order_methods.create_order(metro_station=metro_station, color=color)

        assert status_code == 201
        assert "track" in response
        assert isinstance(response["track"], int)
        assert order_data.get("color") == [color]

    @allure.title("Создание заказа с цветом: {COLORS[1]}")
    def test_create_order_with_color_two(self, order_methods, courier):
        metro_station = 1
        color = COLORS[1]
        order_data = generate_order_data(metro_station, color)

        status_code, response = order_methods.create_order(metro_station=metro_station, color=color)

        assert status_code == 201
        assert "track" in response
        assert isinstance(response["track"], int)
        assert order_data.get("color") == [color]

    @allure.title("Создание заказа с двумя цветами")
    def test_create_order_with_both_colors(self, order_methods, courier):
        metro_station = 1
        color = [COLORS[0], COLORS[1]]
        order_data = generate_order_data(metro_station, color)

        status_code, response = order_methods.create_order(metro_station=metro_station, color=color)

        assert status_code == 201
        assert "track" in response
        assert isinstance(response["track"], int)
        assert sorted(order_data.get("color", [])) == sorted(color)

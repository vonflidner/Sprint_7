import requests
from data import BASE_URL, ORDERS_URL, generate_order_data, STATIONS_SEARCH_URL
import allure


class OrderMethods:

    @allure.step("Создание заказа")
    def create_order(self, metro_station=1, color=None):
        order_data = generate_order_data(metro_station, color)
        response = requests.post(f'{BASE_URL}{ORDERS_URL}', json=order_data)
        return response.status_code, response.json()

    @allure.step("Получение списка заказов")
    def get_orders(self, courier_id=None, metro_station=None, limit=None):
        params = {}
        if courier_id:
            params['courierId'] = courier_id
        if metro_station:
            params['metroStation'] = metro_station
        if limit:
            params['limit'] = limit

        response = requests.get(f'{BASE_URL}{ORDERS_URL}', params=params)
        return response.status_code, response.json()

    @allure.step("Поиск станции метро по названию: {station_name}")
    def get_station_number(self, station_name):
        response = requests.get(f"{BASE_URL}{STATIONS_SEARCH_URL}", params={"s": station_name})

        if response.status_code == 200:
            stations = response.json()
            return stations[0]["number"] if stations else 1
        else:
            allure.attach(
                f"Ошибка при поиске станции метро: {response.text}",
                name="Ошибка",
                attachment_type=allure.attachment_type.TEXT
            )
            return 1

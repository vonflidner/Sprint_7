from data import BASE_URL, COURIERS_URL
import requests
import random
import string
import allure


class CourierMethods:

    @allure.step("Создание нового курьера")
    def create_courier(self, courier_data):
        response = requests.post(f'{BASE_URL}{COURIERS_URL}', json=courier_data)
        if response.status_code == 409:
            print(f"Курьер с логином '{courier_data['login']}' уже существует.")
        return response

    @allure.step("Авторизация курьера")
    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{BASE_URL}{COURIERS_URL}login', json=payload)
        return response

    @allure.step("Удаление курьера по ID")
    def delete_courier(self, courier_id):
        response = requests.delete(f'{BASE_URL}{COURIERS_URL}{courier_id}')
        if response.status_code == 204:
            print(f"Курьер с ID {courier_id} успешно удален.")
        else:
            print(f"Ошибка при удалении курьера с ID {courier_id}: {response.status_code}")
        return response

    @allure.step("Получение списка всех курьеров")
    def get_all_couriers(self):
        response = requests.get(f'{BASE_URL}{COURIERS_URL}')
        return response.json() if response.status_code == 200 else None

    @allure.step("Проверка существования курьера с логином: {login}")
    def courier_exists(self, login):
        couriers = self.get_all_couriers()
        if couriers:
            for courier in couriers:
                if courier['login'] == login:
                    return True
        return False


@allure.step("Регистрация нового курьера и возвращение логина и пароля")
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}{COURIERS_URL}', json=payload)

    if response.status_code == 201:
        login_pass.extend([login, password, first_name])
    return login_pass

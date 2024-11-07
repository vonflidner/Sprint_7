import requests
from data import BASE_URL, COURIERS_URL


class CourierMethods:

    def create_courier(self, courier_data):
        response = requests.post(f'{BASE_URL}{COURIERS_URL}', json=courier_data)
        if response.status_code == 409:
            print(f"Курьер с логином '{courier_data['login']}' уже существует.")
        return response

    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(f'{BASE_URL}{COURIERS_URL}login', json=payload)
        return response

    def delete_courier(self, courier_id):
        response = requests.delete(f'{BASE_URL}{COURIERS_URL}{courier_id}')
        if response.status_code == 204:
            print(f"Курьер с ID {courier_id} успешно удален.")
        else:
            print(f"Ошибка при удалении курьера с ID {courier_id}: {response.status_code}")
        return response

    def get_all_couriers(self):
        response = requests.get(f'{BASE_URL}{COURIERS_URL}')
        return response.json() if response.status_code == 200 else None

    def courier_exists(self, login):
        couriers = self.get_all_couriers()
        if couriers:
            for courier in couriers:
                if courier['login'] == login:
                    return True
        return False

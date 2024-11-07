import pytest
from methods.courier_methods import CourierMethods
from helper import register_new_courier_and_return_login_password
from data import COURIER_PARAMS, COURIER_INVALID_PARAMS
import allure


@allure.suite("Тесты создания курьера")
class TestCreateCourier:

    @pytest.fixture()
    def courier_methods(self):
        return CourierMethods()

    @allure.title("Создание курьера")
    @pytest.mark.parametrize("courier_data", COURIER_PARAMS)
    def test_create_courier(self, courier_data, courier_methods):
        response = courier_methods.create_courier(courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Создание курьера с существующим логином")
    @pytest.mark.parametrize("courier_data", COURIER_PARAMS)
    def test_duplicate_courier(self, courier_data, courier_methods):
        courier_methods.create_courier(courier_data)
        response = courier_methods.create_courier(courier_data)
        assert response.status_code == 409
        assert response.json() == {
            "message": "Этот логин уже используется. Попробуйте другой.",
            "code": 409
        }

    @allure.title("Создание курьера с недостающими полями")
    @pytest.mark.parametrize("courier_data", COURIER_INVALID_PARAMS)
    def test_missing_fields(self, courier_data, courier_methods):
        response = courier_methods.create_courier(courier_data)
        assert response.status_code == 400

    @allure.title("Авторизация курьера")
    def test_authorization(self, courier_methods):
        courier_data = register_new_courier_and_return_login_password()
        assert courier_data, "Не удалось создать курьера"
        login, password, _ = courier_data
        response = courier_methods.login_courier(login, password)
        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title("Ошибки авторизации с неправильным логином/паролем")
    @pytest.mark.parametrize("wrong_login, wrong_password", [
        ("wrong_login", "test_password"),
        ("test_login", "wrong_password"),
    ])
    def test_authentication_errors(self, wrong_login, wrong_password, courier_methods):
        valid_courier_data = register_new_courier_and_return_login_password()
        assert valid_courier_data, "Не удалось создать курьера"
        login, password, _ = valid_courier_data
        response = courier_methods.login_courier(wrong_login, wrong_password)
        assert response.status_code == 404

    @allure.title("Авторизация несуществующего пользователя")
    def test_auth_nonexistent_user(self, courier_methods):
        response = courier_methods.login_courier("nonexistent_login", "nonexistent_password")
        assert response.status_code == 404
        assert response.json() == {"message": "Учетная запись не найдена", "code": 404}

import pytest
from helper import COURIER_PARAMS, COURIER_INVALID_PARAMS
import allure


@allure.suite("Тесты создания курьера")
class TestCreateCourier:

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

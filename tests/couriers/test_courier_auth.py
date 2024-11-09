import allure
import pytest
from methods.courier_methods import register_new_courier_and_return_login_password


@allure.suite("Тесты авторизации курьера")
class TestCourierAuthorization:

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
        response = courier_methods.login_courier(wrong_login, wrong_password)
        assert response.status_code == 404

    @allure.title("Авторизация несуществующего пользователя")
    def test_auth_nonexistent_user(self, courier_methods):
        response = courier_methods.login_courier("nonexistent_login", "nonexistent_password")
        assert response.status_code == 404
        assert response.json() == {"message": "Учетная запись не найдена", "code": 404}

from faker import Faker
import allure

fake = Faker("ru_RU")

COLORS = ['BLACK', 'GREY']


@allure.step("Генерация данных для заказа")
def generate_order_data(metro_station=1, color=None):
    order_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": metro_station,
        "phone": fake.phone_number(),
        "rentTime": fake.random_int(min=1, max=10),
        "deliveryDate": fake.date_this_year().isoformat(),
        "comment": fake.sentence(),
    }

    if color is not None:
        if isinstance(color, list):
            for c in color:
                if c not in COLORS:
                    raise ValueError(f"Invalid color: {c}. Valid options are {COLORS}.")
            order_data["color"] = color
        else:
            if color not in COLORS:
                raise ValueError(f"Invalid color: {color}. Valid options are {COLORS}.")
            order_data["color"] = [color]

    return order_data


@allure.step("Получение данных о курьере")
def get_courier_data():
    return [
        {
            "login": fake.unique.user_name(),
            "password": fake.password(),
            "firstName": fake.first_name()
        },
        {
            "login": fake.unique.user_name(),
            "password": fake.password(),
            "firstName": fake.first_name()
        }
    ]


COURIER_PARAMS = get_courier_data()

COURIER_INVALID_PARAMS = [
    {"firstName": fake.first_name(), "password": fake.password()},
    {"firstName": fake.first_name(), "login": fake.user_name()},
]

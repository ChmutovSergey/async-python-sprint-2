import json
import os

from urllib.request import urlopen

from logger import logger
from utils import ERR_MESSAGE_TEMPLATE, CITIES


class YandexWeatherAPI:
    """
    Base class for requests
    """

    @staticmethod
    def _do_req(url):
        """Base request method"""
        try:
            with urlopen(url) as req:
                resp = req.read().decode("utf-8")
                resp = json.loads(resp)
            if req.status != 200:
                raise Exception(
                    "Error during execute request. {}: {}".format(
                        resp.status, resp.reason
                    )
                )
            return resp
        except Exception as ex:
            logger.error(ex)
            raise Exception(ERR_MESSAGE_TEMPLATE)

    @staticmethod
    def _get_url_by_city_name(city_name: str) -> str:
        try:
            return CITIES[city_name]
        except KeyError:
            raise Exception("Please check that city {} exists".format(city_name))

    def get_forecasting(self, city_name: str):
        """
        :param city_name: key as str
        :return: response data as json
        """
        city_url = self._get_url_by_city_name(city_name)
        return self._do_req(city_url)


def task_for_test_0():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{0}")
    city_name_for_test = "MOSCOW"

    return get_weather(city_name_for_test)


def task_for_test_1():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{1}")
    city_name_for_test = "PARIS"

    return get_weather(city_name_for_test)


def task_for_test_2():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{2}")
    city_name_for_test = "LONDON"

    return get_weather(city_name_for_test)


def task_for_test_3():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{3}")
    city_name_for_test = "BERLIN"

    return get_weather(city_name_for_test)


def task_for_test_4():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{4}")
    city_name_for_test = "BEIJING"

    return get_weather(city_name_for_test)


def task_for_test_5():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{5}")
    city_name_for_test = "BERLIN"

    return get_weather(city_name_for_test)


def task_for_test_6():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{6}")
    city_name_for_test = "KAZAN"

    return get_weather(city_name_for_test)


def task_for_test_7():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{7}")
    city_name_for_test = "LONDON"

    return get_weather(city_name_for_test)


def task_for_test_8():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{8}")
    city_name_for_test = "MOSCOW"

    return get_weather(city_name_for_test)


def task_for_test_9():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info(f"Started task_for_test_{9}")
    city_name_for_test = "PARIS"

    return get_weather(city_name_for_test)


def task_for_test_inner_0():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info("Started task_for_test_inner_0")
    city_name_for_test = "BEIJING"

    yield from read_and_del_file(city_name_for_test)


def task_for_test_inner_1():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info("Started task_for_test_inner_1")
    city_name_for_test = "KAZAN"

    yield from read_and_del_file(city_name_for_test)


def task_for_test_inner_2():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info("Started task_for_test_inner_2")
    city_name_for_test = "SPETERSBURG"

    yield from read_and_del_file(city_name_for_test)


def task_for_test_inner_3():
    """
    Тестовый метод. Используется для интеграционных тестов

    :return:
    """
    logger.info("Started task_for_test_inner_3")
    city_name_for_test = "VOLGOGRAD"

    yield from read_and_del_file(city_name_for_test)


def get_weather(city_name: str):
    """
    Метод создает или удаляет папку если она создана, читает данные из сети и сохраняет в файл

    :param city_name:
    :return:
    """
    if not os.path.exists(city_name):
        os.makedirs(city_name)
    else:
        os.rmdir(city_name)

    ywAPI = YandexWeatherAPI()
    resp = ywAPI.get_forecasting(city_name)
    with open(f"{city_name}.txt", "w") as file:
        file.write(str(resp.get("info")))
    return resp.get("info")


def read_and_del_file(city_name: str):
    """
    Читает данные из файла и возвращает их как результат работы метода
    после чего файл удаляется.

    :param city_name:
    :return:
    """
    with open(f"{city_name}.txt", "r") as file:
        yield file.readlines()
    os.remove(file.name)


worker_tasks = {
    "task_for_test_0": task_for_test_0,
    "task_for_test_1": task_for_test_1,
    "task_for_test_2": task_for_test_2,
    "task_for_test_3": task_for_test_3,
    "task_for_test_4": task_for_test_4,
    "task_for_test_5": task_for_test_5,
    "task_for_test_6": task_for_test_6,
    "task_for_test_7": task_for_test_7,
    "task_for_test_8": task_for_test_8,
    "task_for_test_9": task_for_test_9,
    "task_for_test_inner_0": task_for_test_inner_0,
    "task_for_test_inner_1": task_for_test_inner_1,
    "task_for_test_inner_2": task_for_test_inner_2,
    "task_for_test_inner_3": task_for_test_inner_3,
}

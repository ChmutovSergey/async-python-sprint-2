from scheduler import Scheduler
from tests.conftest import create_tasks


def main():
    """
    Метод для интеграционного тестирования. И демонстрации работы планировщика.

    Создает экземпляр класса Scheduler наполняет его задачами. Штатно останавливает планировщик.
    Создает новый экземпляр класса Scheduler, перезапускает его.


    :return:
    """
    scheduler = Scheduler()
    scheduler_stop(scheduler)

    scheduler = Scheduler()
    scheduler_restart(scheduler)


def scheduler_restart(scheduler: Scheduler):
    """
    Метод эмулирует ситуацию восстановления после штатной остановки

    :param scheduler:
    :return:
    """
    scheduler.restart()


def scheduler_stop(scheduler: Scheduler):
    """
    Метод эмулирует ситуацию штатной остановки

    :param scheduler:
    :return:
    """
    create_tasks(scheduler)
    scheduler.stop()


if __name__ == "__main__":
    main()

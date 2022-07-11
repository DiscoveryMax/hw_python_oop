from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO_MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        '''Возвращает строку сообщения о результатах тренировки'''
        return self.INFO_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65      # Коэфф. длина шага
    M_IN_KM: int = 1000     # Коэфф. в 1 км = 1000 м
    MIN_IN_HOUR: int = 60       # 60 мин = 1 час.

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action: int = action        # Кол-во совершенных действий
        self.duration_hour: float = duration        # Длительность тренировки
        self.weight_kg: float = weight        # Вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Реализуйте get_spent_calories() в {type(self).__name__}().'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_hour,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    SPEED_COEFF_A: int = 18        # Коэфф. скорости
    SPEED_COEFF_B: int = 20        # Коэфф. скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.SPEED_COEFF_A * self.get_mean_speed() - self.SPEED_COEFF_B)
            * self.weight_kg / self.M_IN_KM
            * self.duration_hour * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_COEFF_A: float = 0.035      # Кофф. веса
    WEIGHT_COEFF_B: float = 0.029      # Кофф. веса

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height     # Рост спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.WEIGHT_COEFF_A * self.weight_kg
             + (self.get_mean_speed()**2 // self.height_cm)
             * self.WEIGHT_COEFF_B * self.weight_kg)
            * self.duration_hour * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38      # Коэфф. длина гребка
    SPEED_COEFF: float = 1.1        # Коэфф. скорости
    WEIGHT_COEFF: int = 2        # Коэфф. веса

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_metre: float = length_pool
        self.count_pool: int = count_pool        # Сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость заплыва."""
        return (
            self.length_pool_metre * self.count_pool
            / self.M_IN_KM / self.duration_hour
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEED_COEFF) * self.WEIGHT_COEFF
            * self.weight_kg
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in workout_type_dict:
        raise TypeError('Тренировка не найдена.')

    return workout_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

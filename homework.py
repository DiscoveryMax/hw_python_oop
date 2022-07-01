class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        '''Возвращает строку сообщения о результатах тренировки'''
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65      # Коэфф. длина шага
    M_IN_KM: int = 1000     # Коэфф. в 1 км = 1000 м
    ON_60_MINUTES: int = 60       # 60 мин = 1 час.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action        # Кол-во совершенных действий
        self.duration = duration        # Длительность тренировки
        self.weight = weight        # Вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18        # Коэфф. расчета калорий 1
    coeff_calorie_2: int = 20        # Коэфф. расчета калорий 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * (self.duration * self.ON_60_MINUTES))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035      # Кофф. расчета калорий 1
    coeff_calorie_2: float = 0.029      # Кофф. расчета калорий 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height     # Вес спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_calorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.coeff_calorie_2) * self.duration * self.ON_60_MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38      # Коэфф. длина гребка
    coeff_calorie_1: float = 1.1        # Коэфф. расчета калорий 1
    coeff_calorie_2: int = 2        # Коэфф. расчета калорий 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool      # Длина бассейна в метрах
        self.count_pool = count_pool        # Сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость заплыва."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in workout_type_dict:
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

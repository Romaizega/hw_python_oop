class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float, distance: float,
                 speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает сообщение о тренировке."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOUR_TO_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float, ) -> None:
        super().__init__(action, duration, weight, )
        self.weight = weight

    def get_spent_calories(self) -> float:
        return (
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * self.weight / self.M_IN_KM * (
            self.duration * self.HOUR_TO_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    RATIO_1_OF_WEIGHT: float = 0.035
    RATIO_2_OF_WEIGHT: float = 0.029
    CONVERT_SPEED_INTO_SEC = 0.278
    CONVERT_WEIGHT: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ):
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.height = height

    def get_spent_calories(self) -> float:
        speed_into_ms = self.get_mean_speed() * self.CONVERT_SPEED_INTO_SEC
        height_into_m = self.height / self.CONVERT_WEIGHT
        duration_into_min = self.duration * self.HOUR_TO_MIN
        return (self.RATIO_1_OF_WEIGHT * self.weight
                + (speed_into_ms ** 2 / height_into_m)
                * self.RATIO_2_OF_WEIGHT * self.weight) * duration_into_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    RATIO_SWM_1: float = 1.1
    RATIO_SWM_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool,
                 ):
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed_swm = (self.length_pool
                          * self.count_pool
                          / self.M_IN_KM / self.duration)
        return mean_speed_swm

    def get_spent_calories(self) -> float:
        calor_swm = (
                            (self.get_mean_speed() + self.RATIO_SWM_1)
                     ) * self.RATIO_SWM_2 * self.weight * self.duration
        return calor_swm


def read_package(workout_type: str,
                 data: list,
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""

    train_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    result = train_types[workout_type](*data)
    return result


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

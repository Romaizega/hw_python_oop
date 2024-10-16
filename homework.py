from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Training Information Notice."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Returns a message about the training."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Base class for training."""

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
        """To get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed of movement."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories burned."""
        raise NotImplementedError('Данный метод реализуется '
                                  'отделно для каждого дочернего класса')

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed training."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Training: running."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Get the amount of calories burned."""
        return (
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * self.weight / self.M_IN_KM * (
            self.duration * self.HOUR_TO_MIN
        )


class SportsWalking(Training):
    """Training: power walking."""

    MULTIPLIER_1_OF_WEIGHT: float = 0.035
    MULTIPLIER_2_OF_WEIGHT: float = 0.029
    KMH_TO_MSEC: float = 0.278
    M_TO_CM: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get the number of calories burned."""
        speed_into_ms = self.get_mean_speed() * self.KMH_TO_MSEC
        height_into_m = self.height / self.M_TO_CM
        duration_into_min = self.duration * self.HOUR_TO_MIN
        return (self.MULTIPLIER_1_OF_WEIGHT * self.weight
                + (speed_into_ms ** 2 / height_into_m)
                * self.MULTIPLIER_2_OF_WEIGHT
                * self.weight) * duration_into_min


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT_SWM: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER_SWM: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT_SWM)
            * (self.CALORIES_MEAN_SPEED_MULTIPLIER_SWM
                * self.weight * self.duration)
        )


TRAIN_TYPES: dict[str, type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list) -> Training:
    """Read data received from sensors."""

    if workout_type not in TRAIN_TYPES:
        raise ValueError(f'{workout_type}: неизвестный тип тренировки')
    return TRAIN_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
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

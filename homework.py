from typing import ClassVar, Union, Dict, List
from dataclasses import dataclass


@dataclass(repr=False, eq=False)
class InfoMessage():

    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {round(self.distance, 3):.3f} км; '
                f'Ср. скорость: {round(self.speed, 3):.3f} км/ч; '
                f'Потрачено ккал: {round(self.calories,3):.3f}.'
                )


@dataclass(repr=False, eq=False)
class Training:

    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar = 1000
    LEN_STEP: ClassVar = 0.65
    MINUTES_IN_HOUR: ClassVar = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories() в %s.' % (type(self).__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


@dataclass(repr=False, eq=False)
class Running(Training):

    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar = 18
    COEFF_CALORIE_2: ClassVar = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight
                / self.M_IN_KM * self.duration * self.MINUTES_IN_HOUR)


@dataclass(repr=False, eq=False)
class SportsWalking(Training):

    """Тренировка: спортивная ходьба."""
    height: float
    COEFF_CALORIE_1: ClassVar = 0.035
    COEFF_CALORIE_2: ClassVar = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_2 * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


@dataclass(repr=False, eq=False)
class Swimming(Training):

    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar = 1.38
    MEAN_SPEED: ClassVar = 1.1
    COEFF_CALORIE_1: ClassVar = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.MEAN_SPEED)
                * self.COEFF_CALORIE_1 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    CustomDict = Dict[str, Union['Running', 'SportsWalking', 'Swimming']]
    view_training: CustomDict = {'SWM': Swimming,
                                 'RUN': Running,
                                 'WLK': SportsWalking}
    return view_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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

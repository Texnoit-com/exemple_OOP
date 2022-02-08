from typing import Union


class InfoMessage():

    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {round(self.distance, 3):.3f} км; '
                f'Ср. скорость: {round(self.speed, 3):.3f} км/ч; '
                f'Потрачено ккал: {round(self.calories,3):.3f}.'
                )


class Training:

    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

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
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):

    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        weight_callorie: float = (self.COEFF_CALORIE_1 * self.get_mean_speed() - self.COEFF_CALORIE_2) * self.weight

        return weight_callorie / self.M_IN_KM * self.duration*60


class SportsWalking(Training):

    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        weight_calorie_1: float = self.COEFF_CALORIE_1 * self.weight
        weight_calorie_2: float = (weight_calorie_1 + (self.get_mean_speed()**2 // self.height) *
                                   self.COEFF_CALORIE_2 * self.weight)

        return weight_calorie_2 * self.duration*60


class Swimming(Training):

    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP: float = 1.38
    MEAN_SPEED: float = 1.1
    COEFF_CALORIE_1: float = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (self.get_mean_speed() + self.MEAN_SPEED) * self.COEFF_CALORIE_1 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    CustomDict = dict[str, Union['Running', 'SportsWalking', 'Swimming']]
    view_training: CustomDict = {
                                'SWM': Swimming,
                                'RUN': Running,
                                'WLK': SportsWalking,
                                }
    obj: Union['Running', 'SportsWalking', 'Swimming'] = view_training[workout_type](*data)
    return obj


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

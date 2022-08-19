from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    CONST_MESSAGE: str = ('Тип тренировки: {}; '
                          'Длительность: {:.3f} ч.; '
                          'Дистанция: {:.3f} км; '
                          'Ср. скорость: {:.3f} км/ч; '
                          'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return (self.CONST_MESSAGE.format(*asdict(self).values()))


class Training:

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        return (InfoMessage(self.__class__.__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        return ((self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_2 * self.weight) * self.duration * 60)


class Swimming(Training):
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    training_dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}

    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

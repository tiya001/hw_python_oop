class InfoMessage:
    def __init__(self,
                 training_type,
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
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
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
        pass

    def show_training_info(self) -> InfoMessage:
        info: InfoMessage = InfoMessage(self.__class__.__name__,
                                        self.duration,
                                        self.get_distance(),
                                        self.get_mean_speed(),
                                        self.get_spent_calories())
        return info


class Running(Training):
    def get_spent_calories(self) -> float:
        COEFF_CALORIE_1: int = 18
        COEFF_CALORIE_2: int = 20
        return ((COEFF_CALORIE_1 * self.get_mean_speed() - COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        COEFF_CALORIE_1: float = 0.035
        COEFF_CALORIE_2: float = 0.029
        return ((COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * COEFF_CALORIE_2 * self.weight) * self.duration * 60)


class Swimming(Training):
    LEN_STEP: float = 1.38

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
        COEFF_CALORIE_1: float = 1.1
        COEFF_CALORIE_2: int = 2
        return ((self.get_mean_speed() + COEFF_CALORIE_1)
                * COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    training_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type == 'SWM':
        workout_object: Swimming = training_dict[workout_type](
            data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        workout_object: Running = training_dict[workout_type](
            data[0], data[1], data[2])
    else:
        workout_object: SportsWalking = training_dict[workout_type](
            data[0], data[1], data[2], data[3])
    return workout_object


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

from homework_05.exceptions import LowFuelError, NotEnoughFuel

class Vehicle:
    """Базовый класс для транспортных средств"""
    
    def __init__(self, weight: float = 1000, fuel: float = 50, fuel_consumption: float = 5):
        """
        Инициализация транспортного средства
        
        :param weight: масса транспортного средства (кг)
        :param fuel: количество топлива (л)
        :param fuel_consumption: расход топлива (л/100 км)
        """
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption
        self.started = False
        
    def start(self) -> None:
        """Запуск транспортного средства"""
        if not self.started:
            if self.fuel > 0:
                self.started = True
            else:
                raise LowFuelError("Недостаточно топлива для запуска двигателя")
                
    def move(self, distance: float) -> None:
        """
        Перемещение транспортного средства на указанную дистанцию
        
        :param distance: дистанция в км
        :raises NotEnoughFuel: если топлива недостаточно для преодоления дистанции
        """
        required_fuel = (distance * self.fuel_consumption) / 100
        if self.fuel >= required_fuel:
            self.fuel -= required_fuel
        else:
            raise NotEnoughFuel("Недостаточно топлива для преодоления дистанции")
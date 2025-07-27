from homework_05.base import Vehicle
from homework_05.engine import Engine

class Car(Vehicle):
    """Класс автомобиля"""
    
    def __init__(self, weight: float = 1500, fuel: float = 50, fuel_consumption: float = 8):
        """
        Инициализация автомобиля
        
        :param weight: масса автомобиля (кг)
        :param fuel: количество топлива (л)
        :param fuel_consumption: расход топлива (л/100 км)
        """
        super().__init__(weight, fuel, fuel_consumption)
        self.engine: Engine = None
        
    def set_engine(self, engine: Engine) -> None:
        """
        Установка двигателя
        
        :param engine: экземпляр двигателя Engine
        """
        self.engine = engine
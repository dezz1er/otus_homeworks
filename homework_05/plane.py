from homework_05.base import Vehicle
from homework_05.exceptions import CargoOverload

class Plane(Vehicle):
    """Класс самолета"""
    
    def __init__(self, weight: float = 50000, fuel: float = 5000, 
                 fuel_consumption: float = 50, max_cargo: float = 20000):
        """
        Инициализация самолета
        
        :param weight: масса самолета (кг)
        :param fuel: количество топлива (л)
        :param fuel_consumption: расход топлива (л/100 км)
        :param max_cargo: максимальная грузоподъемность (кг)
        """
        super().__init__(weight, fuel, fuel_consumption)
        self.max_cargo = max_cargo
        self.cargo = 0
        
    def load_cargo(self, cargo: float) -> None:
        """
        Загрузка груза в самолет
        
        :param cargo: масса груза для загрузки (кг)
        :raises CargoOverload: если превышена максимальная грузоподъемность
        """
        if self.cargo + cargo > self.max_cargo:
            raise CargoOverload(f"Превышена максимальная грузоподъемность: {self.max_cargo} кг")
        self.cargo += cargo
        
    def remove_all_cargo(self) -> float:
        """
        Выгрузка всего груза из самолета
        
        :return: масса выгруженного груза (кг)
        """
        removed_cargo = self.cargo
        self.cargo = 0
        return removed_cargo
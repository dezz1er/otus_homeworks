class LowFuelError(Exception):
    """Исключение при недостатке топлива для запуска двигателя"""
    pass

class NotEnoughFuel(Exception):
    """Исключение при недостатке топлива для преодоления дистанции"""
    pass

class CargoOverload(Exception):
    """Исключение при перегрузке самолета"""
    pass
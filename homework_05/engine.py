from dataclasses import dataclass

@dataclass
class Engine:
    """Класс двигателя"""
    volume: float  # объем двигателя в литрах
    pistons: int   # количество поршней
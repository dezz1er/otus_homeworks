from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from domain.base import MediaFile

class Storage(ABC):
    """Абстрактный базовый класс для всех типов хранилищ."""
    
    @abstractmethod
    def save(self, media_file: MediaFile, path: str) -> bool:
        """Сохраняет файл в хранилище."""
        pass
        
    @abstractmethod
    def load(self, path: str) -> Optional[MediaFile]:
        """Загружает файл из хранилища."""
        pass
        
    @abstractmethod
    def delete(self, path: str) -> bool:
        """Удаляет файл из хранилища."""
        pass
        
    @abstractmethod
    def exists(self, path: str) -> bool:
        """Проверяет существование файла в хранилище."""
        pass
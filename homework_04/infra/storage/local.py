import shutil
from pathlib import Path
from typing import Optional
from domain.base import MediaFile
from homework_04.infra.base import Storage

class LocalStorage(Storage):
    """Класс для работы с локальным хранилищем файлов."""
    
    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path).resolve()
        
    def save(self, media_file: MediaFile, path: str) -> bool:
        """Сохраняет файл в локальное хранилище."""
        full_path = self.base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Здесь должна быть реализация сохранения файла
        print(f"Saving {media_file.name} to local storage at {full_path}")
        return True
        
    def load(self, path: str) -> Optional[MediaFile]:
        """Загружает файл из локального хранилища."""
        full_path = self.base_path / path
        if not full_path.exists():
            return None
            
        # Здесь должна быть реализация загрузки файла
        print(f"Loading file from local storage at {full_path}")
        return None  # В реальности возвращаем экземпляр MediaFile
        
    def delete(self, path: str) -> bool:
        """Удаляет файл из локального хранилища."""
        full_path = self.base_path / path
        if not full_path.exists():
            return False
            
        try:
            full_path.unlink()
            return True
        except OSError:
            return False
            
    def exists(self, path: str) -> bool:
        """Проверяет существование файла в локальном хранилище."""
        return (self.base_path / path).exists()
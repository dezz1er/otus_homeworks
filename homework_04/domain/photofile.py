from datetime import datetime
from .base import MediaFile
from typing import Dict, Any
from domain.base import MediaFile

class PhotoFile(MediaFile):
    """Класс для работы с фото файлами."""
    
    def __init__(self, name: str, size: int, owner: str, 
                 resolution: str, camera_model: str = None, **kwargs):
        """
        :param resolution: разрешение фото (например, '6000x4000')
        :param camera_model: модель камеры, если известна
        """
        super().__init__(name, size, owner, **kwargs)
        self.resolution = resolution
        self.camera_model = camera_model
        
    def get_specific_metadata(self) -> Dict[str, Any]:
        return {
            'resolution': self.resolution,
            'camera_model': self.camera_model
        }
        
    def process(self) -> None:
        """Выполняет обработку фото (например, изменение размера или применение фильтров)."""
        print(f"Processing photo {self.name}...")
        # Реализация обработки фото
        
    def detect_faces(self) -> None:
        """Обнаруживает лица на фото."""
        print(f"Detecting faces in {self.name}...")
        # Реализация обнаружения лиц
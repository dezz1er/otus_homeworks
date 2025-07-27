from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, Union, BytesIO

class MediaFile(ABC):
    """Абстрактный базовый класс для всех медиа-файлов."""
    
    def __init__(self, 
                 name: str, 
                 size: int, 
                 owner: str, 
                 content: Optional[Union[bytes, BytesIO]] = None,
                 created_at: datetime = None, 
                 **metadata):
        """
        Инициализация медиа-файла.
        
        :param name: имя файла
        :param size: размер файла в байтах
        :param owner: владелец файла
        :param content: содержимое файла (байты или BytesIO)
        :param created_at: дата создания файла
        :param metadata: дополнительные метаданные
        """
        self.name = name
        self.size = size
        self.owner = owner
        self._content = content
        self.created_at = created_at or datetime.now()
        self.metadata = metadata
        
    @property
    def content(self) -> Optional[Union[bytes, BytesIO]]:
        """Возвращает содержимое файла."""
        return self._content
        
    @content.setter
    def content(self, value: Union[bytes, BytesIO]) -> None:
        """Устанавливает содержимое файла и обновляет размер."""
        self._content = value
        if isinstance(value, bytes):
            self.size = len(value)
        elif isinstance(value, BytesIO):
            self.size = value.getbuffer().nbytes
            
    @abstractmethod
    def get_specific_metadata(self) -> Dict[str, Any]:
        """Возвращает специфичные для типа файла метаданные."""
        pass
        
    @abstractmethod
    def process(self) -> None:
        """Выполняет обработку файла (конвертация, извлечение фич и т.д.)."""
        pass
        
    def get_info(self) -> Dict[str, Any]:
        """Возвращает общую информацию о файле."""
        return {
            'name': self.name,
            'size': self.size,
            'owner': self.owner,
            'created_at': self.created_at,
            'type': self.__class__.__name__,
            'has_content': self.content is not None,
            **self.get_specific_metadata()
        }
        
    def clear_content(self) -> None:
        """Очищает содержимое файла (для экономии памяти)."""
        self._content = None
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', size={self.size}, owner='{self.owner}')"
import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from typing import Optional, Union, Dict, Any
from urllib.parse import urlparse
from domain.base import MediaFile
from domain.audiofile import AudioFile
from domain.photofile imoprt PhotoFile
from domain.videofile import VideoFile
from infra.base import Storage

class S3Storage(Storage):
    """Класс для работы с S3-совместимыми хранилищами."""
    
    def __init__(self, 
                 endpoint_url: str,
                 access_key: str,
                 secret_key: str,
                 bucket_name: str,
                 region: str = 'us-east-1',
                 secure: bool = True):
        """
        Инициализация S3 хранилища.
        
        :param endpoint_url: URL S3-совместимого сервиса (например, 'https://s3.amazonaws.com')
        :param access_key: ключ доступа
        :param secret_key: секретный ключ
        :param bucket_name: имя бакета
        :param region: регион (по умолчанию 'us-east-1')
        :param secure: использовать HTTPS (по умолчанию True)
        """
        self.endpoint_url = endpoint_url
        self.bucket_name = bucket_name
        self.region = region
        
        # Инициализация S3 клиента
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            use_ssl=secure
        )
        
    def save(self, media_file: MediaFile, path: str) -> bool:
        """Сохраняет файл в S3 хранилище."""
        if media_file.content is None:
            return False
            
        try:
            extra_args = self._get_upload_args(media_file)
            
            if isinstance(media_file.content, BytesIO):
                self.s3.upload_fileobj(
                    media_file.content,
                    self.bucket_name,
                    path,
                    ExtraArgs=extra_args
                )
            else:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=path,
                    Body=media_file.content,
                    **extra_args
                )
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False
            
    def load(self, path: str, load_content: bool = True) -> Optional[MediaFile]:
        """Загружает файл из S3 хранилища."""
        try:
            # Получаем метаданные
            head = self.s3.head_object(Bucket=self.bucket_name, Key=path)
            metadata = head.get('Metadata', {})
            
            # Определяем тип файла по content-type
            content_type = head.get('ContentType', 'application/octet-stream')
            
            # Создаем объект MediaFile
            media_file = self._create_media_file(
                name=path.split('/')[-1],
                size=head['ContentLength'],
                owner=head.get('Owner', {}).get('DisplayName', 'unknown'),
                created_at=head['LastModified'],
                content_type=content_type,
                metadata=metadata
            )
            
            if load_content:
                content = self.get_content(path)
                if content:
                    media_file.content = content
                    
            return media_file
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            print(f"Error loading file from S3: {e}")
            return None
            
    def get_content(self, path: str) -> Optional[Union[bytes, BytesIO]]:
        """Получает содержимое файла из S3."""
        try:
            buffer = BytesIO()
            self.s3.download_fileobj(self.bucket_name, path, buffer)
            buffer.seek(0)
            return buffer
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            return None
            
    def delete(self, path: str) -> bool:
        """Удаляет файл из S3 хранилища."""
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")
            return False
            
    def exists(self, path: str) -> bool:
        """Проверяет существование файла в S3."""
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise
            
    def _get_upload_args(self, media_file: MediaFile) -> Dict[str, Any]:
        """Генерирует дополнительные аргументы для загрузки."""
        args = {
            'Metadata': {
                'owner': media_file.owner,
                'created_at': media_file.created_at.isoformat(),
                **media_file.metadata
            }
        }
        
        # Устанавливаем ContentType в зависимости от типа файла
        if isinstance(media_file, AudioFile):
            args['ContentType'] = f'audio/{media_file.codec}'
        elif isinstance(media_file, VideoFile):
            args['ContentType'] = f'video/{media_file.codec}'
        elif isinstance(media_file, PhotoFile):
            args['ContentType'] = 'image/jpeg'  # или другой формат
            
        return args
        
    def _create_media_file(self, 
                         name: str,
                         size: int,
                         owner: str,
                         created_at,
                         content_type: str,
                         metadata: Dict[str, str]) -> MediaFile:
        """Создает соответствующий объект MediaFile на основе метаданных."""
        
        # Парсим дополнительные метаданные
        file_metadata = {
            k: v for k, v in metadata.items() 
            if not k.startswith('x-amz-')
        }
        
        if content_type.startswith('audio/'):
            codec = content_type.split('/')[-1]
            return AudioFile(
                name=name,
                size=size,
                owner=owner,
                content=None,
                created_at=created_at,
                duration=float(metadata.get('duration', 0)),
                bitrate=int(metadata.get('bitrate', 0)),
                codec=codec,
                **file_metadata
            )
        elif content_type.startswith('video/'):
            codec = content_type.split('/')[-1]
            return VideoFile(
                name=name,
                size=size,
                owner=owner,
                content=None,
                created_at=created_at,
                duration=float(metadata.get('duration', 0)),
                resolution=metadata.get('resolution', 'unknown'),
                codec=codec,
                fps=float(metadata.get('fps', 0)),
                **file_metadata
            )
        elif content_type.startswith('image/'):
            return PhotoFile(
                name=name,
                size=size,
                owner=owner,
                content=None,
                created_at=created_at,
                resolution=metadata.get('resolution', 'unknown'),
                camera_model=metadata.get('camera_model'),
                **file_metadata
            )
        else:
            # Для неизвестных типов возвращаем базовый MediaFile
            return MediaFile(
                name=name,
                size=size,
                owner=owner,
                content=None,
                created_at=created_at,
                **file_metadata
            )
            
    def generate_presigned_url(self, path: str, expires_in: int = 3600) -> Optional[str]:
        """Генерирует временную ссылку для доступа к файлу."""
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': path},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
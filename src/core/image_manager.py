import uuid
from typing import Dict, Optional


class ImageManager:
    """
    A class to manage storage and retrieval of image data using UUIDs.
    
    This class provides methods to store image strings with unique identifiers
    and retrieve them later using those identifiers.
    """
    
    def __init__(self):
        """Initialize the ImageManager with an empty dictionary to store images."""
        self._images: Dict[str, str] = {}
    
    def store(self, image_str: str) -> str:
        """
        Store an image string and return a unique identifier for it.
        
        Args:
            image_str: The image data as a string to be stored.
            
        Returns:
            str: A unique identifier (UUID) that can be used to retrieve the image.
        """
        if not image_str:
            raise ValueError("Image string cannot be empty")
            
        image_id = str(uuid.uuid4())
        self._images[image_id] = image_str
        return image_id
    
    def load(self, image_id: str) -> Optional[str]:
        """
        Retrieve an image string using its unique identifier.
        
        Args:
            image_id: The UUID of the image to retrieve.
            
        Returns:
            Optional[str]: The stored image string if found, None otherwise.
        """
        if not image_id:
            raise ValueError("Image ID cannot be empty")
            
        return self._images.get(image_id)

image_manager = ImageManager()
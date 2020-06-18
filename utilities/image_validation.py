from .exception_handler import CustomValidation
from rest_framework import status


def validate_image(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".jpg", ".png"]

    if not ext.lower() in valid_extensions:
        raise CustomValidation(
            "image", "Unsupported file format", status_code=status.HTTP_403_FORBIDDEN,
        )
    if value.size / (1024 * 1024) > 1:
        raise CustomValidation(
            "image",
            "File size should be less than or equal to 1 mb",
            status_code=status.HTTP_403_FORBIDDEN,
        )

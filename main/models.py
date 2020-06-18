from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from datetime import datetime
import uuid
from django.contrib.auth.models import (
    UserManager,
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and Save a new User"""
        if not email:
            raise ValueError("User must have email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Creates and save a new superuser"""
        if not email:
            raise ValueError("User must have email address")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instade of the default username"""

    id = models.UUIDField(
        primary_key=True, null=False, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name


def upload_path(instance, filename):
    """Storing an image with directory post_image with custom file name"""

    now = datetime.now()
    now_string = now.strftime("%d-%m-%Y %H:%M:%S")
    new_filename = now_string + filename
    return "/".join(["post_image", new_filename])


class Category(models.Model):
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class ItemModel(models.Model):
    itemId = models.UUIDField(
        primary_key=True, null=False, default=uuid.uuid4, editable=False
    )
    location = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    boost = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, related_name="post_owner", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    description = models.TextField()
    properties = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # fix this in develop as well


class ItemImageModel(models.Model):
    imageId = models.UUIDField(
        primary_key=True, null=False, default=uuid.uuid4, editable=False
    )
    item = models.ForeignKey(
        ItemModel, related_name="item_images", on_delete=models.CASCADE
    )
    image = models.FileField(null=False, blank=False, upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imageId

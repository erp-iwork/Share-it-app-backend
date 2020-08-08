from django.db import models
from django.contrib.postgres.fields import JSONField

from django.conf import settings
from datetime import datetime
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    UserManager,
)
from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils import Choices

RATING = Choices((1, "one"), (2, "two"), (3, "three"), (4, "four"), (5, "five"),)


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
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    avatar = models.ImageField(upload_to="media/profile_pics", default="no-img.png")
    cover_img = models.ImageField(upload_to="media/cover_pics", default="no-img.png")
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


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, null=False, default=uuid.uuid4, editable=False
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender_user"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver_user"
    )
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ("timestamp",)


class Rating(models.Model):
    """
    Rating user on a scale from one to 5
    """

    ratingId = models.AutoField(primary_key=True,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rater")
    rating = models.PositiveSmallIntegerField(choices=RATING)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} has {self.rating}"


class Profile(models.Model):
    """
    User Profile model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    telegram = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    phonenumber = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.name


class Category(models.Model):
    """
    Item category model
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    Item sub_category model
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="media/sub_category_icons")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ItemModel(models.Model):
    itemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    zip_code = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    boost = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    description = models.TextField()
    term_and_conditions = models.TextField()
    properties = JSONField(blank=True, null=True)
    is_donating = models.BooleanField(default=False)
    view = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.title


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
        return str(self.imageId)


class Follow(models.Model):
    """
    User Followers and following
    """

    follower = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )  # The person following
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )  # The person to be followed
    follow_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-follow_time"]

    def __unicode__(self):
        return str(self.follow_time)

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class SharingStatus(models.Model):
    """
    tracks shared and sharing items
    """

    transaction_type = models.CharField(max_length=255,)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_type

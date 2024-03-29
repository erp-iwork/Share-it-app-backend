from main.models import (
    Category,
    ItemImageModel,
    ItemModel,
    User,
    SharingStatus,
    SubCategory,
    Rating
)
from rest_framework import serializers, status
from user.serializers import UserSerializer, RatingSerializer
from utilities.exception_handler import CustomValidation
from utilities.image_validation import validate_image

# from drf_extra_fields.geo_fields import PointField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ("id", "name", "icon", "category", "category_id")


class SubCategoryByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "icon")


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImageModel
        fields = ("imageId", "image")


class ItemSerializer(serializers.ModelSerializer):
    item_images = ItemImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    owner_id = serializers.CharField(write_only=True)
    sub_category_id = serializers.CharField(write_only=True)
    sub_category = SubCategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField("get_all_rating")

    class Meta:
        model = ItemModel
        fields = "__all__"

    def get_all_rating(self, val):
        ratings = Rating.objects.filter(user=val.owner.id)
        rating = RatingSerializer(ratings, many=True)
        return rating.data

    def create(self, validated_data):
        """Validate the length images >2"""
        if len(self.context.get("request").FILES) < 2:
            raise CustomValidation(
                "image",
                "You should attach atleast two images",
                status.HTTP_400_BAD_REQUEST,
            )

        # Iterate and validate images before saving the post
        for i in self.context.get("request").FILES.values():
            validate_image(i)
        try:
            # Create item or product
            item = ItemModel.objects.create(**validated_data)
            user = self.context.get("request").user
            if item.is_donating:
                SharingStatus.objects.create(
                    transaction_type="Donating", user=user, item=item
                )
            else:
                SharingStatus.objects.create(
                    transaction_type="Sharing", user=user, item=item
                )

        except Exception as e:
            raise CustomValidation()

        # Iterate and create images for using an item instance
        for i in self.context.get("request").FILES.values():
            try:
                ItemImageModel.objects.create(image=i, item=item)
            except Exception as e:
                ItemModel.objects.get(itemId=item.itemId).delete()
                raise CustomValidation(
                    "image",
                    "There is a problem of saving an images, please try again",
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return item


class ItemhistorySerializer(serializers.ModelSerializer):
    """
    serializer that gives selling item title and itemId
    """

    class Meta:
        model = ItemModel
        fields = ("itemId", "title")


class TransactionSerializer(serializers.ModelSerializer):
    """
    serializers for user postign itme serializer
    """

    item = ItemhistorySerializer(read_only=True)

    class Meta:
        model = SharingStatus
        fields = ("transaction_type", "item", "user", "transaction_time")
        write_only_fields = "user"

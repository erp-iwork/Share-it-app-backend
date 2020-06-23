from main.models import Category, ItemImageModel, ItemModel, User
from rest_framework import serializers, status
from user.serializers import UserSerializer
from utilities.exception_handler import CustomValidation
from utilities.image_validation import validate_image
from drf_extra_fields.geo_fields import PointField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImageModel
        fields = ("imageId", "image")


class ItemSerializer(serializers.ModelSerializer):
    item_images = ItemImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    owner_id = serializers.CharField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.CharField(write_only=True)
    location = PointField(write_only=True, allow_null=True)

    class Meta:
        model = ItemModel
        fields = "__all__"

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

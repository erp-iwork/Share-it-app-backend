import json

from django_filters import rest_framework as filters
from main.models import Category, ItemImageModel, ItemModel
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from utilities.exception_handler import CustomValidation
from utilities.permission import IsAuthenticatedOrReadOnly

from .serializers import CategorySerializer, ItemSerializer


class CategoryList(generics.ListAPIView):
    """Return all categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


from main.models import ItemImageModel, ItemModel, Category
from .serializers import ItemSerializer, CategorySerializer

# Add or post item api view with multiple images
class CategoryList(generics.ListAPIView):
    """Allow to post item only authenticated user"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = "category_id"


class ItemListAdd(generics.ListCreateAPIView):
    """
    Allow to post item only authenticated user
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "itemId"

    def post(self, request):
        # Passing request of data and the request context for files
        serializer = ItemSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ItemRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    View that can handle item get, update and delete
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ItemSerializer
    queryset = ItemModel.objects.all()
    lookup_field = "itemId"

    def get(self, request, itemId=None):
        return self.retrieve(request, itemId)

    def put(self, request, itemId=None):
        return self.update(request, itemId)

    def delete(self, request, itemId=None):
        return self.destroy(request, itemId)  # send custom deletion success message


class UserItemList(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of all the items posted
        for the currently authenticated user.
        """
        user = self.request.user
        return ItemModel.objects.filter(owner=user)


class ItemFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = ItemModel
        fields = ["category", "min_price", "max_price", "condition"]


class ItemFilterView(generics.ListAPIView):
    """
    Return items in specific category
    """

    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ItemFilter


class PropertyFilterView(generics.ListAPIView):
    """
    Return items filtered by property in a given category
    """

    serializer_class = ItemSerializer
    queryset = ItemModel.objects.all()

    def get_queryset(self):
        category = self.request.query_params.get("category", None)
        property = self.request.query_params.get("property", None)
        property_dict = json.loads(property)
        return ItemModel.objects.filter(
            category=category, properties__contains=property_dict
        )

import json

from django_filters import rest_framework as filters
from main.models import Category, ItemImageModel, ItemModel, SharingStatus
from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from utilities.exception_handler import CustomValidation
from utilities.permission import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import CategorySerializer, ItemSerializer, TransactionSerializer


class CategoryList(generics.ListAPIView):
    """Return all categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionList(generics.ListAPIView):
    """Return all user transaction history"""

    queryset = SharingStatus.objects.all()
    serializer_class = TransactionSerializer


class ItemListAdd(generics.ListCreateAPIView):
    """
    Allow to post item only authenticated user
    """

    # permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "itemId"

    def post(self, request):
        print(self.request.user.id)
        # Passing request of data and the request context for files
        # print(self.request.user.id)
        # request.data["user"] = self.request.user.id
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
    filter_backends = (
        filters.DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ["title"]
    ordering_fields = ["created_at", "title", "updated_at"]
    ordering = ["created_at"]
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

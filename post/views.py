import json

from django_filters import rest_framework as filters
from main.models import Category, ItemImageModel, ItemModel, SharingStatus, SubCategory
from rest_framework import authentication, generics, permissions, status, pagination
from rest_framework.response import Response
from utilities.exception_handler import CustomValidation
from utilities.permission import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

# from django.contrib.gis import geoip2
# from geopy import distance, Nominatim, GoogleV3
# from geopy.distance import lonlat, distance as dis, Point, geodesic

from .serializers import (
    CategorySerializer,
    ItemSerializer,
    TransactionSerializer,
    SubCategorySerializer,
    SubCategoryByCategorySerializer,
)


class CategoryList(generics.ListAPIView):
    """Return all categories"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    View that can handle item get, update and delete
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"

    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.partial_update(request, id)


def delete(self, request, id=None):
    # send custom deletion success message
    return self.destroy(request, id)


class subCategoryList(generics.ListAPIView):
    """Return all categories"""

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class subCategoryRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    View that can handle item get, update and delete
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = "id"

    def get(self, request, id=None):
        return self.retrieve(request, id)

    def put(self, request, id=None):
        return self.partial_update(request, id)

    def delete(self, request, id=None):
        # send custom deletion success message
        return self.destroy(request, id)


class SubCategoryByCategoryIdList(generics.ListAPIView):
    """ List sub categories in a category """

    serializer_class = SubCategoryByCategorySerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("id", None)
        category = Category.objects.get(id=category_id)
        return category.subcategory_set.all()


class TransactionList(generics.ListAPIView):
    """Return all user transaction history"""

    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all posts(sharing or donating) and buyings
        for the currently authenticated user.
        """

        user = self.request.user
        return SharingStatus.objects.filter(user=user)


class ItemListAdd(generics.ListCreateAPIView):
    """
    Allow to post item only authenticated user
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = ItemModel.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "itemId"

    def post(self, request):
        serializer = ItemSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SharedItemRUD(generics.RetrieveAPIView):
    """
    View that can handle item get, update and delete
    """

    serializer_class = ItemSerializer
    queryset = ItemModel.objects.all()
    lookup_field = "itemId"

    def get(self, request, itemId=None):
        return self.retrieve(request, itemId)


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
        return self.partial_update(request, itemId)

    def delete(self, request, itemId=None):
        # send custom deletion success message
        return self.destroy(request, itemId)


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


# class NearByItemsList(generics.ListAPIView):
#     """
#     gives items that are near to the logged in user
#     """

#     serializer_class = ItemSerializer
#     # permission_classes = (IsAuthenticatedOrReadOnly,)

#     def get_queryset(self):
#         user_location = self.request.user.location
#         print("the cahnged distance is")
#         # print(lonlat(user_location))
#         # geo_locator = Nominatim(user_agent="post")
#         # location = geo_locator.geocode("Addis Ababa")
#         point_a = Point(30, 30)
#         point_b = Point(50, 50)
#         point_c = Point(31, 31)
#         item_distance_miles = geodesic(point_a, point_b).miles
#         item_distance = geodesic(point_a, point_b).km
#         item_distance_2 = dis(point_a, point_c).meters
#         print(f"the point a {point_a}")
#         print("the location is")
#         print(item_distance)
#         print(item_distance_miles)
#         print(item_distance_2)
#         geo_locator = Nominatim(user_agent="post")
#         location = geo_locator.geocode("Addis ababa")  # This needs internet connection
#         print(f"addis ababa location is {location}")


class CustomPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size = 50
    max_page_size = 100


class ItemFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = ItemModel
        fields = ["sub_category", "category",
                  "min_price", "max_price", "condition"]


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
    pagination_class = CustomPagination


class PropertyFilterView(generics.ListAPIView):
    """
    Return items filtered by property in a given category
    """

    serializer_class = ItemSerializer
    queryset = ItemModel.objects.all()

    def get_queryset(self):
        sub_category = self.request.query_params.get("sub_category", None)
        property = self.request.query_params.get("property", None)
        property_dict = json.loads(property)
        return ItemModel.objects.filter(
            sub_category=sub_category, properties__contains=property_dict
        )

from rest_framework import authentication, generics, permissions, status
from rest_framework.response import Response
from utilities.exception_handler import CustomValidation
from utilities.permission import IsAuthenticatedOrReadOnly

from main.models import ItemImageModel, ItemModel, Category
from .serializers import ItemSerializer, CategorySerializer

# Add or post item api view with multiple images
class CategoryList(generics.ListAPIView):
    """Allow to post item only authenticated user"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field = "category_id"


# Add or post item api view with multiple images
class ItemListAdd(generics.ListCreateAPIView):
    """Allow to post item only authenticated user"""

#     permission_classes = (IsAuthenticatedOrReadOnly,)

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
    """View that can handle item get, update and delete"""

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

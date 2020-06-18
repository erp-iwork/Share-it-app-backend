from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .views import CategoryList, ItemListAdd, ItemRUD

app_name = "post"

urlpatterns = [
    path("item/", ItemListAdd.as_view(), name="item_add_list"),
    path("category/", CategoryList.as_view(), name="category"),
    path("item/<str:itemId>/", ItemRUD.as_view(), name="item_rud"),
]
# Adding static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
